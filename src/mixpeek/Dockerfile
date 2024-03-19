# Use an official Python runtime as a parent image
FROM python:3.10

# Install Poetry
RUN pip install --no-cache-dir poetry

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only pyproject.toml and poetry.lock (if available) to cache dependencies installation
COPY pyproject.toml poetry.lock* /usr/src/app/

# Install dependencies from pyproject.toml using Poetry
# Note: The `--no-root` option is used to prevent Poetry from installing the project package at this stage.
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Make port 8003 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches using Poetry
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]