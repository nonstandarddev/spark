# ---- 0: User-Defined Parameters ----

ARG PYTHON_VERSION=3.11
ARG JDK_VERSION=17
ARG SPARK_VERSION=4.1.2

# ---- 1: Computed Parameters ----

ARG PYTHON_SRC=python:${PYTHON_VERSION}-bullseye
ARG JDK_SRC=openjdk-${JDK_VERSION}-jdk
ARG SPARK_SRC=https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz

# ---- 2: Build Tools: Setup ----

FROM ${PYTHON_SRC}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ${JDK_SRC} \
        rsync \
        build-essential \
        software-properties-common \
        ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ---- 3: Apache Spark: Setup ----

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

# ---- 4: Python: Setup ----

# NB: we do not need to install `pyspark` as this will be invoked via 
#     the `spark-submit` binaries stored within ${SPARK_HOME}; however, it is helpful 
#     to do so for intellisense purposes!

RUN pip3 install \
    ipython \
    pandas \
    pyspark==${SPARK_VERSION} \
    pyarrow

CMD ["/bin/bash"]
