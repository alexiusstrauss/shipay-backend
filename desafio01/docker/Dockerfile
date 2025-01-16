FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Atualize o pip e instale o `uv`
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir uv

# Crie o usuário `app` e configure o ambiente
RUN useradd -m app

# Configure o diretório de trabalho
USER app
WORKDIR /home/app/api

# Copie os arquivos do projeto para o container
COPY --chown=app:app . .

# Sincronize o ambiente usando o `uv`
RUN uv sync

# Adicione o caminho do ambiente gerenciado pelo `uv` ao PATH
ENV PATH="/home/app/.local/bin:$PATH"

# Exponha a porta 8000
EXPOSE 8000

# Defina o comando para iniciar o servidor
CMD ["uv", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]