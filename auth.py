from flask import Flask, redirect, request, render_template_string
import requests
import os

app = Flask(__name__)
# Mantenha a secret_key segura. Para produção, considere usar variáveis de ambiente.
app.secret_key = "storeapps_secret_key"

# CONFIGURAÇÕES DO DISCORD
DISCORD_CLIENT_ID = "1435836194456862770"
DISCORD_CLIENT_SECRET = "dz-yYXWFbm8Rb6bizEekYLgvAb6Jj2EC"
# ATENÇÃO: Mude "http://localhost:5000" para o seu domínio em produção
DISCORD_REDIRECT_URI = "http://localhost:5000/callback" 
DISCORD_API_BASE_URL = "https://discord.com/api"
OAUTH_SCOPE = "identify email guilds bot applications.commands"

# SERVIDOR DE SUPORTE (Store Apps)
SUPPORT_SERVER = "https://discord.gg/wxzXrUPHJe" # Link de convite do suporte Store Apps

# --- Rota Principal (Home) ---
@app.route('/')
def home():
    # Conteúdo da Home com design neon
    return render_template_string("""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Store Apps Free - Criador de Bot de Ticket</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary-neon: #00e9ff;
      --secondary-blue: #5865f2;
      --bg-dark: #000000;
      --bg-gradient-start: #010205;
      --bg-gradient-end: #0a0f25;
      --text-light: #b0c4de;
      --text-main: white;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: "Poppins", sans-serif;
    }

    body {
      height: 100vh;
      overflow: hidden;
      color: var(--text-main);
      background: radial-gradient(circle at 20% 20%, var(--bg-gradient-start), var(--bg-dark));
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      position: relative;
    }

    canvas#bg {
      position: fixed;
      top: 0;
      left: 0;
      z-index: 0;
    }

    header {
      position: absolute;
      top: 40px;
      width: 100%;
      text-align: center;
      z-index: 2;
      padding: 10px;
    }

    header h1 {
      font-size: 2.8rem;
      color: var(--primary-neon);
      letter-spacing: 3px;
      font-weight: 800;
      text-shadow: 0 0 35px rgba(0, 233, 255, 1);
      background: linear-gradient(90deg, #00b0ff, #00e9ff);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: pulsate 2s infinite alternate;
    }

    main {
      text-align: center;
      z-index: 2;
      position: relative;
      padding: 0 20px;
    }

    main h2 {
      font-size: 3.5rem;
      color: var(--primary-neon);
      margin-bottom: 25px;
      font-weight: 800;
      text-shadow: 0 0 40px rgba(0, 233, 255, 1);
      line-height: 1.2;
    }

    main p {
      max-width: 700px;
      margin: 0 auto 50px auto;
      color: var(--text-light);
      font-size: 1.3rem;
      line-height: 1.7;
      font-weight: 300;
    }

    .btn-discord {
      background: var(--secondary-blue);
      color: white;
      text-decoration: none;
      padding: 20px 45px;
      border-radius: 18px;
      font-weight: 700;
      font-size: 1.3rem;
      transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
      box-shadow: 0 10px 40px rgba(88, 101, 242, 0.8);
      display: inline-block;
      transform: translateY(0);
      animation: float 4s ease-in-out infinite, neon-glow 1.5s infinite alternate;
      border: 2px solid var(--secondary-blue);
    }

    .btn-discord:hover {
      background: linear-gradient(90deg, #6a79f3, #4752c4);
      transform: translateY(-8px) scale(1.08);
      box-shadow: 0 20px 60px rgba(88, 101, 242, 1);
      border-color: var(--primary-neon);
    }

    footer {
      position: absolute;
      bottom: 30px;
      width: 100%;
      text-align: center;
      color: #999;
      font-size: 1rem;
      z-index: 2;
    }

    footer a {
      color: var(--primary-neon);
      text-decoration: none;
      transition: color 0.3s;
    }

    footer a:hover {
      color: #00ceff;
      text-decoration: underline;
    }

    @keyframes float {
      0% { transform: translateY(0); }
      50% { transform: translateY(-12px); }
      100% { transform: translateY(0); }
    }

    @keyframes neon-glow {
      from { box-shadow: 0 0 10px var(--secondary-blue), 0 0 20px var(--secondary-blue), 0 0 30px var(--secondary-blue); }
      to { box-shadow: 0 0 15px var(--secondary-blue), 0 0 30px var(--primary-neon), 0 0 45px var(--primary-neon); }
    }

    @keyframes pulsate {
      0% { text-shadow: 0 0 25px rgba(0, 233, 255, 0.8), 0 0 50px rgba(0, 233, 255, 0.5); }
      100% { text-shadow: 0 0 35px rgba(0, 233, 255, 1), 0 0 70px rgba(0, 233, 255, 0.7); }
    }

    .particle-glow {
        filter: drop-shadow(0 0 8px var(--primary-neon));
    }
  </style>
</head>
<body>
  <canvas id="bg"></canvas>

  <header>
    <h1>Store Apps Free</h1>
  </header>

  <main>
    <h2>Crie e Gerencie Seu Bot de Ticket com Excelência</h2>
    <p>
      Com o <strong>Store Apps Free</strong>, a automação do seu suporte nunca foi tão fácil.
      Configure seu bot de tickets no Discord em segundos, de forma <strong>rápida, intuitiva e totalmente gratuita</strong>.
      Eleve a organização e a eficiência do atendimento em seu servidor a um novo patamar.
    </p>
    <a href="/login" class="btn-discord">🚀 Iniciar Configuração do Bot</a>
  </main>

  <footer>
    © 2025 Store Apps Free — Elevando a Experiência no Discord.
  </footer>

  <script>
    const canvas = document.getElementById("bg");
    const ctx = canvas.getContext("2d");

    let particles = [];
    const numParticles = 120;

    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }

    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    class Particle {
      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2.5 + 1;
        this.speedX = (Math.random() - 0.5) * 1.8;
        this.speedY = (Math.random() - 0.5) * 1.8;
        this.color = "rgba(0,233,255,0.9)";
      }

      update() {
        this.x += this.speedX;
        this.y += this.speedY;

        if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
        if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
      }

      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.color;
        ctx.fill();
      }
    }

    function init() {
      particles = [];
      for (let i = 0; i < numParticles; i++) {
        particles.push(new Particle());
      }
    }

    function animate() {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.4)'; 
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      particles.forEach((p) => {
        p.update();
        p.draw();
      });
      connectParticles();
      requestAnimationFrame(animate);
    }

    function connectParticles() {
      let opacityValue = 1;
      for (let a = 0; a < particles.length; a++) {
        for (let b = a; b < particles.length; b++) {
          let dx = particles[a].x - particles[b].x;
          let dy = particles[a].y - particles[b].y;
          let distance = Math.sqrt(dx * dx + dy * dy);
          if (distance < 150) {
            opacityValue = 1 - distance / 150;
            ctx.strokeStyle = "rgba(0,233,255," + opacityValue + ")";
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(particles[a].x, particles[a].y);
            ctx.lineTo(particles[b].x, particles[b].y);
            ctx.stroke();
          }
        }
      }
    }

    init();
    animate();
  </script>
</body>
</html>
    """)

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
    # Captura o ID do servidor que o Discord envia na URL de retorno
    guild_id = request.args.get("guild_id")

    if not code:
        return "Erro: nenhum código de autorização recebido.", 400

    # 1. Troca o "code" por token de acesso
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
        return f"Falha ao obter token de acesso: {r.text}", 400

    token_info = r.json()
    access_token = token_info["access_token"]

    # 2. Pega informações do usuário (necessário para o nome de boas-vindas)
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info = requests.get(f"{DISCORD_API_BASE_URL}/users/@me", headers=headers).json()
    username = user_info.get("username", "Prezado Usuário")

    # --- 3. LÓGICA PARA OBTER O NOME REAL DO SERVIDOR ---
    SERVER_NAME = "Nome do Servidor Não Encontrado"
    SERVER_ID = guild_id if guild_id else "ID Não Capturado"
    
    if guild_id:
        try:
            # Requisita a lista de servidores do usuário (requer o scope 'guilds')
            guilds_response = requests.get(f"{DISCORD_API_BASE_URL}/users/@me/guilds", headers=headers)
            
            if guilds_response.status_code == 200:
                guilds = guilds_response.json()
                
                # Busca o servidor na lista que corresponde ao guild_id capturado
                found_guild = next((guild for guild in guilds if guild['id'] == guild_id), None)

                if found_guild:
                    SERVER_NAME = found_guild.get('name', 'Servidor sem Nome')
                    SERVER_ID = guild_id
                # Se não encontrar, mantemos o guild_id para referência, mas a mensagem padrão
                
            else:
                # Falha na requisição de guilds (ex: token de acesso pode ter expirado ou permissão negada)
                SERVER_NAME = f"Erro ao buscar servidores ({guilds_response.status_code})"
                
        except requests.RequestException:
            SERVER_NAME = "Erro de conexão com a API do Discord."

    # --- OUTROS DADOS (Mock mantido por serem difíceis de obter via OAuth User) ---
    CHANNEL_NAME = "#configuracao-inicial"
    BOT_STATUS = "Online ✨ Conectado e Operacional"
    # --- FIM DOS DADOS ---


    return render_template_string(f"""
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🎉 Configuração Concluída - Store Apps Bot</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root {{
                --primary-neon: #00e9ff;
                --secondary-blue: #5865f2;
                --bg-dark: #000000;
                --success-bg: rgba(0, 0, 0, 0.85);
                --text-light: #e0f2f7;
                --text-main: white;
            }}
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: "Poppins", sans-serif;
            }}

            body {{
                height: 100vh;
                background: radial-gradient(circle at 50% 50%, var(--bg-dark) 0%, #05060a 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--text-main);
                overflow-y: auto;
                position: relative;
            }}
            
            .background-glow {{
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle at 60% 60%, rgba(0, 233, 255, 0.15) 0%, transparent 50%);
                animation: bg-pulse 15s infinite alternate ease-in-out;
                z-index: 0;
            }}

            .container {{
                position: relative;
                z-index: 1;
                background: var(--success-bg);
                border: 2px solid var(--primary-neon);
                border-radius: 25px;
                box-shadow: 0 0 60px rgba(0, 233, 255, 0.7);
                padding: 50px;
                text-align: center;
                max-width: 850px;
                width: 90%;
                margin: 20px 0;
                backdrop-filter: blur(12px);
                transition: transform 0.4s ease-in-out;
                animation: fadeInScale 1s ease-out forwards;
            }}
            
            .container:hover {{
                transform: translateY(-8px) scale(1.01);
            }}

            h1 {{
                font-size: 3rem;
                color: var(--primary-neon);
                margin-bottom: 25px;
                font-weight: 800;
                text-shadow: 0 0 20px rgba(0,233,255,1);
                animation: pulsate 2s infinite alternate;
            }}

            .message-text {{
                font-size: 1.25rem;
                color: var(--text-light);
                margin-bottom: 35px;
                line-height: 1.6;
                font-weight: 300;
            }}

            .server-info-card {{
                background: rgba(10, 15, 40, 0.5);
                border-radius: 18px;
                padding: 30px;
                margin-bottom: 40px;
                text-align: left;
                border-left: 6px solid var(--primary-neon);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6);
                display: flex;
                flex-direction: column;
                gap: 15px;
                animation: slideInLeft 0.8s ease-out forwards;
            }}
            
            .server-details p {{
                margin: 0;
                color: var(--text-light);
                font-size: 1.1rem;
                display: flex;
                align-items: center;
                gap: 10px;
            }}

            .server-details strong {{
                color: var(--text-main);
                font-weight: 600;
            }}

            .server-details span.icon {{
                font-size: 1.5rem;
                color: var(--primary-neon);
                text-shadow: 0 0 10px var(--primary-neon);
            }}

            .status-badge {{
                display: inline-block;
                padding: 8px 15px;
                border-radius: 10px;
                font-size: 1rem;
                font-weight: 700;
                background: linear-gradient(90deg, #2ecc71, #27ae60);
                color: var(--bg-dark);
                box-shadow: 0 0 15px rgba(46, 204, 113, 0.7);
                margin-left: auto;
            }}

            .premium-box {{
                background: linear-gradient(145deg, rgba(88, 101, 242, 0.15), rgba(0, 233, 255, 0.1));
                border: 2px solid var(--secondary-blue);
                border-radius: 20px;
                padding: 35px;
                margin-top: 40px;
                text-align: center;
                box-shadow: 0 0 30px rgba(88, 101, 242, 0.5);
                animation: slideInRight 0.8s ease-out forwards;
            }}
            
            .premium-box h3 {{
                color: var(--secondary-blue);
                font-size: 1.8rem;
                margin-bottom: 15px;
                text-shadow: 0 0 10px rgba(88, 101, 242, 0.8);
            }}
            
            .premium-box p {{
                font-size: 1.15rem;
                color: var(--text-light);
                margin-bottom: 25px;
                line-height: 1.6;
            }}
            
            .price-tag {{
                font-size: 3rem;
                font-weight: 800;
                color: var(--primary-neon);
                margin: 15px 0 25px 0;
                display: block;
                text-shadow: 0 0 20px rgba(0, 233, 255, 0.8);
                background: linear-gradient(45deg, #00b0ff, #00e9ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            
            .btn-group {{
                display: flex;
                justify-content: center;
                gap: 20px;
                flex-wrap: wrap;
            }}

            a.btn {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                text-decoration: none;
                padding: 18px 38px;
                border-radius: 15px;
                font-weight: 700;
                transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
                font-size: 1.15rem;
                gap: 10px;
            }}
            
            .btn-support {{
                background: linear-gradient(90deg, #00a2ff, #00e9ff);
                color: var(--bg-dark);
                box-shadow: 0 8px 25px rgba(0,162,255,0.7);
                border: 2px solid var(--primary-neon);
            }}

            .btn-premium {{
                background: linear-gradient(90deg, #5865f2, #7289da);
                color: white;
                box-shadow: 0 8px 25px rgba(88, 101, 242, 0.7);
                border: 2px solid var(--secondary-blue);
            }}
            
            .btn-support:hover {{
                background: linear-gradient(90deg, #00c0ff, #00ffff);
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0,233,255,0.9);
                border-color: white;
            }}

            .btn-premium:hover {{
                background: linear-gradient(90deg, #4752c4, #6272b3);
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(88, 101, 242, 0.9);
                border-color: white;
            }}
            
            footer {{
                margin-top: 50px;
                color: #a0a0a0;
                font-size: 0.95rem;
            }}

            /* Animações */
            @keyframes fadeInScale {{
                from {{ opacity: 0; transform: scale(0.9) translateY(20px); }}
                to {{ opacity: 1; transform: scale(1) translateY(0); }}
            }}

            @keyframes slideInLeft {{
                from {{ opacity: 0; transform: translateX(-50px); }}
                to {{ opacity: 1; transform: translateX(0); }}
            }}

            @keyframes slideInRight {{
                from {{ opacity: 0; transform: translateX(50px); }}
                to {{ opacity: 1; transform: translateX(0); }}
            }}

            @keyframes bg-pulse {{
                0% {{ transform: scale(1); opacity: 0.6; }}
                50% {{ transform: scale(1.05); opacity: 0.8; }}
                100% {{ transform: scale(1); opacity: 0.6; }}
            }}

            @keyframes pulsate {{
                0% {{ text-shadow: 0 0 15px var(--primary-neon), 0 0 30px var(--primary-neon), 0 0 45px rgba(0, 233, 255, 0.5); }}
                100% {{ text-shadow: 0 0 25px var(--primary-neon), 0 0 40px var(--primary-neon), 0 0 60px rgba(0, 233, 255, 0.8); }}
            }}
        </style>
    </head>
    <body>
        <div class="background-glow"></div>
        <div class="container">
            <h1>✨ Configuração Concluída com Sucesso, {username}!</h1>
            <p class="message-text">
                Seu bot de tickets <strong>Store Apps Free</strong> foi implementado com êxito no servidor <strong>{SERVER_NAME}</strong>.
                Prepare-se para uma gestão de tickets otimizada e eficiente.
            </p>

            <div class="server-info-card">
                <div class="server-details">
                    <p><span class="icon">🌐</span> Servidor: <strong>{SERVER_NAME}</strong></p>
                    <p><span class="icon">🆔</span> ID do Servidor: <code>{SERVER_ID}</code></p>
                    <p><span class="icon">💬</span> Canal Selecionado: <strong>{CHANNEL_NAME}</strong></p>
                    <p style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="display: flex; align-items: center; gap: 10px;"><span class="icon">🟢</span> Status do Bot:</span> 
                        <span class="status-badge">{BOT_STATUS}</span>
                    </p>
                </div>
            </div>

            <div class="btn-group">
                <a href="{SUPPORT_SERVER}" class="btn btn-support">
                    <span>Ajuda & Suporte</span> <span class="icon">💡</span>
                </a>
            </div>
            
            <div class="premium-box">
                <h3>💎 Desbloqueie o Potencial Máximo: Plano Premium!</h3>
                <p>
                    Obtenha uma experiência sem fronteiras com o plano <strong>Premium</strong>: recursos ilimitados, personalizações avançadas,
                    suporte prioritário e elimine quaisquer restrições de uso. Leve seu servidor ao próximo nível.
                </p>
                <span class="price-tag">R$ 8,99 / mês</span>
                <a href="{SUPPORT_SERVER}" class="btn btn-premium">
                    <span>Adquirir Plano Premium</span> <span class="icon">⚡</span>
                </a>
            </div>

        </div>
        <footer>© 2025 Store Apps Free — Todos os direitos reservados. Experiência e Eficiência.</footer>
    </body>
    </html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)