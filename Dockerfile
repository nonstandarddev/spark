# ---- 1: User-Defined Parameters ----

ARG PYTHON_VERSION=3.11

# ---- 2: Build Tools: Setup ----

FROM python:${PYTHON_VERSION}-bullseye

ARG JDK_VERSION=17
ARG JDK_SRC=openjdk-${JDK_VERSION}-jdk

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ${JDK_SRC} \
        rsync \
        ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ---- 3: Apache Spark: Setup ----

ARG SPARK_VERSION=4.1.2
ARG SPARK_MINOR_VERSION=4.1
ARG SPARK_SRC=https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz

ENV SPARK_HOME=/opt/spark
ENV SPARK_MASTER_HOST=spark-master
ENV SPARK_MASTER_PORT=7077
ENV SPARK_MASTER_URL="spark://${SPARK_MASTER_HOST}:${SPARK_MASTER_PORT}"
ENV PATH=${SPARK_HOME}/sbin:${SPARK_HOME}/bin:${PATH}
ENV PYSPARK_PYTHON=python3
ENV PYARROW_IGNORE_TIMEZONE=1

RUN mkdir -p ${SPARK_HOME}

WORKDIR ${SPARK_HOME}

RUN curl -fSL "${SPARK_SRC}" -o spark-dist.tgz && \
    tar xvzf spark-dist.tgz --directory "${SPARK_HOME}" --strip-components 1 && \
    rm -f spark-dist.tgz

COPY config/log4j2.properties ${SPARK_HOME}/conf/log4j2.properties

COPY config/spark-defaults.conf ${SPARK_HOME}/conf/spark-defaults.conf

RUN chmod u+x ./sbin/* && \
    chmod u+x ./bin/*

# ---- 4: Delta Lake: Setup ----

ARG SCALA_VERSION=2.13
ARG DELTA_SPARK_VERSION=4.1.0
ENV DELTA_PACKAGE_VERSION=io.delta:delta-spark_${SPARK_MINOR_VERSION}_${SCALA_VERSION}:${DELTA_SPARK_VERSION}

RUN printf "\nspark.jars.packages ${DELTA_PACKAGE_VERSION}\n" >> ${SPARK_HOME}/conf/spark-defaults.conf

# ---- 5: Python: Setup ----

# NB: we do not need to install `pyspark` as this will be invoked via 
#     the `spark-submit` binaries stored within ${SPARK_HOME}; however, it is helpful 
#     to do so for intellisense purposes!

RUN pip3 install --no-cache-dir \
    "pandas>=2.2,<3" \
    pyarrow \
    pyspark==${SPARK_VERSION} \
    delta-spark==${DELTA_SPARK_VERSION} \
    deltalake

COPY provision.sh .

RUN chmod +x provision.sh

ENTRYPOINT ["./provision.sh"]
