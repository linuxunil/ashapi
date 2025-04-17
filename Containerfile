FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /code

# Install the application dependencies.
WORKDIR /code
RUN uv sync --frozen --no-cache

# Run the application.
ENV PATH="/code/.venv/bin:$PATH"
EXPOSE 8000
ENTRYPOINT []
CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0" ]
