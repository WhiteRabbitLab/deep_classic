import requests
import psycopg2
from psycopg2.extras import execute_values

# Database connection parameters
DB_PARAMS = {
    "dbname": "maindb",
    "user": "mainuser",
    "password": "mainpassword",
    "host": "localhost",
    "port": "5432",
}

# OpenOpus API URLs (only for POPULAR composers - not full data set
COMPOSER_URL = "https://api.openopus.org/composer/list/pop.json"
WORKS_URL_TEMPLATE = "https://api.openopus.org/work/list/composer/{composer_id}/genre/all.json"

# Connect to PostgreSQL
def connect_db():
    return psycopg2.connect(**DB_PARAMS)

# Fetch data from OpenOpus API
def fetch_data(url):
    response = requests.get(url)
    print(f"Fetching: {url}")  # Debugging output
    print(f"Response Status: {response.status_code}")  # Check API status
    if response.status_code == 200:
        data = response.json()
        print("Response Data:", data)  # Print the full response
        return data
    print("Failed to fetch data")

# Insert composers into the database
def insert_composers(composers, conn):
    with conn.cursor() as cur:
        sql = """
        INSERT INTO composer (source_id, name, complete_name, birth, death, epoch, recommended, popular)
        VALUES %s
        ON CONFLICT (source_id) DO UPDATE SET
            name = EXCLUDED.name,
            complete_name = EXCLUDED.complete_name,
            portrait = EXCLUDED.portrait,
            birth = EXCLUDED.birth,
            death = EXCLUDED.death,
            epoch = EXCLUDED.epoch,
            recommended = EXCLUDED.recommended,
            popular = EXCLUDED.popular
        RETURNING id, source_id;
        """
        values = [
            (
                c["id"],  # OpenOpus ID as source_id
                c["name"], c["complete_name"], c["birth"], c["death"],
                c["epoch"], True, False
            )
            for c in composers
        ]
        execute_values(cur, sql, values)
        conn.commit()

# Insert works into the database
def insert_works(works, composer_id, conn):
    with conn.cursor() as cur:
        sql = """
        INSERT INTO work (composer_id, title, genre, year, recommended, popular)
        VALUES %s
        ON CONFLICT (title) DO NOTHING;
        """
        values = [
            (
                composer_id, w["title"], w.get("genre", "Unknown"),
                w.get("year", None), True, False
            )
            for w in works
        ]
        execute_values(cur, sql, values)
        conn.commit()

def get_pg_composer_id(openopus_id, conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM composer WHERE source_id = %s", (openopus_id,))
        result = cur.fetchone()
        return result[0] if result else None  # Return PostgreSQL ID

# Main function to fetch and store data
def main():
    conn = connect_db()
    try:
        # Fetch composers
        composers_data = fetch_data(COMPOSER_URL)
        if composers_data:
            composers = composers_data["composers"]
            insert_composers(composers, conn)
            print(f"Inserted {len(composers)} composers.")

            # Fetch and insert works for each composer
            for composer in composers:
                openopus_id = composer["id"]
                print(f"Open Opus ID for Composer: {openopus_id}.")
                postgres_composer_id = get_pg_composer_id(openopus_id, conn)
                print(f"Internal ID for Composer: {postgres_composer_id}.")

                # if not postgres_composer_id:
                #     print(f"Skipping works for composer {composer['name']} (ID {openopus_id}) - not found in DB.")
                # continue  # Skip if composer wasn't inserted

                print(f"Getting Works for composer with internal ID: {postgres_composer_id}.")
                works_data = fetch_data(WORKS_URL_TEMPLATE.format(composer_id=openopus_id))
                if works_data and "works" in works_data:
                    insert_works(works_data["works"], postgres_composer_id, conn)
                    print(f"Inserted {len(works_data['works'])} works for composer {composer['name']}.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
