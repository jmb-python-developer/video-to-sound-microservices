import pika, json, logging

'''
Function does the following
1- Upload file to MongoDB database, using GridFS, which returns a unique file id from Mongo GridFS.
2- Put message in RabbitMQ queue for a downstream service to process the upload by pulling it from Mongo
'''


def upload(file, fs, channel, json_info):
    try:
        fid = fs.put(file)
    except Exception as error:
        logging.error(f"Error occurred while pushing file to MongoDB GridFS: {error}")
        return "Internal Server Error", 500

    # If no errors, put message into queue for the operation
    message = {
        "video_fid": str(fid),
        # Set by a downstream service in charge of the conversion
        "mp3_fid": None,
        "username": json_info["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",  # Actual queue name
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE # Make queue messages durable, in case of crashes
            ),
        )
    except Exception as mq_error:
        logging.error(f"Error while pushing conversion message to RabbitMQ: {mq_error}")
        # If errors while putting the message for downstream services, delete the file first
        fs.delete(fid)
        return "Internal Server Error", 500
