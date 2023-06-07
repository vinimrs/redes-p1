import re
from scripts.Message_Handler import Message_Handler
from passos.passo1 import passo1


# def validar_nome(nome):
#     return re.match(br'^[a-zA-Z][a-zA-Z0-9_-]*$', nome) is not None


# def sair(conexao):
#     print(conexao, 'conexão fechada')
#     conexao.fechar()


# _dados_residuais = ''
# def dados_recebidos(conexao, dados):
#     if dados == b'':
#         return sair(conexao)
    
#     mensagens = []
#     if not dados.endswith(b'\r\n'):
#         # Dividir os dados em substrings e filtrar strings vazias
#         #dados = list(filter(bool, dados.split(b'\r\n')))
#         lines = _dados_residuais + dados
#         mensagens = lines.split(b'\r\n')
    
#         # Armazenar os dados residuais para uso posterior
#         _dados_residuais += mensagens.pop(-1)

#     # Dividir os dados restantes em mensagens individuais e filtrar strings vazias
#     #mensagens = list(filter(bool, dados.split(b'\r\n')))

#     # Processar cada mensagem separadamente
#     for mensagem in mensagens:
#         print(mensagem)
#         Message_Handler(conexao, mensagem)
#         # request, info = mensagem.split(b' ', 1)
#         # # Realizar o processamento necessário para cada mensagem

#         # if request.upper() == b'PING': 
#         #     conexao.enviar(b':server PONG server :' + info + b'\r\n')

#     print(conexao, dados)


# def conexao_aceita(conexao):
#     print(conexao, 'nova conexão')
#     conexao.registrar_recebedor(dados_recebidos)
