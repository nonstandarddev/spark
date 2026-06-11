# Apache Spark - Standalone Cluster (via Docker)

## Overview

This repository outlines a 'minimal' approach for provisioning Apache Spark either on your local machine or, alternatively, on
some kind of cloud-hosted resource (e.g. EC2, Digital Ocean and so forth).

Getting started is as simple as,

```sh
make run
```
Open your browser at `localhost:8080` and you should observe an interface into the 'master' node of your Apache Spark network (details below). 

## Architecture

Broadly speaking, Apache Spark leverages a traditional, intuitive [_master-slave_](https://en.wikipedia.org/wiki/Master%E2%80%93slave_(technology)) architecture,

<p align="center">
    <img src="./figures/architecture.png" alt="Architectural diagram of standalone Spark cluster (driver, manager and worker nodes)" width="600">
</p>

Each of the components outlined above are documented within the following respective files,

* `Dockerfile` which prescribes the base image configured with an Apache Spark distribution
* `compose.yml` which outlines how the base image (above) is adapted into different Apache Spark services (e.g. `master`, `worker` and so on)


## Languages

You can use one or more of,

* Java
* Scala
* Python

Python tends to be more common as it is easier to 'get up and running' (and negates the need
for compilation and so forth).

## Spark Software Libraries

* **Spark Core:** Core functionality - most commonly used.
* **Spark Streaming:** Tools for 'streaming' data from one source to another.
* **Spark SQL:** API for using ANSI-SQL syntax in Spark.
* **MLLib:** Used for machine learning functionality.
* **GraphX:** Used for managing network data and/or graphical data.
