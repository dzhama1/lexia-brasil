import modal
from modal import Image, fastapi_endpoint
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

image = Image.debian_slim()

app = modal.App("lexia-frontend", image=image)

web_app = FastAPI()

@web_app.get("/")
async def home():
    html = """
    <html>
    <head><title>Lexia Brasil</title></head>
    <body style="font-family: Arial; max-width: 700px; margin: 50px auto; padding: 20px;">
        <h1>🇧🇷 Lexia Brasil</h1>
        <p><strong>ИИ-помощник по бразильским законам</strong></p>
        
        <input type="text" id="q" placeholder="Какой налог платит ИП?" style="width: 70%; padding: 10px;">
        <button onclick="ask()" style="padding: 10px 20px;">Спросить</button>
        
        <div id="answer" style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;"></div>
        
        <script>
            async function ask() {
                const q = document.getElementById('q').value;
                document.getElementById('answer').innerHTML = 'Думаю...';
                
                const res = await fetch('/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({question: q})
                });
                const data = await res.json();
                document.getElementById('answer').innerHTML = data.answer;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.function()
@fastapi_endpoint()
def main():
    return web_app