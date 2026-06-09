#!/bin/bash

SPARK_MECHANISM=$1

if [[ "$SPARK_MECHANISM" == "master" ]]; then
  start-master.sh -h $SPARK_MASTER_HOST -p $SPARK_MASTER_PORT
elif [[ "$SPARK_MECHANISM" == "worker" ]]; then
  start-worker.sh $SPARK_MASTER_URL
elif [[ "$SPARK_MECHANISM" == "history" ]]; then
  start-history-server.sh
else
   echo "Provided mechanism '$SPARK_MECHANISM' not recognised (must be one of: 'master', 'worker' or 'history')"
fi
