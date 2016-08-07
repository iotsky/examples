import requests

__doc__ = """
   You can use this sample script to publish json data to the broker endpoint via a REST endpoint.
   Use the mqtt sample subscriber to receive this data on a different window.

   The endpoint is of the form:
      https://A1QA5YMMGWQ50B.iot.us-west-2.amazonaws.com:8443/topics/<UR TOPIC FROM THE IOTSKY PROJECT PAGE>/<SOME TOPIC NAME>?qos=1
"""

# NOTE: Fill appropriate values here based on your project
IOTSKY_ENDPOINT = 'https://A1QA5YMMGWQ50B.iot.us-west-2.amazonaws.com:8443/topics/<UR TOPIC FROM THE IOTSKY PROJECT PAGE>/foo?qos=1'
IOTSKY_PROJECT_CERT_FILE = '/path/to/ur/restCert.pem'
IOTSKY_PROJECT_PRIVATE_KEY_FILE = '/path/to/ur/restPrivateKey.pem'


def main():
    response = requests.post(IOTSKY_ENDPOINT, cert=(IOTSKY_PROJECT_CERT_FILE, IOTSKY_PROJECT_PRIVATE_KEY_FILE), data={"temp": 21})
    print response.status_code
    print response.content

if __name__ == '__main__':
    main()

