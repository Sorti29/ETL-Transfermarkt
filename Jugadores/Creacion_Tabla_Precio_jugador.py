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
CREATE TABLE IF NOT EXISTS market_value_history (
    id SERIAL PRIMARY KEY,
    player_id INT,
    age INT,
    date DATE,
    club_name TEXT,
    club_id INT,
    value NUMERIC,
    updated_at TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES player_profile(player_id)
);
'''

cursor.execute(create_table_query)
connection.commit()
print("Tabla player_profile creada exitosamente")

cursor.close()
connection.close()
