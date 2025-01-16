# Bot de Discord

## Requisitos Previos

Antes de empezar, asegúrate de tener lo siguiente:

- Python 3.7 o superior instalado en tu sistema.
- Una cuenta de Discord y acceso a tu servidor de Discord.

### Instalación de Python

#### Windows

1. Descarga el instalador de Python desde [python.org](https://www.python.org/downloads/).
2. Durante la instalación, **marca la casilla** "Add Python to PATH" antes de hacer clic en "Install Now".
3. Una vez completada la instalación, abre la terminal (símbolo del sistema) y ejecuta:

   ```bash
   python --version
   ```

   Esto debería mostrar la versión de Python que instalaste. Si todo está correcto, ya tienes Python instalado.

#### Linux

1. En la mayoría de las distribuciones de Linux, python viene preinstalado, pero en caso de que no, en distribuciones basadas en Debian (Como ubuntu) podes instalarlo de la siguiente forma:

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. Verifica la instalación con:

   ```bash
   python3 --version
   ```

   Esto debería mostrar la versión de Python que tienes instalada.

## Configuración del Entorno de Desarrollo

1. **Accede al directorio del proyecto**:
   Abre una terminal y navega hasta la carpeta de tu proyecto. Puedes hacerlo con el siguiente comando:

   ```bash
   cd ruta/a/tu/proyecto
   ```

2. **Crear un entorno virtual**:

   En la terminal, ejecuta el siguiente comando para crear un entorno virtual en la carpeta del proyecto:

   ```bash
   python -m venv .venv
   ```

   Esto creará una carpeta llamada `venv` en tu proyecto, que contendrá el entorno virtual.

3. **Activar el entorno virtual**:

   - En **Windows**, ejecuta:

     ```bash
     .\.venv\Scripts\activate
     ```

   - En **Linux** o **Mac**, ejecuta:

     ```bash
     source .venv/bin/activate
     ```

   Después de activar el entorno, deberías ver algo como `(venv)` antes de la línea de comando, lo que indica que estás trabajando dentro del entorno virtual.

4. **Instalar las dependencias del proyecto**:

   Con el entorno virtual activado, instala las dependencias que están en el archivo `requirements.txt` ejecutando:

   ```bash
   pip install -r requirements.txt
   ```

5. **Crear el archivo `.env`**:

   En la raíz de tu proyecto, crea un archivo llamado `.env` (sin extensión). Dentro de este archivo, necesitarás definir dos variables de entorno:

   ```bash
   DISCORD_TOKEN=tu_token_aqui
   POINTS_LOGS_CHANNEL=ID_del_canal_aqui
   ```

   - **Obtener el DISCORD_TOKEN**: Para obtener el token de tu bot de Discord, sigue estos pasos:
     1. Dirígete a [Discord Developer Portal](https://discord.com/developers/applications).
     2. Selecciona tu aplicación (bot).
     3. En la sección "Bot" de la izquierda, bajo "TOKEN", haz clic en **Copy**. Este es tu `DISCORD_TOKEN`.

   - **Obtener el POINTS_LOGS_CHANNEL**:
     1. En tu servidor de Discord, haz clic derecho sobre el canal donde deseas que se registren los logs de puntos.
     2. Selecciona **Copiar ID**. Si no ves esta opción, asegúrate de tener habilitado el "Modo de Desarrollador" en Discord. Para activarlo:
        - En Discord, ve a **Ajustes de Usuario > Apariencia** y activa **Modo Desarrollador**.
     3. El ID copiado será el que debes pegar en el archivo `.env` como valor de `POINTS_LOGS_CHANNEL`.

## Ejecutar el Bot

Una vez que todo esté configurado, puedes ejecutar el bot con el siguiente comando:

```bash
python main.py
```

Cualquier duda contactame por Discord y te respondere en cuanto pueda. Suerte!
