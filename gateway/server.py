# gridfs for storing files in mongo (blobs-like but in Mongo), pika for interacting with RabbitMQ
import gridfs, pika, json, os

from flask import Flask, request, send_file
from flask_pymongo import PyMongo

# Project's packages - To be created
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

server = Flask(__name__)

VIDEOS_COLLECTION = "videos"
MP3S_COLLECTION = "mp3s"
MONGO_DB_URL = "mongodb-nodeport-svc.default.svc.cluster.local:27017"

# GridFS will store files larger than 16mb by splitting them into chunks or parts (of around 255kb each)
mongodb_uri_videos = "mongodb://" + f'{os.environ.get("MONGO_USER")}' + ":" + f'{os.environ.get("MONGO_PASS")}' + "@" + \
    MONGO_DB_URL + f"/{VIDEOS_COLLECTION}?authSource=admin&retryWrites=true&w=majority"
mongodb_uri_mp3s = "mongodb://" + f'{os.environ.get("MONGO_USER")}' + ":" + f'{os.environ.get("MONGO_PASS")}' + "@" + \
    MONGO_DB_URL + f"/{MP3S_COLLECTION}?authSource=admin&retryWrites=true&w=majority"

mongo_video = PyMongo(server, uri=f"{mongodb_uri_videos}")
mongo_mp3 = PyMongo(server, uri=f"{mongodb_uri_mp3s}")

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

# Configures RabbitMQ connection - rabbitmq is the name for the kubernetes statefulSet used for it.
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


# Endpoints

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def upload():
    # Validate user's token upon doing an action in the Product, upload action specifically here.
    json_info, err = validate_token(request)

    if err:
        server.logger.error(f"Error occurred during authorization process: {err}")
        return err

    if json_info["admin"]:
        # Allows for uploading one file per request
        if len(request.files) > 1 or len(request.files) < 1:
            return "Exactly one file required", 400

        for _, file_value in request.files.items():
            err = util.upload(file_value, fs_videos, channel, json_info)
            if err:
                server.logger.error(f"Error while uploading the file: {err}")
                return err

        return "Success", 200
    else:
        return "Not Authorized", 401


# Endpoint to download the video's audio
@server.route("/download", methods=["GET"])
def download():
    # Validate user's token upon doing an action in the Product, upload action specifically here.
    json_info, err = validate_token(request)

    if err:
        server.logger.error(f"Error occurred during authorization process: {err}")
        return err

    if json_info["admin"]:
        # Parameter send in the request to identify the unique file to download when conversion happened.
        fid_string = request.args.get("fid")

        if not fid_string:
            server.logger.error(f"Could not find required request parameter for file id in: {json_info}")
            return "fid is required", 400

        try:
            server.logger.info(f"Attempting to retrieve MP3 file from MongoDB database ...")
            mp3_file = fs_mp3s.get(ObjectId(fid_string))
            # send_file returns back to the requester the download action
            return send_file(mp3_file, download_name=f'{fid_string}.mp3')
        except Exception as err:
            server.logger.error(f"Error during operation to retrieve file from MongoDB, as: {err}")
            return "Internal Server Error", 500

    return "User not authorized", 401


def validate_token(auth_request):
    json_info, err = validate.token(auth_request)
    server.logger.info(f"Result of token validation process: {json_info}")

    if err:
        server.logger.error(f"An Error occurred while validating token: {err}")
        server.logger.error(f"JSON information received: {json_info}")

    # Parse response into JSON dictionary
    json_info = json.loads(json_info)
    return json_info, err


if __name__ == "__main__":
    server.logger.info("Starting up Gateway Service ...")
    '''
    Listen on all public ips by using 0.0.0.0, which means enable docker container's assigned ip (which changes) 
    - see Flask framework docs: http://flask.parallelprojects.com
    '''
    server.run(host="0.0.0.0", port=8080)
    server.logger.info("Shutting down Gateway Service ...")
