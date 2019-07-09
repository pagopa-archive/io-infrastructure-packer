# IO (Digital Citizenship) infrastructure Packer scripts

The repository contains the Packer and Ansible scripts used to create, provision and maintain the IO VMs base images.

## What is IO?

More informations about the IO can be found on the [Digital Transformation Team website](https://teamdigitale.governo.it/en/projects/digital-citizenship.htm)

## Repository structure

io-infrastructure-packer
|_ template-xxx.json (the Packer templates)
|_ ...
|_ ansible
    |_ playbook-xxx.yml (the Ansible playbooks used by the Packer templates)
    |_ ...
    |_ roles (the Ansible roles used by the playbooks)
|_ .circleci (contains the circleCI configs)
|_ helpers (the directory containing the helper tools)
    |_ xxx.py
    |_ ...
    |_ docker (contains the docker-compose file and dockerfiles to build locally the CI/CD repos - used to test builds manually)

## Prerequisites

The following requisites should be satisfied before being able to use Packer.

### Install Packer

Instructions to install Packer are available [here](https://www.packer.io/intro/getting-started/install.html).

Before moving forward make sure that the *packer* command is available at the CLI.

### Initialize the Azure environment and export the environment variables

Before building images you should setup your Azure target environment and export the environment variables that Packer will read.

The init and export scripts are available in the [utils folder of the io-infrastructure-live repo](https://github.com/teamdigitale/io-infrastructure-live).

## How to build an image

Once the environment variables have been setup you can now build and ship images to Azure. To build an image, simply run the command

```shell
packer build TEMPLATE.json
```

Templates are JSON files within the root directory of the repository.

## Azure image versioning

When images change, the version should be always incremented. The image name format is as following:

```
IMAGE_NAME-IMAGE-VERSION
```

For example

```
base-0.1
```

Unfortunately, Azure doesn't allow the use of ":" in the image name. As such, it cannot be used as a separator between the image name and the version.

## Builds and dependencies

Builds are triggered automatically on the CI/CD engine every time certain files of the repository are pushed.
Some Python scripts are run at each CI build. These scripts automatically understand dependencies between Packer templates, Ansible playbooks and roles, so understanding what templates should be built, depending on the changes came in with the last commit.

## The base image

The *base.json* file is a template used to create a "special base image", called base-X.X (where X.X represents the base image version). Base image should be the only image -as now- to be created from an official Azure base image. All other images should be created from this image.

## Ansible configuratoin playbooks

Ansible is used to provision software and configurations on images created by Packer. The repository contains an *ansible* directory with different playbooks that call roles defined in the roles directory. Playbooks should always call roles and never run tasks directly.

## How to contribute

Contributions are welcome. Feel free to open issues and submit a pull request at any time!
