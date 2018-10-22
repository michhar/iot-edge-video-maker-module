# Video Simluator IoT Edge Module

An Azure IoT  Edge module to simulate a stream of images or video feed.

## Prerequisites

1.  Docker (Community Edition) for Mac or Windows
2.  Visual Studio Code (VSCode) text editor with IoT Edge extension (to get this go to View -> Extensions and type in "IoT Edge", select "Azure IoT Edge") - alternatively all of the work may be done on the command line as is shown in [this tutorial](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart-linux).
3.  Azure IoT Hub resource
4.  Azure IoT Edge Device in said Hub

## Setup

Clone this repository.

Create a file, `.env`, at the base of this repo (note the `.`).  Place the following environment variables in it, using the proper container registry information, as in:

```text
CONTAINER_REGISTRY_USERNAME=<azure container registry user name>
CONTAINER_REGISTRY_PASSWORD=<azure container registry password>
CONTAINER_REGISTRY_ADDRESS=<azure container registry address
>
```

Open an integrated terminal window with VSCode (View -> Terminal).  Login in to Azure and add the container registry credentials.

`az login`

`az acr login --name <container registry name>`

Note:  Dockerhub may also be used.

## Build and Push Image

The first step is building a dependency, `azure-iot-sdk-python`.  Then, the deployment template will be used to build an image for the module and push it to the registry specified in the `.env` file.  Finally, a deployment manifest will be created.

1. CD into the `azure-iot-sdk-python` folder and run:
    
    `docker build -f azure-iot-sdk-python/Dockerfile -t wonderwoman/azure-iot-sdk-python .`

2.  Right click on the `deployment.template.json` in the base of the repository, and click "Build and Push IoT Edge Solution" (this should show up if the IoT Edge extension for VSCode has been installed).
3.  Right click on the same file and "Generate IoT Edge Deployment Manifest".  This should create a `config` folder with a file `deployment.json` inside of it.

## Deploy Solution

The above step will generate a `config` folder.  Right click on the `deployment.json` and select "Create Deployment for Single Device", then the device (if there is no device, create one in the IoT Hub).  The "localhost:5000" in the custom Module may need to be replaced with the cloud container registry name.

## Test Image Locally

In the integrated terminal in VSCode or elsewhere, start the container (you may need elevated priveledges as in `sudo` or use an admin terminal instead):

`docker run wonderwoman/edge-image-simulator-module`

And, then, enter into running container with a bash interface:

`docker exec -it [container-id] bash`

## Debugging

To view modules running on the device:

`iotedge list`

To get service logs for IoT Edge:

`journalctl -u iotedge`

To check that security deamon is running:

`systemctl status iotedge`

To restart IoT Edge security daemon:

`systemctl restart iotedge`

## For Reference

Set up a new project by following instructions here:  https://github.com/Azure/cookiecutter-azure-iot-edge-module
