# Base image
FROM python:3.10-slim-bullseye

# Install host dependencies and bins
RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential \
  && pip install --no-cache-dir --upgrade pip

# Create workdir and copy needed dependencies files for pip (requirements.txt) and the whole dir, which has server.py
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

# Expose this port just like in our Flask server config
EXPOSE 8080

# Finally run the authentication servicels
CMD ["python3", "server.py"]