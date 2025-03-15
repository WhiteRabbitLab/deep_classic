CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE composer_embeddings (
     id SERIAL PRIMARY KEY,
     composer_id INT UNIQUE,  -- No FK constraint
     embedding VECTOR(1536)   -- 1536-dimension OpenAI embeddings
);

CREATE TABLE work_embeddings (
     id SERIAL PRIMARY KEY,
     work_id INT UNIQUE,
     embedding VECTOR(1536)
);
