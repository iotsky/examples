import paho.mqtt.client as mqtt
import ssl
from time import sleep

__doc__ = """
    This is a sample script to publish messages to an MQTT broker at AWS.
    You have to register first at iotsky.io and create a new project.

    Then start the subscriber on one terminal and publish from another.

    For more details visit iotsky.io
"""

connflag = False

# NOTE: Fill these with appropriate values
# url to the aws cert is located in the README
AWS_CERT_PATH = '/path/to/awsCert.pem'
IOTSKY_PROJECT_CERT_FILE = '/path/to/iotsky/project/cert.pem'
IOTSKY_PROJECT_PRIVATE_KEY_FILE = '/path/to/iotsky/project/private_key.pem'
# This will be displayed on the project page e.g.
# 9020198dd518778d384bebb123456789-my_project/*
IOTSKY_PROJECT_TOPIC = '9020198dd518778d384bebb123456789-my_project/foo'


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connected with result code {0}".format(str(rc)))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print('{0} {1}'.format(msg.topic, str(msg.payload)))


def on_disconnect(client, userdata, rc):
    print 'Disconnected with status: {0}'.format(rc)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.tls_set(AWS_CERT_PATH, certfile=IOTSKY_PROJECT_CERT_FILE,
               keyfile=IOTSKY_PROJECT_PRIVATE_KEY_FILE, tls_version=ssl.PROTOCOL_TLSv1_2,
               ciphers='AES256-SHA256', cert_reqs=ssl.CERT_REQUIRED)

client.connect("A1QA5YMMGWQ50B.iot.us-west-2.amazonaws.com", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client.loop_start()

while True:
    sleep(0.5)
    if connflag == True:
        data = 20
        client.publish(IOTSKY_PROJECT_TOPIC, data, qos=0)
        print("msg sent: data " + "%.2f" % data )
        sleep(1)
    else:
        print("waiting for connection...")

sleep(2)

