#!/bin/bash
# CREATE DIRECTORY ON DBFS FOR LOGS
LOG_DIR=/dbfs/databricks/scripts/logs/$DB_CLUSTER_ID/dask/
HOSTNAME=`hostname`
mkdir -p $LOG_DIR# INSTALL DASK AND OTHER DEPENDENCIES
set -ex
/databricks/python/bin/python -V
. /databricks/conda/etc/profile.d/conda.sh
conda activate /databricks/python
conda install -y dask
conda install -y pandas=0.23.0
# START DASK – ON DRIVER NODE START THE SCHEDULER PROCESS 
# ON WORKER NODES START WORKER PROCESSESif [[ $DB_IS_DRIVER = "TRUE" ]]; then
  dask-scheduler &>/dev/null &
  echo $! > $LOG_DIR/dask-scheduler.$HOSTNAME.pid
  conda install -y pandas
else
  dask-worker tcp://$DB_DRIVER_IP:8786 --nprocs 4 --nthreads 8 &>/dev/null &
  echo $! > $LOG_DIR/dask-worker.$HOSTNAME.pid &
  conda install -y pandas
fi