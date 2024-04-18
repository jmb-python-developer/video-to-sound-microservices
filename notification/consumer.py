import sys
import os
import pika
import logging

from send import email

'''
This is a Consumer type of service, which consumes messages from RabbitMQ broker, mp3s queue, detecting this way newly
converted video files into mp3 files. 
'''


def main():
    # Rabbit MQ configs
    connection = pika.BlockingConnection(
        # K8s service name resolving to this host name
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()

    def callback(ch, method, properties, body):
        # Send an email to the user that uploaded the video for conversion with the mp3_fid of the mp3 file to download.
        err = email.notification(body)
        # if error, send negative acknowledgment to the channel, to keep the msg and re-process by other process.
        if err:
            logging.error("Error during message processing: " + err)
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            logging.info("Successfully processed message ")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # Configs to consume messages from "MP3" queue.
    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE"),
        # Callback function when a message is pulled off the queue, defined above.
        on_message_callback=callback
    )

    logging.info("Waiting for messages to process. To terminate press CTRL + C ")

    # Starts consuming from RabbitMQ
    channel.start_consuming()


if __name__ == "__main__":
    try:
        logging.info("Starting RabbitMQ Consumer - Name: notification service")
        main()
        logging.info("Shutting down RabbitMQ Consumer - Name: notification service")
    except KeyboardInterrupt:
        print("Interrupted channel consumer")
        logging.warning("Keyboard interrupt was detected")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
