import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="9893",
    database="postgres"
)

cursor = connection.cursor()

# Crear la tabla player_profile
create_table_query = '''
CREATE TABLE IF NOT EXISTS player_profile (
    id SERIAL PRIMARY KEY,
    player_id INT UNIQUE,
    name TEXT,
    description TEXT,
    date_of_birth DATE,
    place_of_birth_city TEXT,
    place_of_birth_country TEXT,
    age INT,
    citizenship TEXT,
    is_retired BOOLEAN,
    retired_since DATE,
    position_main TEXT,
    position_other TEXT,
    club_name TEXT,
    most_games_for TEXT
);
'''

cursor.execute(create_table_query)
connection.commit()
print("Tabla player_profile creada exitosamente")

cursor.close()
connection.close()
