

<!-- help me ccreate a better README.md -->

# ELEVA - Simple FastAPI Application
This is a simple FastAPI application that uses Beanie as an ODM for MongoDB.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

- [Docker](https://www.docker.com/) installed on your machine.
- [Poetry](https://python-poetry.org/) installed for managing Python dependencies.

### Project Structure
- **app** - contains FastAPI application code
- **app/api** - contains API routers and API specific code
- **app/api/v1/views** - contains API endpoints
- **app/api/v1/serializers** - contains pydantic models
- **app/api/v1/services** - contains business logic
- **app/core** - contains core application code
- **app/middleware** - contains middleware code
- **app/models** - contains beanie models
- **tests** - contain unit tests for the FastAPI application
- **docker-compose.dev.yml**: Docker Compose file for the development environment.
- **docker-compose.test.yml**: Docker Compose file for running tests.


## Setup and Usage

1. **Clone the repository**:

```bash
git clone https://github.com/YousefAldabbas/eleva-project.git
```

2. **Change directory to the project root directory**:

```bash
cd eleva-project
```


3. **Run the tests**:

```bash
docker-compose -f docker-compose.test.yml up --build
```

4. **Run the application**:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```