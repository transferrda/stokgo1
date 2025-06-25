FROM python:3.13-slim

# Chromium ve driver'ı yükle
RUN apt-get update && \
    apt-get install -y chromium chromium-driver && \
    rm -rf /var/lib/apt/lists/*

# Uygulama dosyalarını kopyala
WORKDIR /app
COPY . /app

# Python bağımlılıklarını yükle
RUN pip install -r requirements.txt

# Chrome executable yolu
ENV CHROME_BIN=/usr/bin/chromium

# Uygulamayı başlat
CMD ["python3", "app.py"]
