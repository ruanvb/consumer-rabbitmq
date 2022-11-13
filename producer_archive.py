import json

import pika

parameters = pika.URLParameters('amqps://qsvvrqtm:XCvydaLcdvhxgwOUKjXAfviC3G30nK8f@woodpecker.rmq.cloudamqp.com/qsvvrqtm')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='marcacao-ponto', durable=True)

arquivo = open('arquivo_marcacoes.txt')

for linha in arquivo:
    
    data = linha[12:22]
    hora = linha[22:29]
    employeeId = linha[0:6]
    employerId = linha[6:12]

    body = {
        "includedAt": data + " " + hora,
        "employeeId": employeeId, 
        "employerId": employerId
    }

    bodyJson = json.dumps(body)                   

    channel.basic_publish(exchange='',
                        routing_key='marcacao-ponto',
                        body=bodyJson)
    print(" [x] Enviado " + bodyJson)

arquivo.close()

connection.close()