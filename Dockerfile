# ベースイメージとしてPythonを使用
FROM python:3.13-slim

# 作業ディレクトリの作成
WORKDIR /app

# 依存関係のファイルをコピー
COPY requirements.txt .

# 必要なパッケージのインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# Streamlitのポートを開放
EXPOSE 8501

# アプリケーションの起動
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.host=0.0.0.0"]
