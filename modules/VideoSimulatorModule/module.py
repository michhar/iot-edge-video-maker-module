# based on https://github.com/vjrantal/iot-edge-darknet-module/blob/master/module.py
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
for imgf in img_files:
    with open(imgf, 'rb') as fh:
        encoded_str = str(base64.b64encode(fh.read()))
        img_arry.append(encoded_str)

while True:
    # Choose one image at random
    encoded_str = img_arry[np.random.randint(low=0, high=2)]

    # The json that will become the payload
    result = {'image_data': encoded_str}

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
