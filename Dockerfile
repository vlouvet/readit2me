FROM python:3.8-slim

# set working directory
WORKDIR /app

# add and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . /app

# set secret key as an environment variable
ENV SECRET_KEY=supersecretORISIT

# create a volume to store the SQLite database file
VOLUME /app/database

# run server
CMD ["python", "app.py"]
