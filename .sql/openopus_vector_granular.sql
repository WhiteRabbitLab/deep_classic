CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE composer (
  id SERIAL PRIMARY KEY,
  source_id INT UNIQUE,
  name VECTOR(1536),
  complete_name VECTOR(1536),
  portrait VARCHAR(255),
  birth DATE NOT NULL,
  death DATE DEFAULT NULL,
  epoch VECTOR(1536),
  recommended BOOLEAN DEFAULT FALSE,
  popular BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE work (
  id SERIAL PRIMARY KEY,
  work_id INT UNIQUE,
  composer_id INT NOT NULL,
  title VECTOR(1536),
  subtitle VECTOR(1536),
  searchterms VECTOR(1536),
  genre VECTOR(1536),
  year DATE DEFAULT NULL,
  recommended BOOLEAN NOT NULL DEFAULT FALSE,
  popular BOOLEAN NOT NULL DEFAULT FALSE,
  FOREIGN KEY (composer_id) REFERENCES composer(id) ON DELETE CASCADE
);