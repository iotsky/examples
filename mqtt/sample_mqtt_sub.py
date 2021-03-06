import paho.mqtt.client as mqtt
import ssl

__doc__ = """
    This is a sample script to subscribe to messages from an MQTT broker at AWS.
    You have to register first at iotsky.io and create a new project.

    Then start the subscriber on one terminal and publish from another.

    For more details visit iotsky.io

    Ensure that you have the paho mqtt client python lib installed. You can find it here:
     https://pypi.python.org/pypi/paho-mqtt/1.1
"""

connflag = False

# NOTE: Fill these with appropriate values
# url to the aws cert is located in the README
AWS_CERT_PATH = '/path/to/awsCert.pem'
IOTSKY_PROJECT_CERT_FILE = '/path/to/iotsky/project/cert.pem'
IOTSKY_PROJECT_PRIVATE_KEY_FILE = '/path/to/iotsky/project/private_key.pem'
# This will be displayed on the project details page on iotsky.io e.g.
# 9020198dd518778d384bebb123456789-my_project/*
IOTSKY_PROJECT_TOPIC = '9020198dd518778d384bebb123456789-my_project/foo'
CLIENT_ID_SUB = 'YOUR SUBSCRIBE CLIENT ID'


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print('Connected with result code {0}'.format(str(rc)))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    data = client.subscribe(IOTSKY_PROJECT_TOPIC)
    print 'data:'
    print data


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print('{0} {1}'.format(msg.topic, str(msg.payload)))


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print client
        print userdata
        print 'unexpected disconnection'


def on_log(client, userdata, level, buf):
    print level, buf


def main():
    client = mqtt.Client(client_id=CLIENT_ID_SUB)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_log = on_log

    client.tls_set(AWS_CERT_PATH, certfile=IOTSKY_PROJECT_CERT_FILE,
                   keyfile=IOTSKY_PROJECT_PRIVATE_KEY_FILE, tls_version=ssl.PROTOCOL_TLSv1_2,
                   ciphers='AES256-SHA256', cert_reqs=ssl.CERT_REQUIRED)
    client.connect("A1QA5YMMGWQ50B.iot.us-west-2.amazonaws.com", 8883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()


if __name__ == '__main__':
    main()
