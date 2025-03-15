# Open Classic
## Arijit Mitra and Luke Neal 

### Matching software for classical works and repertoire

A vector database of classical music works
for the purposes of classical music repertoire matching.

This repository uses two local PostgreSQL databases;
one to store works in a relational database,
the other to vectorise the data for use in large-langauge models.

## Matching software for classical works and repertoire

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
git clone ***
```

- Initialise the dual databases

```
docker-compose up -d
```

- Populate the local OpenOpus database

```
python -m fecth_data.py
```

- Manual ETL for vectorising the data

```
python -m vectorise_data.py
```

