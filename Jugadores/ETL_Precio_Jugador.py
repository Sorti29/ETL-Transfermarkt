import requests
import psycopg2
from datetime import datetime

# Base URL de la API
base_url = "https://transfermarkt-api.fly.dev/players/{}/market_value"

# Función para conectar a la base de datos
def connect_db():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="9893",
        database="postgres"
    )

# Conectar a la base de datos
connection = connect_db()
cursor = connection.cursor()

# Lista para almacenar los IDs que fallan
failed_ids = []

# Función para convertir el valor a un número
def parse_market_value(value):
    if value:
        try:
            # Remover el símbolo de euro y convertir a número
            return float(value.replace('€', '').replace('k', '000').replace('m', '000000').replace('.', ''))
        except ValueError:
            return 0
    return 0

# Bucle para recorrer los IDs de 1 a 9,999,999
for player_id in range(0, 10000000):
    try:
        # Construir la URL para el jugador actual
        url = base_url.format(player_id)

        # Realizar la solicitud GET a la API
        response = requests.get(url)

        # Si la solicitud es exitosa
        if response.status_code == 200:
            data = response.json()

            # Extraer la fecha de actualización
            updated_at = datetime.strptime(data.get('updatedAt'), '%Y-%m-%dT%H:%M:%S.%f') if data.get('updatedAt') else None

            # Recorrer el historial de valores de mercado
            for entry in data.get('marketValueHistory', []):
                age = int(entry.get('age', 0))
                date = datetime.strptime(entry.get('date'), '%b %d, %Y').date() if entry.get('date') else None
                club_name = entry.get('clubName')
                club_id = int(entry.get('clubID', 0))
                value = parse_market_value(entry.get('value'))

                # Preparar la consulta de inserción
                insert_query = '''
                INSERT INTO market_value_history (
                    player_id, age, date, club_name, club_id, value, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''

                # Ejecutar la consulta de inserción
                cursor.execute(insert_query, (
                    player_id, age, date, club_name, club_id, value, updated_at
                ))
                connection.commit()

            print(f"Datos insertados exitosamente para el jugador con ID {player_id}")
        else:
            # Si no se encontró el jugador, agregar el ID a la lista de fallos
            failed_ids.append(player_id)
            print(f"Jugador con ID {player_id} no encontrado, guardado para revisión.")

    except psycopg2.Error as db_error:
        # Manejo del error relacionado con la base de datos
        print(f"Error con el jugador ID {player_id}: {db_error}")
        failed_ids.append(player_id)

        # Reabrir la conexión y continuar
        connection.rollback()  # Hacer rollback de la transacción actual
        cursor.close()
        connection.close()
        connection = connect_db()  # Reabrir la conexión
        cursor = connection.cursor()  # Reabrir el cursor

    except Exception as e:
        # Capturar cualquier otra excepción y guardar el ID en la lista de fallos
        failed_ids.append(player_id)
        print(f"Error con el jugador ID {player_id}: {e}")

# Cerrar la conexión a la base de datos
cursor.close()
connection.close()

# Mostrar los IDs que fallaron
print("IDs de jugadores no encontrados o que generaron errores:", failed_ids)
