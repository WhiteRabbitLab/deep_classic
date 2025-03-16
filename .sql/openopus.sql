CREATE TABLE composer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(191) UNIQUE,
    complete_name VARCHAR(191),
    portrait VARCHAR(255),
    birth DATE NOT NULL,
    death DATE DEFAULT NULL,
    epoch VARCHAR(191) NOT NULL,
    country VARCHAR(191),
    recommended BOOLEAN DEFAULT FALSE,
    popular BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE work (
  id SERIAL PRIMARY KEY,
  composer_id INT NOT NULL,
  title VARCHAR(191),
  subtitle VARCHAR(512),
  searchterms VARCHAR(1024),
  genre VARCHAR(191) NOT NULL,
  year DATE DEFAULT NULL,
  recommended BOOLEAN NOT NULL DEFAULT FALSE,
  popular BOOLEAN NOT NULL DEFAULT FALSE,
  FOREIGN KEY (composer_id) REFERENCES composer(id) ON DELETE CASCADE
);

CREATE TABLE omnisearch (
    summary VARCHAR(3000) NOT NULL,
    composer_id INT NOT NULL,
    work_id INT DEFAULT NULL,
    FOREIGN KEY (composer_id) REFERENCES composer(id) ON DELETE CASCADE,
    FOREIGN KEY (work_id) REFERENCES work(id) ON DELETE SET NULL
);

CREATE TABLE performer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(255) NOT NULL
);

-- Adding indexes
CREATE INDEX idx_composer_complete_name ON composer(complete_name);
CREATE INDEX idx_composer_birth ON composer(birth);
CREATE INDEX idx_composer_death ON composer(death);
CREATE INDEX idx_composer_epoch ON composer(epoch);
CREATE INDEX idx_composer_country ON composer(country);
CREATE INDEX idx_composer_recommended ON composer(recommended);
CREATE INDEX idx_composer_popular ON composer(popular);

CREATE INDEX idx_performer_role ON performer(role);

CREATE INDEX idx_work_composer_id ON work(composer_id);
CREATE INDEX idx_work_title ON work(title);
CREATE INDEX idx_work_genre ON work(genre);
CREATE INDEX idx_work_year ON work(year);
CREATE INDEX idx_work_recommended ON work(recommended);
CREATE INDEX idx_work_popular ON work(popular);

-- Full-text search indices
CREATE INDEX idx_composer_fulltext ON composer USING gin(to_tsvector('simple', name || ' ' || complete_name));
CREATE INDEX idx_omnisearch_summary ON omnisearch USING gin(to_tsvector('simple', summary));
CREATE INDEX idx_work_titlesearch ON work USING gin(to_tsvector('simple', title || ' ' || subtitle));

ALTER TABLE composer ADD CONSTRAINT unique_composer_name UNIQUE (name);
ALTER TABLE work ADD CONSTRAINT unique_work_title UNIQUE (title);
ALTER TABLE composer ADD COLUMN source_id INT UNIQUE;

