FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Change the working directory to the `app` directory
WORKDIR /app
 
# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# Copy the project into the intermediate image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

# Compile the messages
RUN uv run --locked pybabel compile -d locales -D messages --statistics

# Migrate
RUN uv run --locked alembic --name sqlite upgrade head

# Run the application
CMD sh -c "uv run --locked --module src"
