# 🗳️ Sistema de Votaciones

> **⚠️ ADVERTENCIA:** Este sistema contiene vulnerabilidades de seguridad que fueron creadas **accidentalmente** durante su desarrollo. No utilizar en entornos de producción.

## 📋 Descripción

Sistema de votación web construido con Flask que, debido a errores accidentales en su desarrollo, presenta múltiples fallos de seguridad. Ideal para identificar y corregir vulnerabilidades comunes.

## 🎯 El Desafío del Investigador

Este sistema ha sido diseñado con vulnerabilidades **no intencionadas** que surgieron durante su desarrollo. La tarea del investigador de ciberseguridad es precisamente descubrirlas, identificarlas y proponer soluciones. Las vulnerabilidades pueden estar ocultas en diferentes capas del sistema: desde la interfaz de usuario hasta la lógica del servidor y la base de datos. El reto consiste en aplicar técnicas de pentesting para encontrar estos fallos, entender su origen y aprender cómo prevenirlos en sistemas reales.

## 🚀 Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/sistema-votaciones-vulnerable.git
cd sistema-votaciones-vulnerable

# Instalar dependencias
pip install flask

# Ejecutar
python app.py
```

El sistema estará disponible en: `http://localhost:5000`

## 🎯 Características

- Votación por 2 candidatos (Emilia 👩, Oscar 👨)
- Sistema de puntuación (0-100)
- Control de votos por IP y cookie
- Estadísticas en tiempo real
- Interfaz responsiva

## ⚠️ Vulnerabilidades Accidentales

El sistema presenta errores de seguridad que surgieron **sin intención** durante el desarrollo:

- Fallos en la validación de entradas
- Posibles problemas de inyección
- Errores en el manejo de sesiones
- Validación insuficiente de datos
- Posibles race conditions

## 🔧 Requisitos

- Python 3.6+
- Flask
- SQLite3

## 📄 Licencia

MIT - Proyecto para fines educativos y de aprendizaje
