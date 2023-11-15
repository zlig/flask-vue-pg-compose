#!/bin/bash
set +x
set -e

# Variables
# export AZ_USER=$(echo $USER | base64 -d)
# export AZ_PASS=$(echo $PASS | base64 -d)
# export AZ_TENANT=$(echo $TENANT | base64 -d)
# export AZ_SUBID=$(echo $SUBID | base64 -d)
export PG_PASS=$(echo $PG_PASS | base64 -d)

# Login
# az login --service-principal -u "$AZ_USER" -p "$AZ_PASS" --tenant "$AZ_TENANT"
# az account set -s "$AZ_SUBID"
# az aks get-credentials -g "$AKS_RG" -n "$AKS_NAME" --admin

# Processing
while true; do
  ## VMS
  # az version

  ## LOOP
  sleep 6m
done
