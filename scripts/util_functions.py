import re
# -----------------------------------------------------------------#
def validar_nome(nome):
    return re.match(br'^[a-zA-Z][a-zA-Z0-9_-]*$', nome) is not None
# -----------------------------------------------------------------#
def sair(conexao):
    print(conexao, 'conexão fechada')
    conexao.fechar()
# -----------------------------------------------------------------#
