def passo1(conexao, dados):
    conexao.enviar(b':server PONG server :' + dados.split(b' ', 1)[1])
