#!/bin/bash

SPARK_MECHANISM=$1

if [[ "$SPARK_MECHANISM" == "master" ]]; then
  echo "Provisioning master service..."
  start-master.sh -h $SPARK_MASTER_HOST -p $SPARK_MASTER_PORT
elif [[ "$SPARK_MECHANISM" == "worker" ]]; then
  echo "Provisioning worker service..."
  start-worker.sh $SPARK_MASTER_URL
elif [[ "$SPARK_MECHANISM" == "history" ]]; then
  echo "Provisioning history service..."
  start-history-server.sh
else
   echo "Unrecognised provisioning mechanism!"
fi
