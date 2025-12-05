FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .
RUN pip3.10 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860 7861 7862

CMD [ "python3.10", "main.py" ]