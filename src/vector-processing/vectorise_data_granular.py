import openai
import psycopg2
import numpy as np

# OpenAI API Key
openai.api_key = "xxx"

# Database connection parameters
MAIN_DB_PARAMS = {
    "dbname": "maindb",
    "user": "mainuser",
    "password": "mainpassword",
    "host": "localhost",
    "port": "5432",
}

VECTOR_DB_PARAMS = {
    "dbname": "vectorgranulardb",
    "user": "vectoruser",
    "password": "vectorpassword",
    "host": "localhost",
    "port": "5434",
}

# Generate embeddings using OpenAI
def get_embedding(text):
    if not text or text.strip() == "":
        return [0.0] * 1536  # Return zero-vector for empty fields
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# Fetch composers missing embeddings
def fetch_missing_composers(main_conn, vector_conn):
    with main_conn.cursor() as main_cur, vector_conn.cursor() as vector_cur:
        main_cur.execute("SELECT id, source_id, name, complete_name, "
                         "portrait, birth, death, epoch, "
                         "recommended, popular FROM composer")
        all_composers = main_cur.fetchall()

        vector_cur.execute("SELECT composer_id FROM composer")
        existing_composers = {row[0] for row in vector_cur.fetchall()}

        return [c for c in all_composers if c[0] not in existing_composers]

# Fetch works missing embeddings
def fetch_missing_works(main_conn, vector_conn):
    with main_conn.cursor() as main_cur, vector_conn.cursor() as vector_cur:
        main_cur.execute("SELECT id, composer_id, title, subtitle, "
                         "searchterms, genre, year, recommended, popular FROM work")
        all_works = main_cur.fetchall()

        vector_cur.execute("SELECT work_id FROM work")
        existing_works = {row[0] for row in vector_cur.fetchall()}

        return [w for w in all_works if w[0] not in existing_works]

# Insert composer embeddings into vector database
def insert_composer_embeddings(data, vector_conn):
    with vector_conn.cursor() as cur:
        sql = """
            INSERT INTO composer 
            (source_id, name, complete_name, portrait, birth, death, epoch, recommended, popular)
            VALUES (%i, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for row in data:
            id, source_id, name, completename, portrait, birth, death, epoch, recommended, popular = row
            cur.execute(sql, (
                source_id,
                np.array(get_embedding(name)).tolist(),
                np.array(get_embedding(completename)).tolist(),
                np.array(portrait),
                birth,
                death,
                np.array(get_embedding(epoch)).tolist(),
                recommended,
                popular
            ))
        vector_conn.commit()

# Insert work embeddings into vector database
def insert_work_embeddings(data, vector_conn):
    with vector_conn.cursor() as cur:
        sql = """
            INSERT INTO work 
            (composer_id, title, subtitle, searchterms, genre, year, recommended, popular)
            VALUES (%i, %s, %s, %s, %s, %s, %s, %s)
        """
        for row in data:
            composer_id, title, subtitle, searchterms, genre, year, recommended, popular = row
            cur.execute(sql, (
                composer_id,
                np.array(get_embedding(title)).tolist(),
                np.array(get_embedding(subtitle)).tolist(),
                np.array(get_embedding(searchterms)).tolist(),
                np.array(get_embedding(genre)).tolist(),
                year,
                recommended,
                popular
            ))
        vector_conn.commit()

def main():
    main_conn = psycopg2.connect(**MAIN_DB_PARAMS)
    vector_conn = psycopg2.connect(**VECTOR_DB_PARAMS)

    try:
        # Process Composer Data
        missing_composers = fetch_missing_composers(main_conn, vector_conn)
        if missing_composers:
            insert_composer_embeddings(missing_composers, vector_conn)
            print(f"Inserted {len(missing_composers)} new composer embeddings.")
        else:
            print("No new composers to process.")

        # Process Work Data
        missing_works = fetch_missing_works(main_conn, vector_conn)
        if missing_works:
            insert_work_embeddings(missing_works, vector_conn)
            print(f"Inserted {len(missing_works)} new work embeddings.")
        else:
            print("No new works to process.")

    finally:
        main_conn.close()
        vector_conn.close()

if __name__ == "__main__":
    main()
