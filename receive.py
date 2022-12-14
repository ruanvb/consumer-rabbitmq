#consumer de mensagens do RabbitMQ

#imports
from config import rabbitmq_server, sistema_legado

import os
import sys
import time
import pika
import requests
import json


def main():
    #parâmetros da url para conexão
    parameters = pika.URLParameters(rabbitmq_server["url_connection"])
    connection = pika.BlockingConnection(parameters)
    
    #canal de conexão
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_server["queue"], durable=True)

    #responsável por consumir as mensagens
    def callback(ch, method, properties, body):
        print( " [*] Recebido %r" % body.decode())
        time.sleep(body.count( b'.' ))
        data = body.decode()

        #Request API Legado
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(sistema_legado["url_api"], data=json.dumps(data), headers=headers)
        
        #simula tempo de resposta da API - segundo orientações do Desafio
        #foram utilizados 9 segundos para simular, pois naturalmente a execução já demora em torno de 1 segundo
        #entretanto, o código abaixo ficará comentado, pois como a estrutura de consumers disponibilizada
        #não atende a necessidade atual, para os testes é ideal que não seja considerado o tempo de resposta da API
        #time.sleep(9)
        print(r.json())

        #trata mensagem de retorno
        if(r.status_code == 200):
            #caso sucesso, confirma recebimento
            ch.basic_ack(delivery_tag = method.delivery_tag)
        else:
            #caso erro, permanece mensagem na fila até que seja tratada novamente
            ch.basic_nack(delivery_tag = method.delivery_tag)

    #- Define o tratamento de 1 mensagem por vez, lidas pelos consumers
    #-- A definição correta dependerá de quantos consumers estarão ativos
    #--- Por exemplo, se fosse utilizado apenas um consumer, o número poderia ser maior, mas não seria o ideal.
    #--- Caso fossem utilizados 1000 consumers, o ideal é que fosse realizada uma análise da volumetria, para 
    #--- que desa forma fosse realizado um cálculo balanceado, sem que sobrecarregue um consumer e sem que um
    #--- consumer fique ocioso.
    channel.basic_qos(prefetch_count=1)

    #consome mensagens
    channel.basic_consume(queue=rabbitmq_server["queue"],
                        on_message_callback=callback)

    print(' [*] Aguardando mensagens')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)