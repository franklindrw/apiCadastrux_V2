from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)

conexao = MySQL(app)

# usuarios

# pesquisa todos os usuarios
@app.route('/usuarios', methods=['GET'])
def listarUsuarios():
    try:
        cursor = conexao.connection.cursor()
        sql="SELECT IDUSUARIO, USUARIO, STATUS FROM USUARIOS"
        cursor.execute(sql)
        dados = cursor.fetchall()
        usuarios = []
        for linha in dados:
            usuario = {'id':linha[0], 'usuario':linha[1], 'status':linha[2]}
            usuarios.append(usuario)        
        return jsonify({'usuarios': usuarios, 'mesagem':"Usuários Listados"})
    except Exception as ex:
        return jsonify({'mesagem':"Nenhuma informação encontrada"})


# pesquisa um usuario especifico
@app.route('/usuarios/<usuario>/<senha>', methods=['GET'])
def verificarUsuario(usuario, senha):
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT IDUSUARIO, USUARIO, SENHA FROM USUARIOS WHERE USUARIO = '{0}' AND SENHA = '{1}'".format(usuario, senha) 
        cursor.execute(sql)
        dados = cursor.fetchone()
        if dados != None:
            usuario = {'id':dados[0], 'usuario':dados[1], 'senha':dados[2]}
            return jsonify({'usuario': usuario, 'mesagem':"Usuários Listados"})
        else:
            return jsonify({})
    except Exception as ex:
        return jsonify({'mensagem':"Erro ao consultar na API"})


# cria usuario
@app.route('/usuarios/criar/<usuario>/<senha>', methods=['POST'])
def criarCadastro(usuario, senha):
    try:
        cursor = conexao.connection.cursor()
        sql = "INSERT INTO USUARIOS (USUARIO, SENHA, STATUS) VALUES ('{0}', '{1}', 'True')".format(usuario, senha)
        cursor.execute(sql)
        conexao.connection.commit()
        return 'usuário cadastrado!'
    except Exception as ex:
        return jsonify({'mensagem':"Erro ao consultar na API"})

# atualizar senha
@app.route('/usuarios/update/<senha>/<idUsuario>', methods=['PUT'])
def atualizarCadastro(senha, idUsuario):
    try:
        cursor = conexao.connection.cursor()
        sql = "update usuarios u set u.SENHA = '{0}' where u.IDUSUARIO = '{1}'".format(senha, idUsuario)
        cursor.execute(sql)
        conexao.connection.commit()
        return 'senha Atualizada!'
    except Exception as ex:
        return jsonify({'mensagem':"Erro ao atualizar dados!!!"})

# deletar usuario
@app.route('/usuarios/delete/<idUsuario>', methods=['DELETE'])
def deletarCadastro(idUsuario):
    try:
        cursor = conexao.connection.cursor()
        sql = "delete from usuarios where IDUSUARIO = '{0}'".format(idUsuario)
        cursor.execute(sql)
        conexao.connection.commit()
        return 'usuario Deletado'
    except Exception as ex:
        return jsonify({'mensagem':"Erro ao atualizar dados!!!"})


# Produtos
@app.route('/outdoor', methods=['GET'])
def listarOutdoor():
    try:
        cursor = conexao.connection.cursor()
        sql="SELECT P.IDPRODUTO, P.PRODNOME, P.DESCRICAO, PRE.PRECO, P.CATEGORIA, P.IMAGEM FROM PRODUTOS P INNER JOIN precos pre ON PRE.ID_PRODUTO = P.IDPRODUTO"
        cursor.execute(sql)
        dados = cursor.fetchall()
        produtos = []
        for linha in dados:
            produto = {'id':linha[0], 'produto':linha[1], 'descricao':linha[2], 'preco':linha[3], 'categoria':linha[4], 'imagem':linha[5]}
            produtos.append(produto)
        return jsonify({'produtos': produtos})
    except Exception as ex:
        return jsonify({'mesagem':"Nenhuma informação encontrada"})

def pagina_nao_encontrada(error):
    return "<h2>A página que está tentando buscar não existe</h2>"


# criar produto
@app.route('/criaProduto/<prodnome>/<desc>/<categoria>/<preco>', methods=['POST'])
def criarProduto(prodnome, desc, categoria, preco):
    try:
        cursor = conexao.connection.cursor()
        sql = "insert into produtos p (p.PRODNOME, p.DESCRICAO, p.IMAGEM, p.CATEGORIA) values ('{0}', '{1}', null, '{2}')".format(prodnome, desc, categoria)
        cursor.execute(sql)
        conexao.connection.commit()

        sql2 = "SELECT IDPRODUTO FROM PRODUTOS ORDER BY IDPRODUTO DESC LIMIT 1"
        idproduto = cursor.execute(sql2)

        sql3 = "insert into precos p (p.PRECO, p.ID_PRODUTO) values ('{0}', '{1}')".format(preco, idproduto)
        cursor.execute(sql3)
        conexao.connection.commit()


        return 'produto Cadastrado!'
    except Exception as ex:
        return jsonify({'mensagem':"Erro ao consultar na API"})


@app.route('/produtos', methods=['GET'])
def listarProdutos():
    try:
        cursor = conexao.connection.cursor()
        sql="SELECT P.IDPRODUTO, P.PRODNOME, P.DESCRICAO, PRE.PRECO, P.CATEGORIA FROM PRODUTOS P INNER JOIN precos pre ON PRE.ID_PRODUTO = P.IDPRODUTO"
        cursor.execute(sql)
        dados = cursor.fetchall()
        produtos = []
        for linha in dados:
            produto = {'id':linha[0], 'produto':linha[1], 'descricao':linha[2], 'preco':linha[3], 'categoria':linha[4]}
            produtos.append(produto)
        return jsonify({'produtos': produtos})
    except Exception as ex:
        return jsonify({'mesagem':"Nenhuma informação encontrada"})

def pagina_nao_encontrada(error):
    return "<h2>A página que está tentando buscar não existe</h2>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_nao_encontrada)
    app.run()