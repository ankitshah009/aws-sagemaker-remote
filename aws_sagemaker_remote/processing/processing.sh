#!/bin/sh
echo Processing script
echo Environment
env
echo Arguments
echo "$@"
#echo LS
#ls -lR /opt/ml/processing
echo Running script

if [ ! -z "${AWS_SAGEMAKER_REMOTE_MODULE_MOUNT}" ]; then
    export PYTHONPATH="${AWS_SAGEMAKER_REMOTE_MODULE_MOUNT}:${PYTHONPATH}"
fi

if [ ! -z "${AWS_SAGEMAKER_REMOTE_CONFIGURATION_SCRIPT}" ]; then
    source "${AWS_SAGEMAKER_REMOTE_CONFIGURATION_SCRIPT}"
fi

if [ ! -z "${AWS_SAGEMAKER_REMOTE_CONFIGURATION_COMMAND}" ]; then
    sh -c "${AWS_SAGEMAKER_REMOTE_CONFIGURATION_COMMAND}"
fi

if [ ! -z "${AWS_SAGEMAKER_REMOTE_REQUIREMENTS}" ]; then
    "${AWS_SAGEMAKER_REMOTE_PYTHON}" -m pip install -r "${AWS_SAGEMAKER_REMOTE_REQUIREMENTS}"
fi

#echo Running "${AWS_SAGEMAKER_REMOTE_PYTHON}" "${AWS_SAGEMAKER_REMOTE_SCRIPT}" "$@"

"${AWS_SAGEMAKER_REMOTE_PYTHON}" "${AWS_SAGEMAKER_REMOTE_SCRIPT}" "$@"
