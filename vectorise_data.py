import openai
import psycopg2
import numpy as np

# OpenAI API Key
openai.api_key = "xxx"

MAIN_DB_PARAMS = {
    "dbname": "maindb",
    "user": "mainuser",
    "password": "mainpassword",
    "host": "localhost",
    "port": "5432",
}

VECTOR_DB_PARAMS = {
    "dbname": "vectordb",
    "user": "vectoruser",
    "password": "vectorpassword",
    "host": "localhost",
    "port": "5433",
}

# Generate embeddings using OpenAI
def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]

# Fetch composers that do not have embeddings yet
def fetch_missing_composers(flat_conn, vector_conn):
    with flat_conn.cursor() as flat_cur, vector_conn.cursor() as vector_cur:
        flat_cur.execute("SELECT id, name, complete_name, epoch, country FROM composer")
        all_composers = flat_cur.fetchall()

        print(vector_cur.fetchall())  # Should include 'composer_embeddings'
        vector_cur.execute("SELECT composer_id FROM composer_embeddings")
        existing_composers = {row[0] for row in vector_cur.fetchall()}  # Set of existing composer IDs

        return [c for c in all_composers if c[0] not in existing_composers]

# Fetch works that do not have embeddings yet
def fetch_missing_works(flat_conn, vector_conn):
    with flat_conn.cursor() as flat_cur, vector_conn.cursor() as vector_cur:
        flat_cur.execute("SELECT id, title, subtitle, genre FROM work")
        all_works = flat_cur.fetchall()

        vector_cur.execute("SELECT work_id FROM work_embeddings")
        existing_works = {row[0] for row in vector_cur.fetchall()}  # Set of existing work IDs

        return [w for w in all_works if w[0] not in existing_works]

# Insert embeddings into the vector database
def insert_embeddings(table, column, data, vector_conn):
    with vector_conn.cursor() as cur:
        sql = f"INSERT INTO {table} ({column}, embedding) VALUES (%s, %s)"
        for row in data:
            entity_id, *text_fields = row
            text = " ".join(filter(None, text_fields))  # Join non-null text fields
            embedding = get_embedding(text)
            cur.execute(sql, (entity_id, np.array(embedding).tolist()))
        vector_conn.commit()

def main():
    main_conn = psycopg2.connect(**MAIN_DB_PARAMS)
    vector_conn = psycopg2.connect(**VECTOR_DB_PARAMS)

    try:
        # Process Composer Data
        missing_composers = fetch_missing_composers(main_conn, vector_conn)
        if missing_composers:
            insert_embeddings("composer_embeddings", "composer_id", missing_composers, vector_conn)
            print(f"Inserted {len(missing_composers)} new composer embeddings.")
        else:
            print("No new composers to process.")

        # Process Work Data
        missing_works = fetch_missing_works(main_conn, vector_conn)
        if missing_works:
            insert_embeddings("work_embeddings", "work_id", missing_works, vector_conn)
            print(f"Inserted {len(missing_works)} new work embeddings.")
        else:
            print("No new works to process.")

    finally:
        main_conn.close()
        vector_conn.close()

if __name__ == "__main__":
    main()
