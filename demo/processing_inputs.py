import argparse
import os
import pprint
from torch import nn
from torch.utils import data
from torchvision.datasets import MNIST
import torchvision.transforms as transforms
from aws_sagemaker_remote.processing import sagemaker_processing_main
from aws_sagemaker_remote.args import OPTIONAL, PathArgument

import stat
import pathlib


def show_path(path):
    if not path:
        print("Empty")
    elif path.startswith('s3://'):
        print("Path [{}] is on s3".format(path))
    else:
        if os.path.exists(path):
            print("Path [{}] exists".format(path))
            st_mode = pathlib.Path(path).stat().st_mode
            if os.path.isdir(path):
                print("Directory contents: {}".format(
                    list(os.listdir(path))
                ))
            elif os.path.isfile(path):
                with open(path) as f:
                    contents = f.read()
                print("File contents: [{}]".format(contents))
            elif stat.S_ISFIFO(st_mode):
                print("Path is fifo")
                with open(path) as f:
                    contents = f.read()
                print("Fifo contents: [{}]".format(contents))
            else:
                print("Path [{}] is not file or folder".format(path))
        else:
            print("Path [{}] does not exist".format(path))


def main(args):
    # Main function runs locally or remotely
    print("ARGS")
    print(vars(args))
    print("test_folder")
    show_path(args.test_folder)
    print("test_file")
    show_path(args.test_file)
    print("test_s3_folder")
    show_path(args.test_s3_folder)
    print("test_s3_file")
    show_path(args.test_s3_file)
    print("test_optional")
    show_path(args.test_optional)
    print("test_s3_folder_pipe")
    show_path(args.test_s3_folder_pipe)
    print("test_s3_folder_pipe-manifest")
    show_path("{}-manifest".format(args.test_s3_folder_pipe))
    print("test_s3_folder_pipe_0")
    show_path("{}_0".format(args.test_s3_folder_pipe))
    print("test_s3_file_pipe")
    show_path(args.test_s3_file_pipe)
    print("root dir")
    show_path(os.path.dirname(args.test_folder))


if __name__ == '__main__':
    sagemaker_processing_main(
        main=main,  # main function for local execution
        inputs={
            'test_folder': 'demo/test_folder',
            'test_file': 'demo/test_folder/test_file.txt',
            'test_s3_folder': 's3://sagemaker-us-east-1-683880991063/test_folder',
            'test_s3_file': 's3://sagemaker-us-east-1-683880991063/test_folder/test_file.txt',
            'test_optional': OPTIONAL,
            'test_s3_folder_pipe': PathArgument('demo/test_folder/test_file.txt', mode='Pipe'),
            'test_s3_file_pipe': PathArgument('demo/test_folder/test_file.txt', mode='Pipe'),
        },
        dependencies={
            # Add a module to SageMaker
            # module name: module path
            'aws_sagemaker_remote': os.path.join(__file__, '../../aws_sagemaker_remote')
        },
        configuration_command='pip3 install --upgrade sagemaker sagemaker-experiments',
        # Name the job
        base_job_name='demo-optional-arguments'
    )
