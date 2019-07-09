# Dockerfile to emulate the CI/CD environment container

The `Dockerfile` provided is used to instantiate on a development environment (your laptop) the container used by the CI/CD environment used to deploy the images.

# Requirements

*docker-compose* should be installed before being able to bring up the environment.

# How to bring up the containers

These are the steps used to bring up the containers

## Export the Packer environment variables

Images built by Packer use some environment variables. These are mainly Azure secrets. Make sure you export all the environment variables needed.

For this, you may use the *az-export.sh* script in the [utils folder of the io-infrastructure-live repo](https://github.com/teamdigitale/io-infrastructure-live).

The Dockerfile uses the environment variables exported while creating the containers.

## Build the image

This should be done once, unless the image Dockerfile gets modified. To build the image use

```shell
docker-compose build
```

## Create the containers

To create the container use

```shell
docker-compose up -d
```

This will create two containers named docker_cicd-ubuntu_1 and docker_cicd-centos_1, and will run them in background.

## Access the container CLI

To access the containers' CLI use

```shell
docker exec -it docker_cicd-ubuntu_1 /bin/bash
```

or

```shell
docker exec -it docker_cicd-centos_1 /bin/bash
```

The containers mount by default the *io-infrastructure-packer* directory in *io-infrastructure-packer*, setting that as the default working directory.

You can now run all the commands needed.

## Stop and remove the containers

To stop and remove the running containers use

```
docker-compose kill
```
