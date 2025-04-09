from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# configurando banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dado_cadastro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# defini o modelo de dados da tabela


class Dados(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id auto-incrementada
    nome = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    tell = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    estado_civil = db.Column(db.String(50), nullable=False)
    rua = db.Column(db.String(50), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.String(20), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            'nome': self.nome,
            'idade': self.idade,
            'tell': self.tell,
            'email': self.email,
            'estado civil': self.estado_civil,
            'rua': self.rua,
            'bairro': self.bairro,
            'cep': self.cep,
            'cidade': self.cidade,
            'estado': self.estado
        }


# Cria as tabelas no banco (executar uma vez ou via shell interativo)
with app.app_context():
    db.create_all()

# rota de visualização HTML


@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>Cadastro</title>
        </head>
        <body>
            <p>Visualize os Dados da Sua <u>Empresa</u> em qualquer lugar </p>
            <p>Digitando <b>/dados/<//b> na barra de endereço</p>
        </body>
    </html>
    """

# Rota que renderiza os dados em uma tabela HTML


@app.route('/dados/')
def Tabela_dados():
    dados = Dados.query.all()
    dados_html = ""
    for dd in dados:
        dados_html += f"""
        <tr>
            <td>{dd.id}</td>
            <td>{dd.nome}</td>
            <td>{dd.idade}</td>
            <td>{dd.tell}</td>
            <td>{dd.email}</td>
            <td>{dd.estado_civil}</td>
            <td>{dd.rua}</td>
            <td>{dd.bairro}</td>
            <td>{dd.cep}</td>
            <td>{dd.cidade}</td>
            <td>{dd.estado}</td>
        </tr>
        """
    return f"""
    <html>
        <head>
            <title>Tabela</title>
        </head>
        <body>
            <p><u>Dados Cadastrados</u></p>
            <table border>
                <tr>
                    <th>Id</th>
                    <th>Nome</th>
                    <th>Idade</th>
                    <th>Telefone</th>
                    <th>E-mail</th>
                    <th>Estado Civil</th>
                    <th>Rua</th>
                    <th>Bairro</th>
                    <th>CEP</th>
                    <th>Cidade</th>
                    <th>Estado</th>
                </tr>
                {dados_html}
            </table>
        </body>

    </html>
    """

# Rota da API para listar todos os dados


@app.route('/api/dados/', methods=['GET'])
def api_dados():
    dados = Dados.query.all()
    return jsonify([dd.to_dict() for dd in dados])

# Rota da API para criar um novo dado via POST


@app.route('/api/dados/', methods=['POST'])
def criar_dados():
    data = request.get_json()
    nome = data.get('nome')
    idade = data.get('idade')
    tell = data.get('tell')
    email = data.get('email')
    estado_civil = data.get('estado civil')
    rua = data.get('rua')
    bairro = data.get('bairro')
    cep = data.get('cep')
    cidade = data.get('cidade')
    estado = data.get('estado')
    if not nome or not idade or not tell or not email or not estado_civil or not rua or not bairro or not cep or not cidade or not estado:
        abort(400, "Todos os Campos precisam ser informados corretamente! ")
    novo_dado = Dados(
        nome=nome,
        idade=idade,
        tell=tell,
        email=email,
        estado_civil=estado_civil,
        rua=rua,
        bairro=bairro,
        cep=cep,
        cidade=cidade,
        estado=estado
    )
    db.session.add(novo_dado)
    db.session.commit()  # o id é atribuido automaticamente no commit

    return jsonify(novo_dado.to_dict()), 201

# Função auxiliar para obter um dado pelo id


def get_dados(id):
    dado = Dados.query.get(id)
    if dado is None:
        abort(404, 'Dados não encontrados')
    return dado

# Rota para obter detalhes de um dado pelo id


@app.route('/api/dados/<int:id>/', methods=['GET'])
def detalhar_dados(id):
    dado = get_dados(id)
    return jsonify(dado.to_dict())

# Rota para deletar um dado pelo id


@app.route('/api/dados/<int:id>/', methods=['DELETE'])
def deletar_dados(id):
    dado = get_dados(id)
    db.session.delete(dado)
    db.session.commit()
    return jsonify({'id': id})

# Função auxiliar para obter um dado pelo nome


def get_dados_nome(nome):
    dado = Dados.query.filter_by(nome=nome).first()
    if dado is None:
        abort(404, 'Dados não encontrados')
    return dado

# Rota para obter detalhes de um dado pelo nome


@app.route('/api/dados/<string:nome>/', methods=['GET'])
def detalhar_dados_nome(nome):
    dado = get_dados_nome(nome)
    return jsonify(dado.to_dict())

# Rota para deletar um dado pelo nome


@app.route('/api/dados/<string:nome>/', methods=['DELETE'])
def deletar_dados_nome(nome):
    dado = get_dados_nome(nome)
    db.session.delete(dado)
    db.session.commit()
    return jsonify({'nome': nome})

# Rota para editar completamente um dado pelo id(PUT)


@app.route('/api/dados/<int:id>/', methods=['PUT'])
def editar_dados(id):
    data = request.get_json()
    nome = data.get('nome')
    idade = data.get('idade')
    tell = data.get('tell')
    email = data.get('email')
    estado_civil = data.get('estado civil')
    rua = data.get('rua')
    bairro = data.get('bairro')
    cep = data.get('cep')
    cidade = data.get('cidade')
    estado = data.get('estado')

    if not nome or not idade or not tell or not email or not estado_civil or not rua or not bairro or not cep or not cidade or not estado:
        abort(400, "Todos os Campos precisam ser informados corretamente! ")

    dados = get_dados(id)
    dados.nome = nome
    dados.idade = idade
    dados.tell = tell
    dados.email = email
    dados.estado_civil = estado_civil
    dados.rua = rua
    dados.bairro = bairro
    dados.cep = cep
    dados.cidade = cidade
    dados.estado = estado
    db.session.commit()

    return jsonify(dados.to_dict())

# Rota para edição parcial de um dado pelo id (PATCH)


@app.route("/api/dados/<int:id>/", methods=["PATCH"])
def editar_dados_parcial(id):
    data = request.get_json()
    dado = get_dados(id)

    if "nome" in data:
        dado.nome = data["nome"] or abort(400, "'nome' precisa ser informado!")
    if "idade" in data:
        dado.idade = data["idade"] or abort(
            400, "'idade' precisa ser informada!")
    if "tell" in data:
        dado.tell = data["tell"] or abort(400, "'tell' precisa ser informado!")
    if "email" in data:
        dado.email = data["email"] or abort(
            400, "'email' precisa ser informado!")
    if "estado civil" in data:
        dado.estado_civil = data["estado civil"] or abort(
            400, "'estado civil' precisa ser informado!")
    if "rua" in data:
        dado.rua = data["rua"] or abort(400, "'rua' precisa ser informado!")
    if "bairro" in data:
        dado.bairro = data["bairro"] or abort(
            400, "'bairro' precisa ser informado!")
    if "cep" in data:
        dado.cep = data["cep"] or abort(400, "'cep' precisa ser informado!")
    if "cidade" in data:
        dado.cidade = data["cidade"] or abort(
            400, "'cidade' precisa ser informado!")
    if "estado" in data:
        dado.estado = data["estado"] or abort(
            400, "'estado' precisa ser informado!")

    db.session.commit()
    return jsonify(dado.to_dict())

# Rota para editar completamente um dado pelo nome(PUT)


@app.route('/api/dados/<string:nome>/', methods=['PUT'])
def editar_dados_nome(nome):
    data = request.get_json()
    nome = data.get('nome')
    idade = data.get('idade')
    tell = data.get('tell')
    email = data.get('email')
    estado_civil = data.get('estado civil')
    rua = data.get('rua')
    bairro = data.get('bairro')
    cep = data.get('cep')
    cidade = data.get('cidade')
    estado = data.get('estado')

    if not nome or not idade or not tell or not email or not estado_civil or not rua or not bairro or not cep or not cidade or not estado:
        abort(400, "Todos os Campos precisam ser informados corretamente! ")

    dados = get_dados_nome(nome)
    dados.nome = nome
    dados.idade = idade
    dados.tell = tell
    dados.email = email
    dados.estado_civil = estado_civil
    dados.rua = rua
    dados.bairro = bairro
    dados.cep = cep
    dados.cidade = cidade
    dados.estado = estado
    db.session.commit()

    return jsonify(dados.to_dict())

# Rota para edição parcial de um dado pelo nome (PATCH)


@app.route("/api/dados/<string:nome>/", methods=["PATCH"])
def editar_dados_parcial_nome(nome):
    data = request.get_json()
    dado = get_dados_nome(nome)

    if "nome" in data:
        dado.nome = data["nome"] or abort(400, "'nome' precisa ser informado!")
    if "idade" in data:
        dado.idade = data["idade"] or abort(
            400, "'idade' precisa ser informada!")
    if "tell" in data:
        dado.tell = data["tell"] or abort(400, "'tell' precisa ser informado!")
    if "email" in data:
        dado.email = data["email"] or abort(
            400, "'email' precisa ser informado!")
    if "estado civil" in data:
        dado.estado_civil = data["estado civil"] or abort(
            400, "'estado civil' precisa ser informado!")
    if "rua" in data:
        dado.rua = data["rua"] or abort(400, "'rua' precisa ser informado!")
    if "bairro" in data:
        dado.bairro = data["bairro"] or abort(
            400, "'bairro' precisa ser informado!")
    if "cep" in data:
        dado.cep = data["cep"] or abort(400, "'cep' precisa ser informado!")
    if "cidade" in data:
        dado.cidade = data["cidade"] or abort(
            400, "'cidade' precisa ser informado!")
    if "estado" in data:
        dado.estado = data["estado"] or abort(
            400, "'estado' precisa ser informado!")

    db.session.commit()
    return jsonify(dado.to_dict())


# Tratamento de erro para 400 e 404
@app.errorhandler(400)
def erro_400(erro):
    return jsonify({"erro": str(erro)}), 400


@app.errorhandler(404)
def erro_404(erro):
    return jsonify({"erro": str(erro)}), 404


#app.run(debug=True)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Usa a variável de ambiente PORT se estiver definida, senão usa 5000
    app.run(host='0.0.0.0', port=port, debug=True)