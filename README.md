
# Proyecto: Jugadores Más Valiosos de Transfermarkt
![Logo de GitHub](https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png)

Este proyecto tiene como objetivo obtener datos de jugadores de fútbol desde la API de Transfermarkt y almacenarlos en una base de datos PostgreSQL para su posterior análisis y visualización en Power BI.

## Descripción del Proyecto

Se han creado varios scripts en Python que realizan diferentes funciones, desde la creación de tablas en PostgreSQL hasta la extracción, transformación y carga (ETL) de datos de jugadores. Los datos incluyen perfiles de jugadores, su historial de valor de mercado, y las asociaciones de países con sus respectivos continentes.

### Componentes del Proyecto

1. **Creación de Tablas:**
   - `Creacion_Tabla_Perfil_jugador.py`: Crea la tabla `player_profile` en PostgreSQL para almacenar la información de los perfiles de jugadores, como nombre, fecha de nacimiento, posición, nacionalidad, entre otros detalles.
   - `Creacion_Tabla_Precio_jugador.py`: Crea la tabla `market_value_history` para almacenar el historial del valor de mercado de los jugadores.
   - `Creacion_Tabla_Continente.py`: Crea la tabla `countries` para asociar cada país con su respectivo continente.

2. **ETL de Datos:**
   - `ETL_Perfil_Jugador.py`: Extrae datos de perfil de los jugadores desde la API de Transfermarkt y los inserta en la tabla `player_profile` de PostgreSQL.
   - `ETL_Precio_Jugador.py`: Extrae el historial de valor de mercado de los jugadores desde la API de Transfermarkt y lo inserta en la tabla `market_value_history`.

3. **Visualización:**
   - Se utiliza Power BI para conectar a la base de datos de PostgreSQL y crear visualizaciones dinámicas, como la de los 11 jugadores más valiosos en una formación de fútbol.

### Requisitos

- Python 3.x
- PostgreSQL
- Librerías de Python: `psycopg2`, `requests`
- Power BI

### Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   ```

2. **Instalar dependencias de Python:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar PostgreSQL:**
   - Asegúrate de tener PostgreSQL instalado y ejecutándose en tu máquina.
   - Modifica los scripts de Python con tus credenciales de PostgreSQL (host, usuario, contraseña, etc.).

4. **Crear las Tablas en PostgreSQL:**
   Ejecuta los scripts de creación de tablas:
   ```bash
   python Creacion_Tabla_Perfil_jugador.py
   python Creacion_Tabla_Precio_jugador.py
   python Creacion_Tabla_Continente.py
   ```

5. **Ejecutar los scripts ETL:**
   - Ejecuta los scripts ETL para cargar los datos en las tablas:
   ```bash
   python ETL_Perfil_Jugador.py
   python ETL_Precio_Jugador.py
   ```

### Uso

Una vez que los datos estén cargados en PostgreSQL, puedes utilizar Power BI para conectarte a la base de datos y crear visualizaciones. La imagen adjunta (`PBI.PNG`) muestra un ejemplo de cómo se visualizan los 11 jugadores más valiosos.

### Contribuciones

Si deseas contribuir a este proyecto, siéntete libre de abrir un pull request o enviar tus sugerencias a través de issues.

### Licencia

Este proyecto se distribuye bajo la licencia MIT. Para más detalles, consulta el archivo LICENSE.
