import requests
import psycopg2
from datetime import datetime

# Base URL de la API
base_url = "https://transfermarkt-api.fly.dev/players/{}/profile"

# Conectar a la base de datos
connection = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="9893",
    database="postgres"
)
cursor = connection.cursor()

# Lista para almacenar los IDs que fallan
failed_ids = []

# Bucle para recorrer los IDs de 1 a 9,999,999
for player_id in range(31805, 10000000):
    try:
        # Construir la URL para el jugador actual
        url = base_url.format(player_id)

        # Realizar la solicitud GET a la API
        response = requests.get(url)

        # Si la solicitud es exitosa
        if response.status_code == 200:
            data = response.json()

            # Extraer y mapear los datos
            name = data.get('name')
            description = data.get('description')
            date_of_birth = datetime.strptime(data.get('dateOfBirth'), '%b %d, %Y').date() if data.get(
                'dateOfBirth') else None
            place_of_birth_city = data.get('placeOfBirth', {}).get('city')
            place_of_birth_country = data.get('placeOfBirth', {}).get('country')

            # Intentar obtener la edad del JSON, si falla, calcularla manualmente
            try:
                age = int(data.get('age'))
            except (TypeError, ValueError):
                if date_of_birth:
                    today = datetime.today().date()
                    age = today.year - date_of_birth.year - (
                                (today.month, today.day) < (date_of_birth.month, date_of_birth.day))
                else:
                    age = None  # O un valor por defecto si no hay fecha de nacimiento disponible

            citizenship = data.get('citizenship', [None])[0]  # Solo se guarda la primera ciudadanía
            is_retired = data.get('isRetired')
            retired_since = datetime.strptime(data.get('retiredSince'), '%b %d, %Y').date() if data.get(
                'retiredSince') else None
            position_main = data.get('position', {}).get('main')
            position_other = ', '.join(data.get('position', {}).get('other', []))  # Convertir lista en texto
            club_name = data.get('club', {}).get('name')
            most_games_for = data.get('club', {}).get('mostGamesFor')

            # Preparar la consulta de inserción
            insert_query = '''
            INSERT INTO player_profile (
                player_id, name, description, date_of_birth,
                place_of_birth_city, place_of_birth_country, age, citizenship,
                is_retired, retired_since, position_main, position_other,
                club_name, most_games_for
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (player_id) DO NOTHING;
            '''

            # Ejecutar la consulta de inserción
            cursor.execute(insert_query, (
                player_id, name, description, date_of_birth,
                place_of_birth_city, place_of_birth_country, age, citizenship,
                is_retired, retired_since, position_main, position_other,
                club_name, most_games_for
            ))
            connection.commit()

            print(f"Datos insertados exitosamente para el jugador con ID {player_id}")
        else:
            # Si no se encontró el jugador, agregar el ID a la lista de fallos
            failed_ids.append(player_id)
            print(f"Jugador con ID {player_id} no encontrado, guardado para revisión.")

    except Exception as e:
        # Capturar cualquier otra excepción y guardar el ID en la lista de fallos
        failed_ids.append(player_id)
        print(f"Error con el jugador ID {player_id}: {e}")

# Cerrar la conexión a la base de datos
cursor.close()
connection.close()

# Mostrar los IDs que fallaron
print("IDs de jugadores no encontrados o que generaron errores:", failed_ids)
