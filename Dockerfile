# syntax=docker/dockerfile:1
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=off PIP_DISABLE_PIP_VERSION_CHECK=on
WORKDIR /app
# Copy project (self-contained)
COPY pyproject.toml README.md /app/
COPY . /app/naver_searchad_mcp
RUN pip install --upgrade pip && pip install .
ENTRYPOINT ["naver-searchad-mcp"]
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import json,sys;from naver_searchad_mcp.fastmcp_server import health;print(json.dumps(health()))" || exit 1
