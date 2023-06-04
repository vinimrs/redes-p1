"""
## Passo 2

Um erro muito comum de pessoas que estão começando a trabalhar com *sockets* é acreditar que uma mensagem sempre vai ser transportada de
 uma só vez de uma ponta até a outra. Essa situação ideal pode até persistir enquanto você estiver testando seu programa localmente, 
 mas quando ele estiver funcionando em uma rede real, duas situações eventualmente acontecerão:

 * Uma mensagem do tipo `"linha\r\n"` pode ser quebrada em várias partes. Por exemplo, podemos receber primeiro `"lin"`, depois `"h"`
   e depois `"a\r\n"`.
    
 * Duas ou mais mensagens podem ser recebidas de uma só vez. Por exemplo, podemos receber `"linha 1\r\nlinha 2\r\nlinha 3\r\n"`.

As duas coisas também podem acontecer ao mesmo tempo. Podemos receber, por exemplo, algo do tipo `"a 1\r\nlinha 2\r\nli"`.

Adapte seu servidor para tratar situações similares às descritas acima. Você deve cortar os dados recebidos nas quebras de linha e 
tratar múltiplas mensagens sempre que várias mensagens forem recebidas de uma vez só. Sempre que os dados recebidos não terminarem em 
um fim de linha, você deve armazenar os "dados residuais" para juntar com os dados que serão recebidos na próxima vez que a função for chamada.
 Recomendamos que você armazene os "dados residuais" com um atributo do próprio objeto `conexao`.

Por enquanto, continuaremos enviando apenas mensagens do tipo `PING`, mas tente deixar seu código organizado para implementar o tratamento de
 novos tipos de mensagem, que serão necessárias nos passos seguintes.
"""

def passo2(conexao, dados):

    if not dados.endswith(b'\r\n'):
        # Dividir os dados em substrings e filtrar strings vazias
        dados = list(filter(bool, dados.split(b'\r\n')))
    
        # Armazenar os dados residuais para uso posterior
        conexao.dados_residuais += dados.pop(-1)

    # Dividir os dados restantes em mensagens individuais e filtrar strings vazias
    mensagens = list(filter(bool, dados.split(b'\r\n')))

    # Processar cada mensagem separadamente
    for mensagem in mensagens:
        request, info = mensagem.split(b' ', 1)
        # Realizar o processamento necessário para cada mensagem

        if request.upper() == b'PING': 
            conexao.enviar(b':server PONG server :' + info + b'\r\n')

