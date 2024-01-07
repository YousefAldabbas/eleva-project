FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy pyproject.toml to the work directory
COPY pyproject.toml /app

# Install dependencies
RUN poetry install --no-dev

# Copy the rest of the application
COPY . /app

# Expose the port
EXPOSE 8000

# Command to run the FastAPI application using uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
