from database import db


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


class Filmes(db.Model):
    __tablename__ = 'filmes'
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    sinopse = db.Column(db.Text, nullable=False)
    data_lancamento = db.Column(db.Date, nullable=True)
    popularidade = db.Column(db.Float, nullable=True)
    media_votos = db.Column(db.Float, nullable=True)
    qtd_votos = db.Column(db.Integer, nullable=True)
    poster_path = db.Column(db.String(255), nullable=True)
    generos = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Filme {self.titulo}>'
