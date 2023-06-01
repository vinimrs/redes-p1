'''
Você recebeu um arquivo de exemplo chamado servidor que escuta na porta 6667 e mostra na saída todas as conexões estabelecidas, dados recebidos e conexões fechadas.
Estude o código contido no arquivo tcp.py para entender como o servidor utiliza os recursos do sistema operacional e da linguagem Python.
Complete o código do servidor para tratar mensagens do tipo PING recebidas do cliente e respondê-las corretamente.
'''


def passo1(conexao, dados):
    conexao.enviar(b':server PONG server :' + dados.split(b' ', 1)[1])
