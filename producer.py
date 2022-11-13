import pika

parameters = pika.URLParameters('amqps://qsvvrqtm:XCvydaLcdvhxgwOUKjXAfviC3G30nK8f@woodpecker.rmq.cloudamqp.com/qsvvrqtm')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='marcacao-ponto', durable=True)

i = 1

for i in range(5000):
    x = "Mensagem número " + str(i)

    channel.basic_publish(exchange='',
                        routing_key='marcacao-ponto',
                        body=x)
    print(" [x] Enviado " + x)


connection.close()