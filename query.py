import sqlite3

class Lite_db():
    
    def __init__(self,banco =None):
        self.banco = None
        self.cursor = None

        if banco:
            self.open(banco)
    
    def open(self,banco):
        try:
            self.banco = sqlite3.connect(banco)
            self.cursor = self.banco.cursor()
            #print('conexão criada com sucesso!')
        except sqlite3.Error as e:
            #print('Não foi possivel estabelecer conexão')
            pass


    def criar_tabela_funcs(self):
        cursor = self.cursor
        cursor.execute('''CREATE TABLE funcs(
            id integer primary key autoincrement,
            nome text,
            endereco text,
            documento integer,
            admin integer
            )''')

    def criar_tabela_users(self):
        cursor = self.cursor
        cursor.execute('''CREATE TABLE users(
            id integer primary key,
            username text,
            password text,
            acesso text)''')

    def inserir_apaga_atualiza(self,query):
        cursor = self.cursor
        cursor.execute(query)
        self.banco.commit()


    def pega_dados(self,query):
        cursor = self.cursor
        cursor.execute(query)
        return cursor.fetchall()





db = Lite_db('mananger.db')
#db.criar_tabelas()
#db.criar_tabela_users()
#db.inserir_apaga_atualiza('''INSERT INTO funcs (nome,
#documento,endereco,admin) VALUES (
#"Jessica","342434","casa da tigresa","0")''')
#db.inserir_apaga_atualiza('''UPDATE funcs SET nome
#= "Paulo" WHERE nome = "PAULO"''')

#print(db.pega_dados ("SELECT * FROM funcs"))
