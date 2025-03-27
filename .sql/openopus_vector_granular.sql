CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE composer (
  id SERIAL PRIMARY KEY,
  composer_id INT UNIQUE,
  source_id INT UNIQUE,
  name VECTOR(1536),
  complete_name VECTOR(1536),
  portrait VARCHAR(255),
  birth VECTOR(1536),
  death VECTOR(1536),
  epoch VECTOR(1536),
  country VECTOR(1536),
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
  year VECTOR(1536),
  recommended BOOLEAN NOT NULL DEFAULT FALSE,
  popular BOOLEAN NOT NULL DEFAULT FALSE,
  FOREIGN KEY (composer_id) REFERENCES composer(id) ON DELETE CASCADE
);