import sys

import gridfs
import os
import pika
import logging

from convert import to_mp3
from pymongo import MongoClient

MONGO_DB_URL = "mongodb-nodeport-svc.default.svc.cluster.local:27017"


def main():
    mongo_db_authentication_url = "mongodb://" + f'{os.environ.get("MONGO_USER")}' + ":" + f'{os.environ.get("MONGO_PASS")}' + "@" + \
                                  MONGO_DB_URL
    client = MongoClient(mongo_db_authentication_url)
    # videos is the Doc from mongo where videos are persisted in gateway microservice
    db_videos = client.videos
    # Destination dir for converted videos into mp3s
    db_mp3s = client.mp3s

    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    def callback(ch, method, properties, body):
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        # if error, send negative acknowledgment to the channel, to keep the msg and re-process by other process.
        if err:
            logging.error("Error during message processing: " + err)
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            logging.info("Successfully processed message ")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # Rabbit MQ configs
    connection = pika.BlockingConnection(
        # K8s service name resolving to this host name
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()

    # Configs to consume messages from "video" queue.
    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"),
        # Callback function when a message is pulled off the queue
        on_message_callback=callback
    )

    logging.info("Waiting for messages to process. To terminate press CTRL + C ")

    # Starts consuming from RabbitMQ
    channel.start_consuming()


if __name__ == "__main__":
    try:
        logging.info("Starting RabbitMQ Consumer - Name: converter")
        main()
        logging.info("Shutting down RabbitMQ Consumer - Name: converter")
    except KeyboardInterrupt:
        print("Interrupted channel consumer")
        logging.warning("Keyboard interrupt was detected")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
