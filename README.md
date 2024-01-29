# EventHub

## Installation

### Clone the repository:

```shell
git clone git@gitlab.com:noors312/eventhub.git
```
or
```shell
git clone https://gitlab.com/noors312/eventhub.git
```

### Copy env file
```shell
cp .env.template .env
```

### Install dependencies
```shell
poetry install
```
If you don't have poetry installed, please read the [Documentation](https://python-poetry.org/docs/#installation)

### Configure services

Run the project

```shell
docker-compose up --build -d
```
