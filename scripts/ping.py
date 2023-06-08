# -----------------------------------------------------------------#
def PING_handler(conexao, dados):
    return conexao, b':server PONG server :' + dados.split(b' ', 1)[1] + b'\r\n'
    # print('respondendo PING com PONG')
    # print(conexao, dados)
# -----------------------------------------------------------------#