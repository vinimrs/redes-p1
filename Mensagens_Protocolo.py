import re
from passos.passo1 import passo1


def validar_nome(nome):
    return re.match(br'^[a-zA-Z][a-zA-Z0-9_-]*$', nome) is not None


def sair(conexao):
    print(conexao, 'conexão fechada')
    conexao.fechar()


def dados_recebidos(conexao, dados):
    if dados == b'':
        return sair(conexao)

    passo1(conexao, dados)
    print(conexao, dados)


def conexao_aceita(conexao):
    print(conexao, 'nova conexão')
    conexao.registrar_recebedor(dados_recebidos)
