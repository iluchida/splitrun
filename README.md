# Gemini AI マーケティング診断フォーム

Flask × Gemini API によるマーケティング支援フォームアプリです。

## 📦 セットアップ手順

### 1. リポジトリをクローン
```bash
git clone https://your-repo-url.git
cd your-repo
```

### 2. `.env` を作成
```
GEMINI_API_KEY=your_google_api_key
FLASK_SECRET_KEY=your_flask_secret_key
```

### 3. Docker を使う場合
#### ビルド＆起動
```bash
docker-compose up --build
```

http://localhost:5000

### 4. Node.js + Sass (開発用ビルド)
```bash
npm install
npm run build:scss       # 1回だけビルド
npm run watch:scss       # SCSSファイルを監視して自動ビルド
```

### 5. Python venv 利用時（代替）
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## 📁 ディレクトリ構成
```
.
├── app.py                  # メインアプリ
├── templates/              # HTML テンプレート
├── static/css/style.css    # ビルド後のCSS
├── src/scss/style.scss     # 開発用SCSS
├── ngwords.csv             # NGワード設定
├── data/responses.csv      # 回答保存先
├── data/cache.json         # キャッシュデータ
├── Dockerfile
├── docker-compose.yml
├── package.json            # npmビルド定義
├── requirements.txt
└── README.md
```

## ✏️ 設問例（主題：マーケティング戦略）
- 自社サービスが顧客に支持される理由は何だと思いますか？
- 検証プロセスにおける最大のボトルネックは？
- デザイン思考をどのようにマーケティングに活かしていますか？
- 広告におけるクリエイティブ表現で意識していることは？
- 配信チャネルの選定基準は何ですか？

## ✅ 機能
- Gemini API によるAI回答
- 設問別 NGワードフィルタ（CSV管理）
- ローディング状態対応
- キャッシュ処理
- SCSS（Sass）でUI開発
- Docker / npm 対応

---

## 📌 注意点

- フォーム質問文と `ngwords.csv` の質問見出しは完全一致させてください
- `responses.csv` および `cache.json` はGit管理外推奨
- `style.css` は自動生成のため、手動編集しないでください

---

## 🧰 その他コマンド

```bash
# Python依存をファイル出力したい場合
pip freeze > requirements.txt
```

```bash
# .gitignore 例（最低限）
venv/
.env
__pycache__/
*.pyc
data/*.csv
data/*.json
static/css/style.css
```

## 仮想環境の停止
deactivate

## 仮想環境の再起動
source venv/bin/activate

## 仮想環境の削除
rm -rf venv
