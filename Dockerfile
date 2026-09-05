FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
# Installe Flask + versions corrigées de setuptools/msgpack, et met à jour pip.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade "setuptools>=78.1.1" "msgpack>=1.2.1"

COPY app.py .

# Utilisateur non-root (corrige missing-user / DS-0002)
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
