"""
based on https://github.com/vjrantal/iot-edge-darknet-module/blob/master/module.py

Example of decoding the base 64-encoded output image stream:
    # Load json payload
    input_data = json.loads(input_data)['image_data']
    # Remove unnecessary characters (extra quotes etc.)
    input_data = ''.join(list(input_data)[2:-1])
    # Convert image from base64 string to int
    input_data = base64.b64decode(bytes(input_data, 'utf-8'))
"""


import os
import numpy as np
import json
import time
import base64
import glob

from sender import Sender

# This environment variable is set when the module is started by the
# IoT Edge runtime
IS_EDGE = os.getenv('IOTEDGE_MODULEID', False)

if IS_EDGE:
    sender = Sender()
else:
    sender = False

img_arry = []
img_files = glob.glob(os.path.join(os.getcwd(), 'data', '*.jpg'))
num_imgs = len(img_files)
for imgf in img_files:
    with open(imgf, 'rb') as fh:
        encoded_str = str(base64.b64encode(fh.read()))
        img_arry.append(encoded_str)

while True:
    # Choose one image at random
    rand_num = np.random.randint(low=0, high=num_imgs)
    filename = img_files[rand_num]
    encoded_str = img_arry[rand_num]

    # The json that will become the payload
    result = {'image_data': encoded_str, 'filename': os.path.basename(filename)}

    # print(json.dumps(result, indent=4))

    if sender:
        msg_properties = {
        }
        json_formatted = json.dumps(result)
        sender.send_event_to_output('imageData', json_formatted, msg_properties, 0)

    # To avoid sending too frequently on hardware where detection is fast
    time.sleep(1)

# This stdout print is currently checked in the Travis CI script exactly
# as it is so pay attention if changing it
print('Program exiting normally')
