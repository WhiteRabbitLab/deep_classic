# Deep Classic
## Arijit Mitra and Luke Neal 

### Matching software for classical works and repertoire

A vector database of classical music works
for the purposes of classical music repertoire matching.

This repository uses two local PostgreSQL databases;
one to store works in a relational database,
the other to vectorise the data for use in large-langauge models.

## Prerequisites

A UNIX-based system, with Docker and Python installed.

### To install on MacOS:

Install brew

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"```
```

Install git

```
brew install git
```

Install Docker

```
brew install docker
```

Install Python

```
brew install python
```

### How to run

- Clone the repository

```
git clone https://github.com/WhiteRabbitLab/open_classic.git
```

- Initialise the dual databases

```
docker-compose up -d
```

- Populate the local OpenOpus database

```
python ./src/pre-processing/fetch_data.py
```

- Manual ETL for vectorising the data and populating the vector database

```
python ./src/vector-processing/vectorise_data.py
```

### Useful commands

- Clean down the vector database volume

```
docker volume rm deep_classic_postgres_vector_data
```


Write script to create database with all fields vectorised 

vector db for query