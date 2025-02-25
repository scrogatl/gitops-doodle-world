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
    # Setup RabbitMQ
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    
    # Get dt headers from New Relic
    log_message = {"message": "sent from doodle-world"}
    context = newrelic.agent.get_linking_metadata()
    
    # Tell someone about it
    log_message.update(context)
    logit(str(log_message))
    
    # Publish to RabbitMQ
    channel.basic_publish(exchange='', routing_key=queue_name, body=str(log_message))
    
    return "World (" + shard + "), ECS_CONTAINER_METADATA_URI_V4: " + ecs_cmd
