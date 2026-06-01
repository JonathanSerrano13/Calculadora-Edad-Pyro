# Calculadora de Edad

Proyecto de cálculo de edad, signo zodiacal y próximos cumpleaños implementado con **Pyro5** para exponer la lógica como un objeto remoto.

## Arquitectura

- `backend/`: lógica Pyro, puente web y cliente de consola.
- `frontend/`: interfaz web estática.
 
## Estructura del proyecto

```
Proyecto Pyro/
├─ app.py
├─ pyro_uri.txt
├─ README.md
├─ render.yaml
├─ requirements.txt
├─ backend/
│  ├─ __init__.py
│  ├─ age_calculator.py
│  ├─ calculator_service.py
│  ├─ pyro_client.py
│  ├─ pyro_server.py
│  └─ web_bridge.py
└─ frontend/
	├─ index.html
	├─ script.js
	└─ style.css
```
 
## Descripción de archivos

- `app.py`: Punto de entrada; arranca el servidor web y el puente Pyro si procede.
- `pyro_uri.txt`: Almacena la URI del servidor Pyro para clientes locales.
- `render.yaml`: Configuración y metadata para desplegar en Render.
- `requirements.txt`: Lista de dependencias Python necesarias.

- `backend/__init__.py`: Marca el paquete `backend`.
- `backend/age_calculator.py`: Lógica para calcular edad, próximos cumpleaños y signo zodiacal.
- `backend/calculator_service.py`: Adaptador/servicio que encapsula la lógica del calculador.
- `backend/pyro_client.py`: Cliente que consume el servicio expuesto por Pyro.
- `backend/pyro_server.py`: Servidor Pyro que registra el objeto remoto con la lógica.
- `backend/web_bridge.py`: Puente HTTP que expone una API REST y arranca Pyro si es necesario.

- `frontend/index.html`: Página principal de la interfaz web.
- `frontend/script.js`: Lógica cliente (fetch a la API, manejo de la UI).
- `frontend/style.css`: Estilos y diseño de la interfaz web.

## Requisitos

- Python 3.14 o superior.
- Pyro5 instalado desde `requirements.txt`.
- Navegador moderno para la versión web.

## Instalación

```bash
python -m pip install -r requirements.txt
```

## Ejecución

### 1. Iniciar todo con un solo comando

```bash
python app.py
```

## Despliegue

Breve guía para desplegar la app en Render:

- Crea un `Web Service` en Render apuntando al repositorio.
- Usa este comando de inicio:

```bash
python app.py
```

`app.py` inicia el puente web, y `web_bridge.py` arranca `pyro_server.py` como proceso hijo si no hay un servidor Pyro activo, así que no hace falta configurar procesos separados.

Notas de configuración:
- Si Render requiere que el servidor escuche en el puerto indicado por la variable de entorno `PORT`, `web_bridge.py` ya lo soporta.
- Si cambias la URL pública del backend, actualiza `frontend/script.js` para apuntar a la ruta correcta de la API. El valor por defecto es relativo (`/api/calculate`) y funciona cuando todo se sirve desde el mismo origen.

### Pasos detallados

- Desplegar en Render:
	1. En Render, crea un nuevo `Web Service`.
	2. Selecciona tu repositorio y elige la rama a desplegar.
	3. En `Start Command` usa `python app.py`.
	4. Asegúrate de que `requirements.txt` esté en la raíz para instalar dependencias.
	5. Render asignará y expondrá la variable de entorno `PORT`; `web_bridge.py` ya la lee automáticamente.

### Comprobación local rápida

Inicia todo localmente con:

```bash
python app.py
# abre http://localhost:8000 en tu navegador
```

Para probar solo la API (sin frontend):

```bash
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/calculate -ContentType "application/json" -Body (@{ birthdate = "1990-01-01" } | ConvertTo-Json -Compress)
```

Este comando levanta el servidor Pyro si no está activo y después inicia el puente web. En PowerShell, `Invoke-RestMethod` 

### 2. Abrir la interfaz

- `http://127.0.0.1:8000`

### 3. Usar el cliente de consola

```bash
python backend/age_calculator.py
```

Si el servidor Pyro no está activo, el cliente de consola y el puente web intentan iniciarlo automáticamente.

## Formatos aceptados

- `DD/MM/AAAA`
- `AAAA-MM-DD`

## Tecnologías usadas

- HTML5
- CSS3
- JavaScript
- Python 3
- Pyro5

