'''
Implemente suporte a troca de mensagens entre usuários usando PRIVMSG.
O seu código só vai passar no teste se você estiver acompanhando corretamente a troca de apelidos e direcionando as mensagens à conexão correta.
Ignore mensagens enviadas para apelidos que não existem ou que não estão mais em uso.
'''
from Mensagens_Protocolo import validar_nome

# Placeholder p/ estrutura de dados para apelidos
nicknames = []

def PRIVMSG_Handler(conexao, mensagem):
    # Pegar o nick do sender
    sender = nicknames[conexao.s]
    # Pegar o nick do receiver (Na mensagem)
    receiver = mensagem.split(maxsplit=2)[1]
    # (Passo 6) verificar se o receiver é um canal
    # Garantir que o nick do receiver é válido
    if(validar_nome(receiver) is False):
        return
    # Comparar com o dicionário de nicks
    if(nicknames[receiver] is None):
        return
    # Enviar mensagem
    conexao.enviar(b':' + sender + b' PRIVMSG ' + receiver + b' :' + mensagem.split(maxsplit=2)[2])
    return 