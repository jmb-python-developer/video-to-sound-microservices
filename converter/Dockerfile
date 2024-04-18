# Base image
FROM python:3.10-slim-bullseye

# Install host dependencies and bins
RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential ffmpeg \
  && pip install --no-cache-dir --upgrade pip

# Create workdir and copy needed dependencies files for pip (requirements.txt) and the whole dir, which has server.py
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

# Finally run the authentication servicels
CMD ["python3", "consumer.py"]
