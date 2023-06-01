#!/usr/bin/env python3
import asyncio
from tcp import Servidor
import Mensagens_Protocolo as SF

'''
def validar_nome(nome):
    return re.match(br'^[a-zA-Z][a-zA-Z0-9_-]*$', nome) is not None


def sair(conexao):
    print(conexao, 'conexão fechada')
    conexao.fechar()


def dados_recebidos(conexao, dados):
    if dados == b'':
        return sair(conexao)

    print(conexao, dados)
    passo1(conexao, dados)


def conexao_aceita(conexao):
    print(conexao, 'nova conexão')
    conexao.registrar_recebedor(dados_recebidos)
'''

servidor = Servidor(6667)
servidor.registrar_monitor_de_conexoes_aceitas(SF.conexao_aceita)
asyncio.get_event_loop().run_forever()
