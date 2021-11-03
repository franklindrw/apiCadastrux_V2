from flask_mysqldb import MySQL


class DevelopmentConfig():
    DEBUG = True

    #Banco de dados
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'cadastrux'

config = {
    'development': DevelopmentConfig
}