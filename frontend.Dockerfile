FROM python:3.12-slim

WORKDIR /app

COPY ./frontend/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

COPY ./frontend/ /app

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]