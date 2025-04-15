FROM ghcr.io/astral-sh/uv:latest

ENV PATH="/app/.venv/bin:$PATH"

ADD . /app

WORKDIR /app

COPY ./pyproject.toml /code/project.toml

RUN uv sync --frozen

CMD ["uv", "run", "fastapi", "app/main.py", "--port", "80"]
