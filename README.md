# たとえ話＋イメージ図生成アプリ

このアプリは、ユーザーが入力したキーワードや内容に基づき、「たとえ話」と「イメージ図（画像）」を自動生成します。  
OpenAI APIを活用し、抽象的な概念をわかりやすくビジュアルと文章で表現します。

---

## 🚀 主な機能

- 入力キーワードに応じた「たとえ話」の自動生成
- OpenAIの画像生成APIによるイメージ図の出力
- シンプルで直感的なUI（HTMXベース）

---

## 🛠 使用技術

- Python 3.x
- Django
- HTMX
- OpenAI API
- Bootstrap（スタイル調整用）

---

## 🔧 セットアップ方法

1. リポジトリをクローンします：

```bash
git clone https://github.com/ntltss/MeteferOpenAI_API.git
cd your-repo-name

2.仮想環境を作成して、依存関係をインストールします：

python -m venv venv
source venv/bin/activate  # Windowsの方は venv\Scripts\activate
pip install -r requirements.txt

3. .env ファイルをプロジェクトルートに作成し、以下のように記述します：
# .env
OPENAI_API_KEY=your-api-key-here
※.envファイルは、プロジェクトフォルダ直下にご自身で作ってください。

4.開発サーバーを起動します：
python manage.py runserver