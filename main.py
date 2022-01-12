
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import sys
from tela_inicial import Ui_inicial
from tela_cadastrar import Ui_cadastro
from tela_login import Ui_login
from tela_atualizar import Ui_atualizar
from tela_consulta import Ui_consulta
from query import Lite_db

class Cadastrar(QDialog,Ui_cadastro):
    def __init__(self):
        super(Cadastrar,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Tela de Cadastro')

        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.canc)
        self.pushButton_3.clicked.connect(self.limpar)

       

    def add(self):
        db = Lite_db('mananger.db')

        name = self.lineEdit.text()
        end = self.lineEdit_2.text()
        doc = self.lineEdit_3.text()
        admin = 1
        if name =='' or doc =='' or end =='':
            #QMessageBox.information(QMessageBox(),"OPA OPA","Preencha todos os campos!")
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Atenção!")
            msg.setText("Preencha todos os campos!")
            msg.exec()
        else:
            db.inserir_apaga_atualiza(f'''INSERT INTO funcs (nome,endereco,documento,admin)
            VALUES ('{name}','{end}','{doc}','{admin}')''')
            #QMessageBox.information(QMessageBox(),"OPA OPA","DADOS GRAVADOS COM SUCESSO!")
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Inseridos no banco!")
            msg.setText("Dados gravados com sucesso!")
            msg.exec()

            self.limpar()

    def canc(self):
        self.close()

    def limpar(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')



class Atualizar(QDialog,Ui_atualizar):
    def __init__(self):
        super(Atualizar,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Tela de atualização')

        self.carrega_dados()
        self.tableWidget.itemSelectionChanged.connect(self.preencher_dados)
        self.pushButton_4.clicked.connect(self.apagar_cadastro)
        self.pushButton_3.clicked.connect(self.limpar_campos)
        self.pushButton_2.clicked.connect(self.atualizar_cadastro)
        self.pushButton.clicked.connect(self.consultar)


    def preencher_dados(self):
        id_linha_selecionada = self.pega_selecao_banco()

        if self.tableWidget.item(id_linha_selecionada,1)!=None:
            nome = self.tableWidget.item(id_linha_selecionada,1).text()
            self.lineEdit_2.setText(nome)

        if self.tableWidget.item(id_linha_selecionada,2)!=None:
            endereco = self.tableWidget.item(id_linha_selecionada,2).text()
            self.lineEdit_3.setText(endereco)

        if self.tableWidget.item(id_linha_selecionada,3)!=None:
            documento = self.tableWidget.item(id_linha_selecionada,3).text()
            self.lineEdit_4.setText(documento)
    
    
    
    def pega_selecao_banco(self):
        return self.tableWidget.currentRow()
        
    
    def pega_selecao_tabela(self):
        valor = self.tableWidget.item(self.pega_selecao_banco(),0)
        return valor.text() 
   
   
   
    def apagar_cadastro(self):
        try:
            db = Lite_db('mananger.db')
            id = self.pega_selecao_tabela()
            db.inserir_apaga_atualiza(f'DELETE FROM funcs WHERE id = "{id}"')
            #QMessageBox.information(QMessageBox(),'Você Perdeu!','Dados deletados!')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Você Removeu!")
            msg.setText("Dados deletados com sucesso")
            msg.exec()
            self.carrega_dados()
       
        except:
            #QMessageBox.warning(QMessageBox(),'Algo deu errado!','Não foi possivel deletar!')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Algo deu errado!")
            msg.setText("Não foi possivel deletar os dados!")
            msg.exec()
    
    def atualizar_cadastro(self):
        try:
            db = Lite_db('mananger.db')
            id = self.pega_selecao_tabela()
            
            nome = self.lineEdit_2.text()
            endereco = self.lineEdit_3.text()
            documento = self.lineEdit_4.text()

            db.inserir_apaga_atualiza(f'''UPDATE funcs SET nome = "{nome}",
            endereco = "{endereco}",documento = "{documento}"
            WHERE id = "{id}"''')

            #QMessageBox.warning(QMessageBox(),'Completado','Atualizado Cadastro')

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Completado!")
            msg.setText("Atualizado o Cadastro!")
            msg.exec()
            self.carrega_dados()
        
        except:
            #QMessageBox.warning(QMessageBox(),'Algo deu errado!','Não foi possivel atualizar!')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Algo deu errado!")
            msg.setText("Não foi possivel atualizar os dados!")
            msg.exec()

    
    def limpar_campos(self):
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
    

    def consultar(self):
        db = Lite_db('mananger.db')
        valor_consulta = ''
        valor_consulta = self.lineEdit.text()

        lista = db.pega_dados(f'''SELECT * FROM funcs WHERE nome 
        like "%{valor_consulta}%" or documento like "%{valor_consulta}%"''')

        lista = list(lista)

        if not lista:
            #return QMessageBox.warning(QMessageBox(),'Atenção!','Usuário não tem cadastro!')

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Atenção!")
            msg.setText("Usuário não tem cadastro!")
            msg.exec()
        
        else:
            self.tableWidget.setRowCount(0)
            
            for idxLinha, linha in enumerate(lista):
                self.tableWidget.insertRow(idxLinha)
                for idxColuna, coluna in enumerate(linha):
                    self.tableWidget.setItem(idxLinha,idxColuna,QTableWidgetItem(str(coluna)))
        
   

   
    def carrega_dados(self):
        db = Lite_db('mananger.db')
        lista = db.pega_dados("SELECT * FROM funcs")

        self.tableWidget.setRowCount(0)
        for linha, dados in enumerate(lista):
            self.tableWidget.insertRow(linha)
            for coluna_n, dados in enumerate(dados):
                self.tableWidget.setItem(linha,coluna_n,QTableWidgetItem(str(dados)))
        


class Pesquisar(QDialog,Ui_consulta):
    def __init__(self):
        super(Pesquisar,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Consultar usuários')
        self.pushButton.clicked.connect(self.consultar)

    def consultar(self):
        db = Lite_db('mananger.db')
        valor_consulta = ''
        valor_consulta = self.lineEdit.text()

        lista = db.pega_dados(f'''SELECT * FROM funcs WHERE nome 
        like "%{valor_consulta}%" or documento like "%{valor_consulta}%"''')

        lista = list(lista)

        if not lista:
            #return QMessageBox.warning(QMessageBox(),'Atenção!','Usuário não tem cadastro!')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Atenção!")
            msg.setText("Usuário não tem cadastro!")
            msg.exec()
        
        else:
            self.tableWidget.setRowCount(0)
            
            for idxLinha, linha in enumerate(lista):
                self.tableWidget.insertRow(idxLinha)
                for idxColuna, coluna in enumerate(linha):
                    self.tableWidget.setItem(idxLinha,idxColuna,QTableWidgetItem(str(coluna)))
        



class Tela_principal(QMainWindow,Ui_inicial):
    def __init__(self,tela_login,logado):
        super(Tela_principal,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Usuários')
        self.tela_login = tela_login
        
        self.actionCadastrar.triggered.connect(self.add)
        self.carrega_dados()
        self.actionRefresh.triggered.connect(self.carrega_dados)
        self.actionAtualizar.triggered.connect(self.atualizar)
        self.actionProcurar.triggered.connect(self.pesquisar)
        self.actionApagar.triggered.connect(self.apagar_cadastro)
        self.user_logado = logado
        self.label.setText(self.user_logado)

        
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Alerta!',
                                     "Tem certeza que deseja sair?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.tela_login.show()
            self.clearMask()
            self.destroy()
        else:
            event.ignore()
        
        
    

    def carrega_dados(self):
        db = Lite_db('mananger.db')
        lista = db.pega_dados("SELECT * FROM funcs")

        self.tableWidget.setRowCount(0)
        for linha, dados in enumerate(lista):
            self.tableWidget.insertRow(linha)
            for coluna_n, dados in enumerate(dados):
                self.tableWidget.setItem(linha,coluna_n,QTableWidgetItem(str(dados)))
        

    def add(self):
        tela = Cadastrar()
        tela.exec()


    def pesquisar(self):
        pesquisar = Pesquisar()
        pesquisar.exec()

    def atualizar(self):
        atualizar = Atualizar()
        atualizar.exec() 
    
    def pega_selecao_banco(self):
        return self.tableWidget.currentRow()
        
    
    def pega_selecao_tabela(self):
        valor = self.tableWidget.item(self.pega_selecao_banco(),0)
        return valor.text() 
   
   
   
    def apagar_cadastro(self):
        try:
            db = Lite_db('mananger.db')
            id = self.pega_selecao_tabela()
            db.inserir_apaga_atualiza(f'DELETE FROM funcs WHERE id = "{id}"')
            #QMessageBox.information(QMessageBox(),'Você Perdeu!','Dados deletados!')
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Você Removeu!")
            msg.setText("Dados deletados com sucesso")
            msg.exec()
            self.carrega_dados()
       
        except:
            #QMessageBox.warning(QMessageBox(),'Algo deu errado!','Não foi possivel deletar!')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Algo deu errado!")
            msg.setText("Não foi possivel deletar os dados!")
            msg.exec()
    
              


class Login(QDialog,Ui_login):
    def __init__(self):
        super(Login,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Sistema de cadastro')

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.sair)


    def login(self):
        db = Lite_db('mananger.db')
        
        user = self.lineEdit.text()
        passw = self.lineEdit_2.text()

        if user == '' or passw =='':
            #QMessageBox.warning(QMessageBox(),'Alerta!','Preencha todos os campos!')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Alerta!")
            msg.setText("Preencha todos os campos!")
            msg.exec()
        
        else:
            dados = db.pega_dados(f'''SELECT acesso FROM users WHERE username = "{user}"
            and password = "{passw}"''')

            if dados:
                self.logado = user
                #QMessageBox.information(QMessageBox(),'login realizado!','ENTROU COM SUCESSO!')
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Login Realizado!")
                msg.setText("Login Realizado com sucesso!")
                msg.exec()

                self.window = Tela_principal(self,self.logado)
                self.window.show()
                window.close()
            else:
                #QMessageBox.warning(QMessageBox(),'login errado!','NÃO ENTROU COM SUCESSO!')
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Login errado!")
                msg.setText("Não logado com sucesso!")
                msg.exec()

    def sair(self):
        self.close()







if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec()