from flask import Flask
from flask import request
from datetime import datetime
import pika

import os
import logging

import newrelic.agent

# Initialize the New Relic agent
# Make sure to call this at the start of your application
newrelic.agent.initialize()

log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

app = Flask(__name__)

shard = os.environ.get('SHARD', "SHARD_NOT_SET")
ecs_cmd = os.environ.get("ECS_CONTAINER_METADATA_URI_V4", "NOT_SET")
queue_name = os.environ.get('QUEUE', "hello")
rmq_host = os.environ.get('RMQ_HOST', "[HOST NOT SET")

def logit(message):
    timeString = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log.info(timeString + " - [world: " + shard + "] - " + message)
    # print(timeString + " - [world: " + shard + "] - " + message)


@app.route("/")
def world():
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    log_message = {"message": "Hello World"}
    context = newrelic.agent.get_linking_metadata()
    log_message.update(context)
    logit(str(log_message))
    channel.basic_publish(exchange='', routing_key='hello', body=str(log_message))
    logit("SHARD: " + shard )
    return "World (" + shard + "), ECS_CONTAINER_METADATA_URI_V4: " + ecs_cmd
