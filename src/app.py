from flask import Flask, jsonify
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)

conexao = MySQL(app)

@app.route('/usuarios', methods=['GET'])
def listarUsuarios():
    try:
        cursor = conexao.connection.cursor()
        sql="SELECT IDUSUARIO, USUARIO, SENHA FROM USUARIOS"
        cursor.execute(sql)
        dados = cursor.fetchall()
        usuarios = []
        for linha in dados:
            usuario = {'id':linha[0], 'usuario':linha[1], 'senha':linha[2]}
            usuarios.append(usuario)        
        return jsonify({'usuarios': usuarios, 'mesagem':"Usuários Listados"})
    except Exception as ex:
        return jsonify({'mesagem':"Nenhuma informação encontrada"})


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

def pagina_nao_encontrada(error):
    return "<h2>A página que está tentando buscar não existe</h2>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_nao_encontrada)
    app.run()