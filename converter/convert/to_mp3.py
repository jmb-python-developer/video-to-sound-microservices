import logging

import pika
import json
import tempfile
import os
import moviepy.editor

from bson.objectid import ObjectId


def start(message, fs_videos, fs_mp3s, channel):
    # Get queue's message contents into a JSON object
    logging.debug(f"Loading message from channel {channel}")
    message = json.loads(message)

    # Create temp file for writing video contents to it
    logging.debug("Writing temporary video file to local filesystem")
    tf = tempfile.NamedTemporaryFile()

    # Video contents, uses id property as sent by the gateway service while persisting the video to mongo ("video_fid")
    out = fs_videos.get(ObjectId(message["video_fid"]))

    # Add the video contents to the empty temporary file
    tf.write(out.read())

    # Convert video file to audio mp3
    logging.debug("Converting video to mp3 ... ")
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    # Write audio to temp file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    logging.debug(f"Writing out MP3 Audio file to temporary file with path and name: {tf_path}")
    audio.write_audiofile(tf_path)

    # Save to Mongo
    logging.debug("Saving Audio file to MongoDB ")
    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    # Free the volume from the temp file
    os.remove(tf_path)
    logging.debug("Successfully saved audio file to MongoDB")

    # Finally, put a message in the relevant queue for the Notification service (consumer) to pick and process.
    message["mp3_fid"] = str(fid)

    logging.debug("Publishing message to 'mp3' queue")
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        # If message was not put in queue, then delete the mp3 from mongo
        fs_mp3s.delete(fid)
        logging.error(f"An error occured: {err}")
        return "Failed to publish message to notifications queue"

    logging.debug("Successfully published message to 'mp3' queue")



