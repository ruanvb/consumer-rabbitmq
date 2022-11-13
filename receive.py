import os
import sys
import time

import pika
import requests
import json


def main():
    parameters = pika.URLParameters('amqps://qsvvrqtm:XCvydaLcdvhxgwOUKjXAfviC3G30nK8f@woodpecker.rmq.cloudamqp.com/qsvvrqtm')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='marcacao-ponto', durable=True)

    def callback(ch, method, properties, body):
        print( " [*] Recebido %r" % body.decode())
        time.sleep(body.count( b'.' ))

        url = "https://api.mockytonk.com/proxy/ab2198a3-cafd-49d5-8ace-baac64e72222"
        data = body.decode()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print(r.json())
        print(r.status_code)

        ch.basic_ack(delivery_tag = method.delivery_tag)
        #ch.basic_nack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='marcacao-ponto',
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