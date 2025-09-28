# Translation Function Commit Summary

## 1. 主要修改內容

### 前端 (index.html)
- 新增「翻譯」按鈕與語言選擇下拉選單，讓使用者可選擇目標語言並翻譯內容。
- 新增「還原」按鈕，翻譯後可還原為原始內容（僅限尚未儲存）。
- 修改 `translateNote()`，改為直接翻譯編輯區內容（支援新建筆記），並暫存原始內容。
- 新增 `revertContent()`，還原翻譯前內容。
- 在切換/新建筆記時重設暫存。

#### 主要程式片段
```javascript
async translateNote() {
    const content = document.getElementById('noteContent').value.trim();
    // ...
    if (this.originalContent === null) {
        this.originalContent = content;
    }
    // ...呼叫 /api/translate 並更新 noteContent...
}

revertContent() {
    if (this.originalContent !== null) {
        document.getElementById('noteContent').value = this.originalContent;
        this.originalContent = null;
    }
}
```

### 後端 (routes/note.py)
- 新增 `/api/translate` API，接收 content 與 target_lang，回傳翻譯結果，不影響資料庫。
- API 範例：
```python
@note_bp.route('/translate', methods=['POST'])
def translate_content():
    from src.llm import translate
    data = request.json
    content = data.get('content')
    target_lang = data.get('target_lang')
    if not content or not target_lang:
        return jsonify({'error': 'content and target_lang required'}), 400
    try:
        translated = translate(content, target_lang)
        return jsonify({'translated_content': translated}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### llm.py
- 確認 `translate(text, target_language)` 函式可正確呼叫 LLM 並回傳翻譯內容。

## 2. 步驟與說明
1. **設計前端 UI**：在編輯器區塊新增語言選擇與翻譯、還原按鈕。
2. **前端暫存原始內容**：翻譯前將內容暫存，翻譯後可還原。
3. **API 設計**：新增 `/api/translate`，支援翻譯任意內容，不需 note_id。
4. **串接 LLM**：後端呼叫 llm.py 的 translate 函式。
5. **確保資料安全**：只有儲存或自動儲存才會寫入資料庫，翻譯/還原不影響 DB。

## 3. 影響檔案
- `src/static/index.html`
- `src/routes/note.py`
- `src/llm.py`

---

此 commit 讓使用者可在編輯或新建筆記時即時翻譯內容，並可隨時還原，提升多語言筆記體驗且不影響資料安全。