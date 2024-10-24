# ベースイメージとしてPython 3.9のslimバージョンを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    && rm -rf /var/lib/apt/lists/*

# GitHubリポジトリからコードをクローン
RUN git clone https://github.com/ayuka-kitsuda/AI_Portfolio_Applications.git .

# Pythonの依存関係をインストール
COPY requirements.txt .
RUN pip3 install --default-timeout=100 -r requirements.txt

# ポート8501を公開
EXPOSE 8501

# コンテナのヘルスチェック
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# アプリケーションのエントリーポイント
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]