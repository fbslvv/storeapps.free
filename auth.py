from flask import Flask, redirect, request, render_template_string
import requests

app = Flask(__name__)
app.secret_key = "storeapps_secret_key"

# CONFIGURAÇÕES DO DISCORD
DISCORD_CLIENT_ID = "1435836194456862770"
DISCORD_CLIENT_SECRET = "dz-yYXWFbm8Rb6bizEekYLgvAb6Jj2EC"
DISCORD_REDIRECT_URI = "http://localhost:5000/callback"
DISCORD_API_BASE_URL = "https://discord.com/api"
OAUTH_SCOPE = "identify email guilds bot applications.commands"

# SERVIDOR DE SUPORTE (Store Apps)
SUPPORT_SERVER = "https://discord.gg/wxzXrUPHJe"

@app.route('/')
def home():
    return redirect("/login")

@app.route('/login')
def login():
    # Redireciona o usuário para o login do Discord
    auth_url = (
        f"{DISCORD_API_BASE_URL}/oauth2/authorize?"
        f"client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={DISCORD_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={OAUTH_SCOPE}"
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get("code")
    if not code:
        return "Erro: nenhum código recebido.", 400

    # Troca o "code" por token de acesso
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
        "scope": OAUTH_SCOPE,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(f"{DISCORD_API_BASE_URL}/oauth2/token", data=data, headers=headers)

    if r.status_code != 200:
        return f"Erro ao obter token: {r.text}", 400

    token_info = r.json()
    access_token = token_info["access_token"]

    # Pega informações do usuário
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info = requests.get(f"{DISCORD_API_BASE_URL}/users/@me", headers=headers).json()

    username = user_info.get("username", "Usuário")

    # Tela final com agradecimento e botão de suporte
    return render_template_string(f"""
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Store Apps Free - Obrigado</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: "Poppins", sans-serif;
            }}

            body {{
                height: 100vh;
                background: url('foto.png') no-repeat center center/cover;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                overflow: hidden;
            }}

            .overlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.6);
                z-index: 0;
            }}

            .container {{
                position: relative;
                z-index: 1;
                background: rgba(10, 15, 40, 0.75);
                border: 1px solid rgba(0, 162, 255, 0.3);
                border-radius: 20px;
                box-shadow: 0 0 30px rgba(0, 162, 255, 0.4);
                padding: 50px 60px;
                text-align: center;
                max-width: 500px;
                backdrop-filter: blur(10px);
            }}

            h1 {{
                font-size: 2rem;
                color: #00a2ff;
                margin-bottom: 10px;
                text-shadow: 0 0 20px rgba(0,162,255,0.7);
            }}

            p {{
                font-size: 1.1rem;
                color: #ccc;
                margin-bottom: 30px;
                line-height: 1.6;
            }}

            a.btn {{
                display: inline-block;
                text-decoration: none;
                color: white;
                padding: 15px 35px;
                border-radius: 12px;
                font-weight: 600;
                margin: 10px;
                transition: 0.3s;
                background: #00a2ff;
                box-shadow: 0 0 20px rgba(0,162,255,0.6);
            }}

            a.btn:hover {{
                background: #0090e6;
                transform: scale(1.05);
                box-shadow: 0 0 40px rgba(0,162,255,0.9);
            }}

            footer {{
                position: absolute;
                bottom: 20px;
                width: 100%;
                text-align: center;
                color: #aaa;
                font-size: 0.9rem;
            }}

            footer a {{
                color: #00a2ff;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="overlay"></div>
        <div class="container">
            <h1>🎉 Obrigado, {username}!</h1>
            <p>✨ Agradecemos por utilizar o <strong>Store Apps Free Bot</strong>.<br>
            Nosso objetivo é facilitar sua gestão de tickets e tornar seu servidor ainda mais profissional.</p>
            <a href="{SUPPORT_SERVER}" class="btn">💬 Atendimento Store Apps</a>
        </div>
        <footer>© 2025 Store Apps Free — Todos os direitos reservados</footer>
    </body>
    </html>
    """)

@app.route('/auth')
def auth_route():
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
