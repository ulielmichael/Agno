"""
🚀 WebDev Pro Agent - Server
שרת FastAPI עם ממשק צ'אט מובייל מלא
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import json
import os

app = FastAPI(title="WebDev Pro Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """אתה סוכן פיתוח אתרים ואפליקציות עסקיות מקצועי ומנוסה.

## יכולות הליב שלך:
- React, Vue, Next.js, Nuxt - קומפוננטים, pages, routing, state management
- HTML/CSS מתקדם - אנימציות, Flexbox, Grid, Responsive Design  
- Backend: Node.js, Python (FastAPI, Django), REST APIs, GraphQL
- Full Stack SaaS: Auth, DB (Postgres, Supabase), Stripe, deployment
- Landing Pages עסקיות: המרות, CRO, UX/UI מקצועי

## אופן העבודה שלך:
1. הבן את הדרישה העסקית לפני שאתה כותב קוד
2. הצע ארכיטקטורה ברורה לפני המימוש
3. כתוב קוד נקי, מתועד ומוכן לפרודקשן
4. הסבר את הקוד שאתה כותב בעברית

## כשאתה כותב קוד:
- הוסף תמיד TypeScript types כשרלוונטי
- הוסף error handling מלא
- כתוב קוד שמוכן לסקייל

תקשר בעברית. היה ישיר ומעשי. הצג אפשרויות כשיש יותר מגישה אחת."""


class ChatRequest(BaseModel):
    message: str
    history: list = []


@app.get("/", response_class=HTMLResponse)
async def get_chat_ui():
    return HTMLResponse(content=CHAT_HTML)


@app.post("/chat")
async def chat(req: ChatRequest):
    messages = []
    for msg in req.history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": req.message})

    def generate():
        with client.messages.stream(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/health")
async def health():
    return {"status": "ok", "agent": "WebDev Pro"}


# ─────────────────────────────────────────────
# ממשק הצ'אט - HTML מלא
# ─────────────────────────────────────────────

CHAT_HTML = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>WebDev Pro</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Hebrew:wght@300;400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/tokyo-night-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
  :root {
    --bg: #0a0a0f;
    --surface: #111118;
    --border: #1e1e2e;
    --accent: #7c6af7;
    --accent2: #4fc3f7;
    --text: #e2e2f0;
    --muted: #6b6b8a;
    --user-bg: #1a1a2e;
    --agent-bg: #111118;
    --radius: 16px;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Noto Sans Hebrew', sans-serif;
    background: var(--bg);
    color: var(--text);
    height: 100dvh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* Header */
  .header {
    padding: 14px 18px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 12px;
    flex-shrink: 0;
  }

  .logo {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
  }

  .header-text h1 {
    font-size: 15px;
    font-weight: 600;
    letter-spacing: -0.3px;
  }

  .header-text p {
    font-size: 11px;
    color: var(--muted);
    margin-top: 1px;
  }

  .status-dot {
    width: 8px; height: 8px;
    background: #4caf50;
    border-radius: 50%;
    margin-right: auto;
    box-shadow: 0 0 6px #4caf5088;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }

  /* Messages */
  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px 12px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    scroll-behavior: smooth;
  }

  .messages::-webkit-scrollbar { width: 4px; }
  .messages::-webkit-scrollbar-track { background: transparent; }
  .messages::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

  .message {
    display: flex;
    flex-direction: column;
    gap: 6px;
    animation: fadeUp 0.25s ease;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .message.user { align-items: flex-start; }
  .message.agent { align-items: flex-end; }

  .bubble {
    max-width: 88%;
    padding: 12px 15px;
    border-radius: var(--radius);
    font-size: 14px;
    line-height: 1.65;
    word-break: break-word;
  }

  .message.user .bubble {
    background: var(--user-bg);
    border: 1px solid var(--border);
    border-top-right-radius: 4px;
  }

  .message.agent .bubble {
    background: var(--agent-bg);
    border: 1px solid var(--border);
    border-top-left-radius: 4px;
    direction: rtl;
  }

  .sender {
    font-size: 10px;
    color: var(--muted);
    padding: 0 4px;
  }

  /* Markdown inside bubbles */
  .bubble pre {
    background: #0d0d14;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px;
    overflow-x: auto;
    margin: 10px 0;
    direction: ltr;
    text-align: left;
  }

  .bubble code:not(pre code) {
    background: #1a1a2e;
    padding: 2px 6px;
    border-radius: 5px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--accent2);
    direction: ltr;
    display: inline-block;
  }

  .bubble pre code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    line-height: 1.6;
  }

  .bubble strong { color: #fff; font-weight: 600; }
  .bubble em { color: var(--accent2); font-style: normal; }

  .bubble h1, .bubble h2, .bubble h3 {
    font-size: 14px;
    font-weight: 600;
    color: var(--accent);
    margin: 12px 0 6px;
  }

  .bubble ul, .bubble ol {
    padding-right: 18px;
    margin: 6px 0;
  }

  .bubble li { margin: 3px 0; font-size: 13.5px; }

  .bubble p { margin: 4px 0; }

  /* Copy button on code blocks */
  .code-wrapper { position: relative; margin: 10px 0; }
  .copy-btn {
    position: absolute;
    top: 8px; left: 8px;
    background: var(--border);
    border: none;
    color: var(--muted);
    font-size: 10px;
    padding: 3px 8px;
    border-radius: 6px;
    cursor: pointer;
    font-family: 'JetBrains Mono', monospace;
    transition: all 0.2s;
  }
  .copy-btn:hover { background: var(--accent); color: #fff; }

  /* Typing indicator */
  .typing {
    display: flex; gap: 5px; align-items: center;
    padding: 14px 16px;
    background: var(--agent-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    border-top-left-radius: 4px;
    width: fit-content;
    margin-right: auto;
  }

  .typing span {
    width: 7px; height: 7px;
    background: var(--accent);
    border-radius: 50%;
    animation: bounce 1.2s infinite;
  }
  .typing span:nth-child(2) { animation-delay: 0.2s; }
  .typing span:nth-child(3) { animation-delay: 0.4s; }

  @keyframes bounce {
    0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
    40% { transform: scale(1); opacity: 1; }
  }

  /* Quick suggestions */
  .suggestions {
    padding: 8px 12px;
    display: flex;
    gap: 8px;
    overflow-x: auto;
    flex-shrink: 0;
    border-top: 1px solid var(--border);
  }

  .suggestions::-webkit-scrollbar { display: none; }

  .suggestion {
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--muted);
    font-size: 11.5px;
    padding: 6px 12px;
    border-radius: 20px;
    white-space: nowrap;
    cursor: pointer;
    font-family: 'Noto Sans Hebrew', sans-serif;
    transition: all 0.2s;
    flex-shrink: 0;
  }

  .suggestion:hover, .suggestion:active {
    border-color: var(--accent);
    color: var(--accent);
    background: #7c6af710;
  }

  /* Input area */
  .input-area {
    padding: 12px;
    background: var(--surface);
    border-top: 1px solid var(--border);
    display: flex;
    gap: 10px;
    align-items: flex-end;
    flex-shrink: 0;
  }

  textarea {
    flex: 1;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    color: var(--text);
    font-family: 'Noto Sans Hebrew', sans-serif;
    font-size: 14px;
    padding: 12px 15px;
    resize: none;
    max-height: 120px;
    min-height: 46px;
    line-height: 1.5;
    outline: none;
    transition: border-color 0.2s;
    direction: rtl;
  }

  textarea:focus { border-color: var(--accent); }
  textarea::placeholder { color: var(--muted); }

  .send-btn {
    width: 46px; height: 46px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border: none;
    border-radius: 14px;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    transition: all 0.2s;
    font-size: 18px;
  }

  .send-btn:active { transform: scale(0.93); }
  .send-btn:disabled { opacity: 0.4; cursor: not-allowed; }

  /* Welcome */
  .welcome {
    text-align: center;
    padding: 40px 20px;
    color: var(--muted);
    animation: fadeUp 0.4s ease;
  }

  .welcome .icon { font-size: 48px; margin-bottom: 16px; }

  .welcome h2 {
    font-size: 20px;
    color: var(--text);
    margin-bottom: 8px;
    font-weight: 600;
  }

  .welcome p { font-size: 13px; line-height: 1.6; }
</style>
</head>
<body>

<div class="header">
  <div class="logo">⚡</div>
  <div class="header-text">
    <h1>WebDev Pro</h1>
    <p>סוכן פיתוח AI</p>
  </div>
  <div class="status-dot"></div>
</div>

<div class="messages" id="messages">
  <div class="welcome">
    <div class="icon">🚀</div>
    <h2>שלום! אני WebDev Pro</h2>
    <p>סוכן AI לפיתוח אתרים ואפליקציות עסקיות.<br>שאל אותי כל שאלה על קוד, ארכיטקטורה, או פרויקטים.</p>
  </div>
</div>

<div class="suggestions" id="suggestions">
  <button class="suggestion" onclick="useSuggestion(this)">בנה לנדינג פייג' עסקי</button>
  <button class="suggestion" onclick="useSuggestion(this)">קומפוננט React לטבלה</button>
  <button class="suggestion" onclick="useSuggestion(this)">API ב-FastAPI עם auth</button>
  <button class="suggestion" onclick="useSuggestion(this)">SaaS ארכיטקטורה</button>
  <button class="suggestion" onclick="useSuggestion(this)">Stripe Subscriptions</button>
</div>

<div class="input-area">
  <textarea
    id="input"
    placeholder="שאל על קוד, ארכיטקטורה, פרויקטים..."
    rows="1"
    onkeydown="handleKey(event)"
    oninput="autoResize(this)"
  ></textarea>
  <button class="send-btn" id="sendBtn" onclick="sendMessage()">➤</button>
</div>

<script>
  let history = [];
  let isLoading = false;

  function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 120) + 'px';
  }

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  function useSuggestion(btn) {
    document.getElementById('input').value = btn.textContent;
    document.getElementById('suggestions').style.display = 'none';
    sendMessage();
  }

  function scrollToBottom() {
    const msgs = document.getElementById('messages');
    msgs.scrollTop = msgs.scrollHeight;
  }

  function renderMarkdown(text) {
    // Code blocks
    text = text.replace(/```(\w*)\n?([\s\S]*?)```/g, (_, lang, code) => {
      const highlighted = lang && hljs.getLanguage(lang)
        ? hljs.highlight(code.trim(), { language: lang }).value
        : hljs.highlightAuto(code.trim()).value;
      return `<div class="code-wrapper">
        <button class="copy-btn" onclick="copyCode(this)">העתק</button>
        <pre><code class="hljs">${highlighted}</code></pre>
      </div>`;
    });

    // Inline code
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Headers
    text = text.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    text = text.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    text = text.replace(/^# (.+)$/gm, '<h1>$1</h1>');

    // Bold & italic
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Lists
    text = text.replace(/^- (.+)$/gm, '<li>$1</li>');
    text = text.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

    // Paragraphs
    text = text.replace(/\n\n/g, '</p><p>');
    text = '<p>' + text + '</p>';
    text = text.replace(/<p><\/p>/g, '');
    text = text.replace(/<p>(<[uh][l1-6])/g, '$1');
    text = text.replace(/(<\/[uh][l1-6]>)<\/p>/g, '$1');

    return text;
  }

  function copyCode(btn) {
    const code = btn.nextElementSibling.textContent;
    navigator.clipboard.writeText(code).then(() => {
      btn.textContent = '✓ הועתק';
      setTimeout(() => btn.textContent = 'העתק', 2000);
    });
  }

  function addMessage(role, content, stream = false) {
    const msgs = document.getElementById('messages');

    // Remove welcome on first message
    const welcome = msgs.querySelector('.welcome');
    if (welcome) welcome.remove();

    const div = document.createElement('div');
    div.className = `message ${role}`;

    const sender = document.createElement('div');
    sender.className = 'sender';
    sender.textContent = role === 'user' ? 'אתה' : 'WebDev Pro';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    div.appendChild(sender);
    div.appendChild(bubble);
    msgs.appendChild(div);
    scrollToBottom();

    return bubble;
  }

  function showTyping() {
    const msgs = document.getElementById('messages');
    const div = document.createElement('div');
    div.id = 'typing';
    div.className = 'message agent';
    div.innerHTML = `<div class="typing"><span></span><span></span><span></span></div>`;
    msgs.appendChild(div);
    scrollToBottom();
  }

  function hideTyping() {
    const t = document.getElementById('typing');
    if (t) t.remove();
  }

  async function sendMessage() {
    if (isLoading) return;
    const input = document.getElementById('input');
    const msg = input.value.trim();
    if (!msg) return;

    isLoading = true;
    document.getElementById('sendBtn').disabled = true;
    document.getElementById('suggestions').style.display = 'none';
    input.value = '';
    input.style.height = 'auto';

    addMessage('user', msg);
    history.push({ role: 'user', content: msg });

    showTyping();

    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg, history: history.slice(0, -1) })
      });

      hideTyping();
      const bubble = addMessage('agent', '');
      let fullText = '';

      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ') && line !== 'data: [DONE]') {
            try {
              const data = JSON.parse(line.slice(6));
              fullText += data.text;
              bubble.innerHTML = renderMarkdown(fullText);
              scrollToBottom();
            } catch {}
          }
        }
      }

      history.push({ role: 'assistant', content: fullText });

    } catch (err) {
      hideTyping();
      const bubble = addMessage('agent', '');
      bubble.textContent = 'שגיאה בחיבור לשרת. בדוק שהשרת פעיל.';
    }

    isLoading = false;
    document.getElementById('sendBtn').disabled = false;
    input.focus();
  }
</script>
</body>
</html>"""


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
