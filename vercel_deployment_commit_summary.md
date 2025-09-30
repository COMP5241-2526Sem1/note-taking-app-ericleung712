# Vercel Deployment Change Summary

## 1. 主要修改內容

### 後端 (main.py, .env, requirements.txt)

#### 主要程式片段與演進說明

**1. 資料庫改為 PostgreSQL（Supabase）**
```python
from dotenv import load_dotenv
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
```
**原因：** SQLite 不適合雲端，改用 Supabase PostgreSQL，連線字串由 .env 取得。

**2. .env 新增資料庫連線字串**
```properties
DATABASE_URL=postgresql://postgres:[Eric1234!!]@db.aqjrcaezkwtcvtpzyawc.supabase.co:5432/postgres
```
**原因：** 讓程式可安全取得雲端資料庫連線資訊。

**3. requirements.txt 新增必要套件**
```text
python-dotenv
psycopg2-binary
```
**原因：** 支援 .env 讀取與 PostgreSQL 連線。

**4. 移除 SQLite 相關路徑與本地檔案依賴**
```python
# 刪除 DB_PATH, os.makedirs 等本地檔案相關程式
```
**原因：** Vercel 不支援本地檔案持久化，所有資料需存雲端。

### Vercel 設定

**1. 新增環境變數**
- 在 Vercel 專案設定新增 `DATABASE_URL`、`supabaseURL`、`supabaseKey`。

**2. 部署流程**
- 連結 GitHub Repo，Vercel 自動偵測 Python 專案。
- 若偵測失敗，可手動選擇 Python 或 Other。
- 部署後測試 API 是否正常。

## 2. 步驟與說明
1. **程式碼修改**：將 SQLite 改為 PostgreSQL，並用 .env 管理連線字串。
2. **安裝依賴**：requirements.txt 加入必要套件。
3. **Vercel 設定**：新增環境變數，確認入口檔案。
4. **部署測試**：確認 API 可正常連線雲端資料庫。

## 3. 影響檔案
- `.env`
- `src/main.py`
- `requirements.txt`

---

此 commit 讓專案可安全部署於 Vercel，資料存於雲端 PostgreSQL，符合雲端環境需求。
每段程式碼均有演進原因，方便日後維護與擴充。
