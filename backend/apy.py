from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Iniciando o Flask
app = Flask(__name__)

# Conectando com o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)

# Resetando tokens de conexão
reset_tokens = {}


# Criando classe de banco de dados
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pw_hash = db.Column(db.String(255), nullable=False)
    generos_fav = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.username}>'

# Rota de login


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    print("requisição recebida")

    usuario_db = Usuario.query.filter_by(username=username).first()

    if usuario_db and check_password_hash(usuario_db.pw_hash, password):
        print("Autenticação bem sucedida")
        return jsonify({"success": True, "message": "Login realizado com sucesso"})
    else:
        print("Autenticacao falhou!!")
        return jsonify({"success": False, "message": "usuario ou senha incorreta"}), 401

# Rota de status da API.


@app.route('/status')
def status():
    return jsonify({'status': "API FUNCIONANDO"})

# Simulação básica de recomendação


@app.route('/filmes/mock')
def recomendacoes_mock():
    filmes_falsos = [
        {'id': 1, 'titulo': 'Norbit', 'ano': '2023'},
        {'id': 2, 'titulo': 'as branquelas', 'ano': '2024'},
        {'id': 3, 'titulo': 'vovozona', 'ano': '2022'},
    ]
    return jsonify(filmes_falsos)

# Rota de cadastro de usuário


@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    user = data.get("user")
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    generos = data.get("generos_fav")

    print("requisição recebida")

    if Usuario.query.filter_by(username=user).first() is not None:
        return jsonify({"success": False, "message": "Nome de usuário já existe"}), 409
    if Usuario.query.filter_by(email=email).first() is not None:
        return jsonify({"success": False, "message": "Email já cadastrado"}), 401

    hashed_password = generate_password_hash(password)

    generos_str = ",".join(generos) if generos else ""

    novo_usuario = Usuario(
        username=user,
        name=name,
        email=email,
        pw_hash=hashed_password,
        generos_fav=generos_str

    )

    db.session.add(novo_usuario)
    db.session.commit()

    print(f"novo usuario {user} cadastrado com sucesso")
    return jsonify({
        "success": True,
        "message": f"usuario {user} cadastrado com sucesso!"}), 200

# Rota para o reset da senha


@app.route('/reset_senha', methods=['POST'])
def resetar_senha():
    data = request.get_json()
    email = data.get("email")

    usuario_db = Usuario.query.filter_by(email=email).first()
    if not usuario_db:
        return jsonify({"success": False, "message": "Email não existe no banco de dados"})
    print("recebemos o email")
    token = secrets.token_urlsafe(32)
    expira = datetime.now() + timedelta(minutes=30)
    reset_tokens[token] = {"email": email, "expira": expira}

    link = f"http://localhost:8501/redefinir?token={token}"

    msg = MIMEText(f"Clique no link para redefinir sua senha: {link}")
    msg['Subject'] = "Redefinição de senha"
    msg['From'] = "rotacinefilmes@gmail.com"
    msg['To'] = email

    try:
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT")) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
            server.sendmail(msg['From'], msg['To'], msg.as_string())
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao enviar o email: {e}"
        })
    return jsonify({
        "success": True,
        "message": f"Email enviado com instruções para {email}"
    })

# Rota para redefinir a senha


@app.route('/redefinir', methods=["POST"])
def confirmar_reset():
    data = request.get_json()
    token = data.get("token")
    new_pw = data.get("new_pw")

    info = reset_tokens.get(token)
    if not info or datetime.now() > info['expira']:
        return jsonify({
            "sucess": False,
            "message": "Token inválido ou expirado"}), 400

    email = info["email"]

    usuario_db = Usuario.query.filter_by(email=email).first()
    if not usuario_db:
        return jsonify({"success": False, "message": "Email não existe no banco de dados"})

    usuario_db.pw_hash = generate_password_hash(new_pw)
    db.session.commit()

    del reset_tokens[token]
    print(f"Senha de {email} foi alterada no banco de dados")

    return jsonify({
        "sucess": True,
        "message": "senha redefinida com sucesso!"
    })

# Inicialização do bloco de código main()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
