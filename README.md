# Calculadora de Edad

Proyecto de cálculo de edad, signo zodiacal y próximos cumpleaños implementado con **Pyro5** para exponer la lógica como un objeto remoto.

## Arquitectura

- `backend/`: lógica Pyro, puente web y cliente de consola.
- `frontend/`: interfaz web estática.

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

Breve guía para desplegar la app:

- Frontend (Vercel): despliega la carpeta `frontend/` como sitio estático. Puedes conectar tu repositorio GitHub a Vercel y seleccionar `frontend` como el directorio raíz del proyecto. También hemos incluido `vercel.json` para ayudar a Vercel a servir los archivos estáticos.

- Backend (Render): crea un servicio web en Render que apunte al repositorio y use este comando de inicio:

```bash
python backend/web_bridge.py
```

`web_bridge.py` intentará arrancar `pyro_server.py` como proceso hijo si no hay un servidor Pyro activo, por lo que en Render no hace falta configurar procesos separados.

Notas de configuración:
- Si Render requiere que el servidor escuche en el puerto indicado por la variable de entorno `PORT`, `web_bridge.py` ya lo soporta.
- Cuando publiques el frontend en Vercel y el backend en Render, actualiza `frontend/script.js` para apuntar a la URL pública de Render (por ejemplo `https://mi-backend.onrender.com/api/calculate`) cambiando la constante `API_URL`. Actualmente el valor por defecto es relativo (`/api/calculate`) y funciona si frontend y backend se sirven desde la misma origen.

### Pasos detallados

- Desplegar frontend en Vercel:
	1. En Vercel, crea un nuevo proyecto y conecta tu repositorio GitHub.
	2. Selecciona la carpeta `frontend` como root si se te pide el Directorio de Proyecto.
	3. Tipo de despliegue: static. `vercel.json` incluido debería servir los archivos estáticos.
	4. (Opcional) Si necesitas que el frontend apunte a la URL pública del backend, en Vercel añade una variable de entorno `API_BASE_URL` y cambia `frontend/script.js` para leerla en tiempo de build o inyectarla en `index.html`.

- Desplegar backend en Render:
	1. En Render, crea un nuevo `Web Service`.
	2. Selecciona tu repositorio y elige la rama a desplegar.
	3. En `Start Command` usa `python app.py`.
	4. Asegúrate de que `requirements.txt` esté en la raíz para instalar dependencias.
	5. Render asignará y expondrá la variable de entorno `PORT`; `web_bridge.py` ya la lee automáticamente.
	6. (Opcional) Si quieres exponer solo el backend HTTP (sin los archivos estáticos), configura `Start Command` a `python backend/web_bridge.py`.

### Comprobación local rápida

Inicia todo localmente con:

```bash
python app.py
# abre http://localhost:8000 en tu navegador
```

Para probar solo la API (sin frontend):

```bash
curl -X POST http://localhost:8000/api/calculate -H "Content-Type: application/json" -d '{"birth_year":1990}'
```

Este comando levanta el servidor Pyro si no está activo y después inicia el puente web.

### 2. Abrir la interfaz

- `http://127.0.0.1:8000`

### 3. Usar el cliente de consola

```bash
python age_calculator.py
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

## Observación

No se utilizaron Docker, kubectl ni Kubernetes en este proyecto.
