# 🚀 מדריך פרסום - Railway (חינם)

---

## שלב 1 — העלה את הקבצים ל-GitHub

1. כנס ל-github.com → **New repository**
2. שם: `webdev-agent`
3. לחץ **Create repository**
4. העלה את 3 הקבצים:
   - `server.py`
   - `requirements.txt`
   - `Procfile`

---

## שלב 2 — פרסם ב-Railway

1. כנס ל-**railway.app** (הרשמה חינם עם GitHub)
2. לחץ **New Project → Deploy from GitHub repo**
3. בחר את `webdev-agent`
4. Railway יזהה אוטומטית את ה-Procfile ויבנה הכל ✅

---

## שלב 3 — הוסף את ה-API Key

ב-Railway, לך ל:
**Settings → Variables → Add Variable**

```
ANTHROPIC_API_KEY = sk-ant-xxxxx...
```

> קבל מפתח בחינם: https://console.anthropic.com

---

## שלב 4 — קבל קישור וכנס מהטלפון

1. ב-Railway לך ל: **Settings → Networking → Generate Domain**
2. תקבל קישור כמו: `https://webdev-agent-xxx.up.railway.app`
3. **פתח את הקישור הזה מהטלפון** — זה הצ'אט שלך! 🎉

---

## חלופה — Render (גם חינם)

1. כנס ל-**render.com**
2. **New → Web Service → Connect GitHub**
3. בחר את הריפו
4. הגדר:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT`
5. הוסף את `ANTHROPIC_API_KEY` ב-Environment Variables
6. לחץ **Create Web Service**

---

## בדיקה מקומית (אופציונלי)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
python server.py
# פתח: http://localhost:8000
```
