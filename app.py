from flask import Flask, render_template, request, jsonify, make_response
import sqlite3
import hashlib
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect('votaciones.db')
    c = conn.cursor()
    
    # Tabla de votos (con IP y Cookie)
    c.execute('''CREATE TABLE IF NOT EXISTS votos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT NOT NULL,
        cookie_hash TEXT NOT NULL,
        nombre_votante TEXT NOT NULL,
        candidato TEXT NOT NULL,
        puntaje INTEGER NOT NULL,
        fecha_voto TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Tabla de estadísticas por candidato
    c.execute('''CREATE TABLE IF NOT EXISTS estadisticas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidato TEXT UNIQUE NOT NULL,
        total_votos INTEGER DEFAULT 0,
        promedio_puntaje REAL DEFAULT 0,
        suma_puntajes INTEGER DEFAULT 0
    )''')
    
    # Insertar candidatos si no existen
    candidatos = ['Emilia', 'Oscar']
    for candidato in candidatos:
        c.execute('INSERT OR IGNORE INTO estadisticas (candidato, total_votos, promedio_puntaje, suma_puntajes) VALUES (?, 0, 0, 0)',
                 (candidato,))
    
    conn.commit()
    conn.close()

# Función para actualizar estadísticas
def actualizar_estadisticas(candidato, puntaje):
    conn = sqlite3.connect('votaciones.db')
    c = conn.cursor()
    
    c.execute('SELECT total_votos, suma_puntajes FROM estadisticas WHERE candidato = ?', (candidato,))
    resultado = c.fetchone()
    
    if resultado:
        total_votos, suma_puntajes = resultado
        nuevo_total = total_votos + 1
        nueva_suma = suma_puntajes + puntaje
        nuevo_promedio = nueva_suma / nuevo_total
        
        c.execute('''UPDATE estadisticas 
                    SET total_votos = ?, promedio_puntaje = ?, suma_puntajes = ?
                    WHERE candidato = ?''', 
                 (nuevo_total, nuevo_promedio, nueva_suma, candidato))
    
    conn.commit()
    conn.close()

# Función para obtener estadísticas
def obtener_estadisticas():
    conn = sqlite3.connect('votaciones.db')
    c = conn.cursor()
    c.execute('SELECT candidato, total_votos, promedio_puntaje FROM estadisticas ORDER BY candidato')
    stats = c.fetchall()
    conn.close()
    return stats

# Función para generar hash de cookie
def generar_cookie_hash(cookie_value):
    return hashlib.sha256(cookie_value.encode()).hexdigest()

# Función para verificar si ya votó (IP OR Cookie)
def ya_voto(ip, cookie_hash, candidato):
    conn = sqlite3.connect('votaciones.db')
    c = conn.cursor()
    # Verificar si la IP o la Cookie ya votaron por este candidato
    c.execute('''SELECT * FROM votos 
                WHERE (ip = ? OR cookie_hash = ?) AND candidato = ?''', 
             (ip, cookie_hash, candidato))
    resultado = c.fetchone()
    conn.close()
    return resultado is not None

# Función para obtener los votos del usuario (IP OR Cookie)
def obtener_votos_usuario(ip, cookie_hash):
    conn = sqlite3.connect('votaciones.db')
    c = conn.cursor()
    c.execute('''SELECT candidato FROM votos 
                WHERE ip = ? OR cookie_hash = ?''', 
             (ip, cookie_hash))
    resultados = c.fetchall()
    conn.close()
    return [r[0] for r in resultados]

# Ruta principal
@app.route('/')
def index():
    cookie_value = request.cookies.get('voto_session')
    if not cookie_value:
        cookie_value = hashlib.sha256(os.urandom(32)).hexdigest()
    
    cookie_hash = generar_cookie_hash(cookie_value)
    ip = request.remote_addr
    
    votos_usuario = obtener_votos_usuario(ip, cookie_hash)
    estadisticas = obtener_estadisticas()
    
    response = make_response(render_template('index.html', 
                                           votos_usuario=votos_usuario,
                                           estadisticas=estadisticas,
                                           ip=ip))
    
    if not request.cookies.get('voto_session'):
        response.set_cookie('voto_session', cookie_value, max_age=365*24*60*60)
    
    return response

# Ruta para votar
@app.route('/votar', methods=['POST'])
def votar():
    data = request.get_json()
    nombre_votante = data.get('nombre_votante')
    candidato = data.get('candidato')
    puntaje = data.get('puntaje')
    
    # Validar datos
    if not nombre_votante or not candidato or puntaje is None:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    # Validar candidato
    if candidato not in ['Emilia', 'Oscar']:
        return jsonify({'error': 'Candidato inválido'}), 400
    
    try:
        puntaje = int(puntaje)
        if puntaje < 0 or puntaje > 100:
            return jsonify({'error': 'Puntaje fuera de rango (0-100)'}), 400
    except ValueError:
        return jsonify({'error': 'Puntaje inválido'}), 400
    
    # Verificar sesión
    ip = request.remote_addr
    cookie_value = request.cookies.get('voto_session')
    if not cookie_value:
        return jsonify({'error': 'Sesión no válida'}), 400
    
    cookie_hash = generar_cookie_hash(cookie_value)
    
    # Verificar si ya votó (IP OR Cookie)
    if ya_voto(ip, cookie_hash, candidato):
        return jsonify({'error': f'Ya has votado por {candidato} (IP o Cookie registrada)'}), 400
    
    # Guardar voto
    try:
        conn = sqlite3.connect('votaciones.db')
        c = conn.cursor()
        c.execute('''INSERT INTO votos (ip, cookie_hash, nombre_votante, candidato, puntaje) 
                    VALUES (?, ?, ?, ?, ?)''', 
                 (ip, cookie_hash, nombre_votante, candidato, puntaje))
        conn.commit()
        conn.close()
        
        # Actualizar estadísticas
        actualizar_estadisticas(candidato, puntaje)
        
        return jsonify({'success': True, 'message': f'Voto por {candidato} registrado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener estadísticas (API)
@app.route('/estadisticas')
def estadisticas():
    stats = obtener_estadisticas()
    return jsonify(stats)

# Inicializar base de datos al iniciar
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
