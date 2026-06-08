ARG PYTHON_VERSION=3.11
ARG PYTHON_SRC=python:${PYTHON_VERSION}-bullseye

FROM ${PYTHON_SRC} AS spark-base

# ---- 0: General Utilities: Setup ----

ARG JDK_VERSION=17
ARG JDK_SRC=openjdk-${JDK_VERSION}-jdk

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ${JDK_SRC} \
        rsync \
        build-essential \
        software-properties-common \
        ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ---- 1: Apache Spark: Setup ----

ARG SPARK_VERSION=4.1.2
ARG SPARK_SRC=https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz

ENV SPARK_HOME=/opt/spark
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=${SPARK_HOME}/sbin:${SPARK_HOME}/bin:${PATH}
ENV PYSPARK_PYTHON=python3

RUN mkdir -p ${HADOOP_HOME} && mkdir -p ${SPARK_HOME}

WORKDIR ${SPARK_HOME}

RUN curl -fSL "${SPARK_SRC}" -o spark-dist.tgz && \
    tar xvzf spark-dist.tgz --directory . --strip-components 1 && \
    rm -f spark-dist.tgz

RUN chmod u+x ./sbin/* && \
    chmod u+x ./bin/*

# ---- 2: Python Packages: Setup ----

# NB: we do not need to install `pyspark` as these will be accessed via 
#     the `spark-submit` binaries stored within ${SPARK_HOME}; however, it is helpful 
#     to do so for intellisense purposes!

RUN pip3 install \
    ipython \
    pandas \
    pyspark==${SPARK_VERSION} \
    pyarrow

CMD ["/bin/bash"]
