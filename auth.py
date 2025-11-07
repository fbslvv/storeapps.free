from flask import Flask, redirect, request, render_template_string, session, jsonify
import requests
import os
import json
import base64

app = Flask(__name__)
# Secret key for session (keep safe in production)
app.secret_key = "storeapps_secret_key"

# ------------------ CONFIG DISCORD ------------------
DISCORD_CLIENT_ID = "1435836194456862770"
DISCORD_CLIENT_SECRET = "dz-yYXWFbm8Rb6bizEekYLgvAb6Jj2EC"
DISCORD_REDIRECT_URI = "http://localhost:5000/callback"
DISCORD_API_BASE_URL = "https://discord.com/api"
OAUTH_SCOPE = "identify email guilds bot applications.commands"

# ------------------ SUPPORT ------------------
SUPPORT_SERVER = "https://discord.gg/wxzXrUPHJe"

# ------------------ MERCADO PAGO ------------------
MP_ACCESS_TOKEN = "APP_USR-3778188104054704-110615-d4b7694c6359b558b8bfce62c15778e1-2285179310"
MP_API_BASE_URL = "https://api.mercadopago.com"
MP_PREMIUM_PRICE = 8.99  # R$ 8,99

# ------------------ ROUTAS ------------------
@app.route('/')
def home():
    if 'user_data' in session:
        return redirect('/success')
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
      --primary-green: #2ecc71;
      --accent-green: #00ff8a;
      --bg-dark: #050505;
      --panel: #0b0b0b;
      --text-light: #cfeee0;
      --text-main: #ffffff;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: "Poppins", sans-serif; }
    body { min-height: 100vh; color: var(--text-main); background: radial-gradient(circle at 20% 20%, #07100a, var(--bg-dark)); display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; }
    header { position: absolute; top: 30px; width: 100%; text-align: center; z-index: 2; }
    header h1 { font-size: 2.4rem; color: var(--accent-green); letter-spacing: 2px; font-weight: 800; text-shadow: 0 0 20px rgba(0,255,138,0.12); }
    main { text-align: center; z-index: 2; width: 100%; max-width: 980px; }
    main h2 { font-size: 3rem; color: var(--accent-green); margin-bottom: 18px; font-weight: 800; }
    main p { max-width: 800px; margin: 0 auto 30px auto; color: var(--text-light); font-size: 1.1rem; line-height: 1.6; font-weight: 300; }
    .btn-discord { background: linear-gradient(90deg, var(--primary-green), var(--accent-green)); color: black; text-decoration: none; padding: 16px 36px; border-radius: 14px; font-weight: 700; font-size: 1.05rem; box-shadow: 0 10px 40px rgba(46,204,113,0.12); border: 1px solid rgba(255,255,255,0.03); }
    .btn-discord:hover { transform: translateY(-6px); box-shadow: 0 18px 50px rgba(46,204,113,0.18); }
    footer { position: absolute; bottom: 20px; width: 100%; text-align: center; color: #9bbfae; font-size: 0.95rem; z-index: 2; }
    @media (max-width: 768px) {
        body { padding-top: 70px; }
        header h1 { font-size: 1.8rem; }
        main h2 { font-size: 1.9rem; }
    }
  </style>
</head>
<body>
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
  <footer>© 2025 Store Apps Free — Elevando a Experiência no Discord.</footer>
</body>
</html>
    """)

@app.route('/login')
def login():
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
    guild_id = request.args.get("guild_id")

    if not code:
        if 'user_data' in session:
            return redirect('/success')
        return "Erro: nenhum código de autorização recebido.", 400

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
        if 'user_data' in session:
            return redirect('/success')
        return f"Falha ao obter token de acesso: {r.text}", 400

    token_info = r.json()
    access_token = token_info["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    user_info = requests.get(f"{DISCORD_API_BASE_URL}/users/@me", headers=headers).json()
    username = user_info.get("username", "Prezado Usuário")

    SERVER_NAME = "Nome do Servidor Não Encontrado"
    SERVER_ID = guild_id if guild_id else "ID Não Capturado"

    if guild_id:
        try:
            guilds_response = requests.get(f"{DISCORD_API_BASE_URL}/users/@me/guilds", headers=headers)
            if guilds_response.status_code == 200:
                guilds = guilds_response.json()
                found_guild = next((guild for guild in guilds if guild['id'] == guild_id), None)
                if found_guild:
                    SERVER_NAME = found_guild.get('name', 'Servidor sem Nome')
                    SERVER_ID = guild_id
        except requests.RequestException:
            pass

    CHANNEL_NAME = "#configuracao-inicial"
    BOT_STATUS = "Online ✨ Conectado e Operacional"

    session['user_data'] = {
        'username': username,
        'server_name': SERVER_NAME,
        'server_id': SERVER_ID,
        'channel_name': CHANNEL_NAME,
        'bot_status': BOT_STATUS
    }

    return redirect('/success')

@app.route('/success')
def success():
    if 'user_data' not in session:
        return redirect('/')

    data = session['user_data']
    username = data['username']
    SERVER_NAME = data['server_name']
    SERVER_ID = data['server_id']
    CHANNEL_NAME = data['channel_name']
    BOT_STATUS = data['bot_status']

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🎉 Configuração Concluída - Store Apps Bot</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root {{
                --primary-green: #2ecc71;
                --accent-green: #00ff8a;
                --bg-dark: #050505;
                --panel: #0b0b0b;
                --text-light: #cfeee0;
                --text-main: #ffffff;
            }}
            * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: "Poppins", sans-serif; }}
            body {{ min-height: 100vh; background: radial-gradient(circle at 50% 50%, #07100a, var(--bg-dark)); display: flex; align-items: center; justify-content: center; color: var(--text-main); padding: 20px; }}
            .container {{ background: linear-gradient(180deg, rgba(15,15,15,0.9), rgba(8,8,8,0.9)); border: 1px solid rgba(46,204,113,0.1); border-radius: 18px; padding: 36px; max-width: 900px; width: 95%; box-shadow: 0 10px 50px rgba(46,204,113,0.06); }}
            h1 {{ color: var(--accent-green); font-size: 2.6rem; margin-bottom: 10px; }}
            .message-text {{ color: var(--text-light); margin-bottom: 20px; }}
            .server-info-card {{ background: var(--panel); padding: 20px; border-radius: 12px; border-left: 6px solid var(--primary-green); margin-bottom: 20px; }}
            .btn-support {{ display: inline-block; padding: 12px 20px; border-radius: 10px; text-decoration: none; background: linear-gradient(90deg,var(--primary-green),var(--accent-green)); color: black; font-weight: 700; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✨ Configuração Concluída com Sucesso, {username}!</h1>
            <p class="message-text">
                Seu bot de tickets <strong>Store Apps Free</strong> foi implementado com êxito no servidor <strong>{SERVER_NAME}</strong>.
            </p>

            <div class="server-info-card">
                <p>🌐 Servidor: <strong>{SERVER_NAME}</strong></p>
                <p>🆔 ID do Servidor: <code>{SERVER_ID}</code></p>
                <p>💬 Canal Selecionado: <strong>{CHANNEL_NAME}</strong></p>
                <p>🟢 Status do Bot: <strong>{BOT_STATUS}</strong></p>
            </div>

            <a class="btn-support" href="{SUPPORT_SERVER}">Ajuda & Suporte</a>

            <div style="margin-top:24px; padding:18px; background:linear-gradient(90deg, rgba(46,204,113,0.06), rgba(0,255,138,0.03)); border-radius:12px;">
                <h3 style="color:var(--primary-green); margin-bottom:6px;">💎 Plano Premium</h3>
                <p style="color:var(--text-light); margin-bottom:12px;">Valor: <strong>R$ {MP_PREMIUM_PRICE:.2f} / mês</strong></p>
                <a href="/premium" class="btn-support">Adquirir Plano Premium</a>
            </div>
        </div>
    </body>
    </html>
    """)

# ------------------ MERCADO PAGO: Gerar Pix ------------------
@app.route('/payment_init', methods=['POST'])
def payment_init():
    """Endpoint para gerar a transação Pix no Mercado Pago."""
    if 'user_data' not in session:
        return jsonify({'error': 'Sessão expirada ou não autenticada.'}), 401

    user_data = session['user_data']

    # Gera referência única (Idempotency Key)
    external_reference = f"PREMIUM-{user_data['server_id']}-{os.urandom(4).hex()}"

    payment_data = {
        "transaction_amount": MP_PREMIUM_PRICE,
        "description": "Plano Premium Store Apps Bot - 1 Mês",
        "payment_method_id": "pix",
        "installments": 1,
        "external_reference": external_reference,
        "payer": {
            "email": f"usuario_{user_data['server_id']}@storeapps.com"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MP_ACCESS_TOKEN}",
        "X-Idempotency-Key": external_reference
    }

    try:
        mp_response = requests.post(
            f"{MP_API_BASE_URL}/v1/payments",
            json=payment_data,
            headers=headers,
            timeout=15
        )

        # Debug logs (você pode remover depois)
        print(f"[MP] Status: {mp_response.status_code}")
        print(f"[MP] Resposta: {mp_response.text}")

        mp_response.raise_for_status()
        payment = mp_response.json()

        payment_id = payment.get('id')
        # Nem sempre vem qr_code_base64 dependendo da integração, tentamos extrair com segurança
        poi = payment.get('point_of_interaction', {})
        transaction_data = poi.get('transaction_data', {}) if poi else {}
        qr_base64 = transaction_data.get('qr_code_base64')
        qr_code = transaction_data.get('qr_code')

        # Se o MP retornar apenas imagem em URL (raramente) tentamos converter:
        if not qr_base64 and transaction_data.get('qr_code_url'):
            try:
                img_resp = requests.get(transaction_data.get('qr_code_url'))
                img_resp.raise_for_status()
                qr_base64 = base64.b64encode(img_resp.content).decode('utf-8')
            except Exception as e:
                print("[MP] Falha ao baixar qr_code_url:", e)

        session['mp_payment_id'] = payment_id

        return jsonify({
            'success': True,
            'payment_id': payment_id,
            'qr_base64': qr_base64,
            'qr_code': qr_code,
            'external_reference': external_reference
        })

    except requests.exceptions.HTTPError as e:
        return jsonify({'success': False, 'error': f"Erro na API do Mercado Pago (Status {e.response.status_code}): {e.response.text}"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': f"Erro de conexão com o Mercado Pago: {e}"}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f"Erro interno inesperado na geração do Pix: {e}"}), 500

@app.route('/check_payment/<string:payment_id>', methods=['GET'])
def check_payment(payment_id):
    """Endpoint para checar o status do pagamento via polling."""
    headers = {
        "Authorization": f"Bearer {MP_ACCESS_TOKEN}"
    }

    try:
        mp_response = requests.get(
            f"{MP_API_BASE_URL}/v1/payments/{payment_id}",
            headers=headers,
            timeout=10
        )
        mp_response.raise_for_status()
        payment_info = mp_response.json()

        status = payment_info.get('status')

        if status == 'approved':
            if 'mp_payment_id' in session:
                del session['mp_payment_id']
            session['is_premium'] = True
            return jsonify({'status': 'approved', 'message': 'Pagamento Aprovado!'})

        return jsonify({'status': status, 'message': 'Aguardando pagamento...'})

    except requests.exceptions.RequestException:
        return jsonify({'status': 'error', 'message': 'Erro ao verificar pagamento.'}), 500

@app.route('/premium')
def premium_page():
    if 'user_data' not in session:
        return redirect('/')

    if session.get('is_premium'):
        return render_template_string(f"""
        <div style="text-align:center; padding: 50px; background: #07100a; color: white;">
            <h1>✅ Premium Ativo!</h1>
            <p style="margin-bottom: 20px;">Seu Plano Premium já foi resgatado com sucesso.</p>
            <a href="{SUPPORT_SERVER}" style="padding: 15px 30px; background: var(--primary-green); color: black; text-decoration: none; border-radius: 10px; font-weight: bold;">Ir para o Servidor</a>
        </div>
        """)

    data = session['user_data']
    username = data['username']

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🔒 Pagamento Premium - Store Apps</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root {{
                --primary-green: #2ecc71;
                --accent-green: #00ff8a;
                --bg-dark: #050505;
                --panel: #0b0b0b;
                --text-light: #cfeee0;
                --text-main: #ffffff;
            }}
            * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: "Poppins", sans-serif; }}
            body {{ min-height: 100vh; background: radial-gradient(circle at 50% 30%, rgba(0,0,0,0.6), #070707); display: flex; align-items: center; justify-content: center; color: var(--text-main); padding: 20px; }}
            .container {{ width: 100%; max-width: 600px; background: linear-gradient(180deg, rgba(10,10,10,0.9), rgba(6,6,6,0.95)); border-radius: 14px; padding: 22px; box-shadow: 0 10px 50px rgba(46,204,113,0.05); border: 1px solid rgba(46,204,113,0.06); }}
            h1 {{ color: var(--accent-green); font-size: 1.6rem; margin-bottom: 8px; }}
            .subtitle {{ color: var(--text-light); margin-bottom: 12px; }}
            #payment-area {{ background: rgba(8,8,8,0.7); border-radius: 10px; padding: 18px; display:flex; flex-direction: column; align-items:center; gap:12px; }}
            #qr-image-container img {{ width: 220px; height: 220px; border: 6px solid #fff; border-radius: 10px; background: white; box-shadow: 0 6px 30px rgba(46,204,113,0.12); }}
            .price-timer {{ width:100%; display:flex; justify-content:space-between; align-items:center; color:var(--text-light); margin-bottom:6px; }}
            #timer {{ color: var(--accent-green); font-weight:700; }}
            #price {{ color: var(--primary-green); font-weight:700; }}
            #pix-code-display {{ width:100%; background:#0f0f0f; border-radius:8px; padding:10px; display:flex; gap:8px; align-items:center; }}
            #pix-code-text {{ color: #e9ffe7; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
            #pix-copy-button {{ background: linear-gradient(90deg,var(--primary-green),var(--accent-green)); color:black; border:none; padding:10px 14px; border-radius:8px; font-weight:700; cursor:pointer; }}
            .how-to {{ width:100%; margin-top:10px; font-size:0.95rem; color:var(--text-light); background: linear-gradient(180deg, rgba(46,204,113,0.02), transparent); padding:10px; border-radius:8px; }}
            .success-msg {{ color: #2ecc71; font-weight:800; }}
            @media (max-width:480px) {{ #qr-image-container img {{ width:160px; height:160px; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Concluir Pagamento Premium</h1>
            <p class="subtitle">Olá {username} — pague via Pix para ativar seu plano.</p>

            <div id="payment-area">
                <div class="price-timer"><div>Valor a pagar:</div><div id="price">R$ {MP_PREMIUM_PRICE:.2f}</div></div>
                <div class="price-timer"><div>Tempo restante:</div><div id="timer">10:00</div></div>

                <div id="qr-image-container"></div>

                <div id="pix-code-display">
                    <div id="pix-code-text">Gerando código...</div>
                    <button id="pix-copy-button">Copiar</button>
                </div>

                <div class="how-to">
                    <strong>Como pagar com Pix:</strong>
                    <ol style="margin:8px 0 0 18px; padding:0; color:var(--text-light);">
                        <li>Abra o app do seu banco.</li>
                        <li>Escolha "Pix" → "Pagar com código".</li>
                        <li>Cole o código abaixo ou escaneie o QR Code.</li>
                        <li>Confirme o pagamento — em até 10 minutos.</li>
                    </ol>
                </div>

                <div id="success-state" style="display:none;"><p class="success-msg">✅ Pagamento identificado com sucesso!</p><a href="{SUPPORT_SERVER}" style="display:inline-block; padding:10px 16px; border-radius:8px; background:linear-gradient(90deg,var(--primary-green),var(--accent-green)); color:black; font-weight:800; text-decoration:none;">Resgatar Bot</a></div>
                <div id="error-state" style="display:none;"><p style="color:#ff6b6b;">❌ Erro no pagamento.</p><button onclick="location.reload()" style="padding:8px 12px; border-radius:8px; background:#333; color:#fff; border:none;">Tentar Novamente</button></div>
            </div>
        </div>

        <script>
            const INITIAL_TIME = 600;
            let timeRemaining = INITIAL_TIME;
            let timerInterval, pollInterval;
            let paymentId = null;

            function updateTimer(){{
                if(timeRemaining<=0){{
                    clearInterval(timerInterval);
                    clearInterval(pollInterval);
                    document.getElementById('timer').textContent = "00:00";
                    document.getElementById('error-state').style.display = 'block';
                    return;
                }}
                const m = Math.floor(timeRemaining/60).toString().padStart(2,'0');
                const s = (timeRemaining%60).toString().padStart(2,'0');
                document.getElementById('timer').textContent = `${{m}}:${{s}}`;
                timeRemaining--;
            }}

            async function checkPaymentStatus(){{
                if(!paymentId) return;
                try{{
                    const res = await fetch(`/check_payment/${{paymentId}}`);
                    const data = await res.json();
                    if(data.status === 'approved'){{ 
                        clearInterval(timerInterval); clearInterval(pollInterval);
                        document.getElementById('success-state').style.display = 'block';
                        document.getElementById('pix-code-display').style.display = 'none';
                        document.getElementById('qr-image-container').style.display = 'none';
                    }}
                }}catch(e){{
                    console.error("Erro ao checar pagamento:",e);
                }}
            }}

            async function initPayment(){{
                try{{
                    const res = await fetch('/payment_init', {{ method: 'POST', headers: {{ 'Content-Type':'application/json' }} }});
                    const data = await res.json();
                    if(data.success){{
                        paymentId = data.payment_id;
                        // QR
                        const qrContainer = document.getElementById('qr-image-container');
                        if(data.qr_base64){{
                            qrContainer.innerHTML = `<img src="data:image/png;base64,${{data.qr_base64}}" alt="QR Pix">`;
                        }} else if(data.qr_code){{
                            // Gerar imagem de QR via API externa poderia ser feito, aqui apenas mostramos texto
                            qrContainer.innerHTML = '<div style="color:#bbb; padding:12px; text-align:center;">QR gerado (sem imagem)</div>';
                        }} else {{ qrContainer.innerHTML = '<div style="color:#bbb;">QR não disponível</div>'; }}

                        // Pix code
                        const pixText = data.qr_code || '---';
                        document.getElementById('pix-code-text').textContent = pixText;
                        const copyBtn = document.getElementById('pix-copy-button');
                        copyBtn.onclick = async ()=>{{
                            try{{
                                if(navigator.clipboard && window.isSecureContext){{
                                    await navigator.clipboard.writeText(pixText);
                                }}else{{
                                    const ta = document.createElement('textarea');
                                    ta.value = pixText;
                                    document.body.appendChild(ta);
                                    ta.select();
                                    document.execCommand('copy');
                                    ta.remove();
                                }}
                                copyBtn.textContent = 'Copiado!';
                                setTimeout(()=>copyBtn.textContent='Copiar',2000);
                            }}catch(e){{ console.error('Erro ao copiar',e); }}
                        }}

                        // Timer & Polling
                        updateTimer();
                        timerInterval = setInterval(updateTimer,1000);
                        pollInterval = setInterval(checkPaymentStatus,5000);
                    }}else{{
                        document.getElementById('pix-code-text').textContent = 'Erro ao gerar Pix';
                        document.getElementById('error-state').style.display = 'block';
                    }}
                }}catch(e){{
                    console.error('Erro inicialização:', e);
                    document.getElementById('pix-code-text').textContent = 'Erro de conexão';
                    document.getElementById('error-state').style.display = 'block';
                }}
            }}

            document.addEventListener('DOMContentLoaded', initPayment);
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
