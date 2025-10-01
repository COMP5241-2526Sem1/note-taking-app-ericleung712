import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.note import note_bp
from src.models.note import Note
from dotenv import load_dotenv

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(note_bp, url_prefix='/api')
# configure database to use repository-root `database/app.db`
ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(ROOT_DIR, 'database', 'app.db')
# ensure database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

load_dotenv()
POSTGRES_URL = os.getenv("supabaseURL")
POSTGRES_KEY = os.getenv("supabaseKey")
# Supabase 連線字串格式通常為：postgresql://user:password@host:port/dbname
# 你可在 Supabase 專案設定中取得完整連線字串
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/src/')
def home():
    return 'Hello from Vercel!'

# 需加下列程式讓 Vercel 正確啟動
def handler(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    # 檢查 Note.order 欄位是否存在，若不存在則新增（SQLite only）
    with app.app_context():
        from sqlalchemy import inspect, text
        conn = db.engine.connect()
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('note')]
        if 'order' not in columns:
            conn.execute(text('ALTER TABLE note ADD COLUMN "order" INTEGER DEFAULT 0'))
        conn.close()
    app.run(host='0.0.0.0', port=5001, debug=True)
