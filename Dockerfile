FROM python:3.12-slim

# 作業ディレクトリ
WORKDIR /app

# 必要パッケージをインストール（nodeとnpmを含む）
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Pythonパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Node.jsパッケージをインストール（postcss-cli含める）
COPY package.json package-lock.json* ./
RUN npm install

# アプリケーションコードをコピー
COPY . .

# SCSSビルド（npm script で postcss を実行）
RUN npm run build:scss

# Flask起動
CMD ["python", "app.py"]
