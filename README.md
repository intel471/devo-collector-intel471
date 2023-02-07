&#x2B07;&#x2B07;&#x2B07;&#x2B07; REMOVE THIS SECTION &#x2B07;&#x2B07;&#x2B07;&#x2B07;

### How to use this template

> **DO NOT FORK THIS PROJECT** > Click on [![](https://img.shields.io/static/v1?label=&message=Use%20this%20template&color=2da44e&style=flat)](../../generate) button for creating a new repository using this one as template.

1. `CTRL` + [![](https://img.shields.io/static/v1?label=&message=Use%20this%20template&color=2da44e&style=flat)](../../generate) (to open a new tab)
1. Choose the proper `Owner`value
1. In the `Repository name` field set the name of the new repository to be created
1. Fill the `Description` field with the proper content (Optional)
1. Establish the desired visibility (`Public` or `Private`)
1. Its recomended to left unmarked the `Include all branches` check box
1. Click on `Create repository from template`
1. Fill `metadata.json` file with proper values. See below for details
1. Replace values in curly braces with the corresponding value
1. Remove this section

### How to fill `metadata.json`

This file is used to deploy the collector into our cloud service named Collector Server.

```json
{
  "title": "<vendor_name> <product_name> collector - Integrations Factory",
  "package_name": "<vendor_name>_<product_name>",
  "version": "1.0.0",
  "version_description": "<collector_description>",
  "labels": ["label_1", "label_1"],
  "collector_type": "continuous",
  "package_description": "The collector retrieves events information from blah, blah, blah",
  "owner": "aaa.bbb@domain.com",
  "allow_validation": "0"
}
```

1. `title`: name displayed into the Collector server
1. `package_name`: name of the generated Docker image
1. `version`: version of the generated Docker image
1. `version_description`: a little description about this particular version
1. `labes`: fields related to the collector
1. `collector_type`: this field will be used by the Collector Server. Leave it as it is
1. `package_description`: a general description of the collector
1. `owner`: leaver your email address here
1. `allow_validation`: leave it as it is for the moment

&#x2B06;&#x2B06;&#x2B06;&#x2B06; REMOVE THIS SECTION &#x2B06;&#x2B06;&#x2B06;&#x2B06;

----
# {VendorName} {ProductName} collector for Devo Platform

![](https://img.shields.io/badge/language-Python-blue?style=flat)
![](https://img.shields.io/badge/devo--collector--sdk-%3D%3D1.6.1-blue?style=flat)

## Overview

A brief explanation of what this collector does

## Vendor Setup

This section will contain all the information required to have an environment ready to be collected, such as:
  * How to create an account
  * How to create the required setup in the environment
  * How to generate some data to be collected
  * How to create credentials (and also the required permissions)

## Minimal Configuration Required

This section will contain all the information required to have the collector instance running, such as:
  * Authentication info
  * List of existing services (remarking mandatory/optional parameters)

## Build and run the collector

### Collector execution during development

Although the final way of executing the data collector is using a Docker container, the data collector can be executed in a local non dockerized environment.

### Using terminal

```
python3 -m devocollectorsdk.main --config <config_filename>.yaml
```

### Using PyCharm

This is a screenshot of a running configuration:

![Example of running configuration for PyCharm](docs/images/pycharm_execution_conf.png "Example of running configuration for PyCharm")

>## **Note**
>
> The required Python package (`devo-collector-sdk==1.6.1`) is not still published in a public repository (the process on going) and, meanwhile this is done, a manual installation has to be done, it can be used the following command:
>
>```script 
>pip install ./devo-collector-sdk-1.6.1.tar.gz
>```

---

### Building

The following bash script must be executed from the collector's root directory.

```bash
./build_tools/build_docker.sh
```

### Running as a Docker container

Change `<version>` with a proper value.
```bash
docker run \
--name collector-cylance-if \
--volume $PWD/certs:/devo-collector/certs \
--volume $PWD/config:/devo-collector/config \
--volume $PWD/credentials:/devo-collector/credentials \
--volume $PWD/state:/devo-collector/state \
--env CONFIG_FILE=config.yaml \
--rm --interactive --tty \
{docker_image_name}:<version>
```

## Vulnerabilities check with Trivy

The security vulnerabilities can be checked using the Trivy software (https://trivy.dev/)

### Local installation

Change `<version>` with a proper value.
```bash
trivy image --severity CRITICAL,HIGH,UNKNOWN path_to_collector_image:<version>
```

### Docker

Change `<version>` with a proper value.
```bash
docker run aquasec/trivy image --severity CRITICAL,HIGH,UNKNOWN devo.com/collectors/ms-graph-collector-if:<version>
```
