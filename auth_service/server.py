import datetime
import jwt
import os
from flask import Flask, request
from flask_mysqldb import MySQL
from logging.config import dictConfig

# Logging Configurations
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

server = Flask(__name__)
mysql = MySQL(server)

'''server config'''

# Auth DB Configurations - Fed by Kubernetes configMap and secret yaml files
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))

# Routes (Endpoints)
@server.route("/login", methods=["POST"])
def login():
    # Credentials for a 'Basic Authentication' header as provided by request package
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    # Check DB for username and password provided, use cursor from flask mysql conn to interact with DB
    try:
        cursor = mysql.connection.cursor()
        result = cursor.execute(
            "SELECT email, password FROM user WHERE email=%s", (auth.username,)
        )
    except Exception as mysqlex:
        server.logger.error(f'Could not connect to MySQL server, stack: {mysqlex}')
        return "connection error", 401

    if result > 0:
        user_row = cursor.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    # User doesn't exist in DB, user doesn't have access
    else:
        return "invalid credentials", 401


# Route validates the JWT passed, which basically checks the JWT was encoded with the right secret
# Or in our case, encoded with the right secret in the method createJWT below.
@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    # Not validating the type of the authentication scheme, skipping for brevity's sake
    # Bearer [space] token_value
    encoded_jwt = encoded_jwt.split(' ')[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "not authorized", 403

    return decoded, 200


'''authz tells us whether the user is an allowed entity or not (admin role in the example),
   hence it can call our endpoints'''
def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
        },
        # To be used for the symmetric encoding algorithm - Keeping auth simple (basic for illustrative purposes)
        secret,
        algorithm="HS256",
    )


if __name__ == "__main__":
    '''
    Listen on all public ips by using 0.0.0.0, which means enable docker container's assigned ip (which changes) 
    - see Flask framework docs: http://flask.parallelprojects.com
    '''
    server.run(host="0.0.0.0", port=5000)
