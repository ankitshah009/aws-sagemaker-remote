import argparse
import os
import pprint
from torch import nn
from torch.utils import data
from torchvision.datasets import MNIST
import torchvision.transforms as transforms
from aws_sagemaker_remote.training import sagemaker_training_main
import aws_sagemaker_remote
from aws_sagemaker_remote.args import PathArgument
import stat
import pathlib

from scipy.io import wavfile
from io import BytesIO
from aws_sagemaker_remote.util.pipes import chunk_iterable
from sagemaker.amazon.record_pb2 import Record
from sagemaker.amazon.common import read_recordio


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


def read_pipe(pipe):
    for i in range(5):
        with open(pipe+"_{}".format(i), 'rb') as f:
            print("opened pipe {}".format(i))
            for label, f1, f2 in chunk_iterable(read_recordio(f), 3):
                label = int(label.decode('utf-8'))
                fs1, aud1 = wavfile.read(BytesIO(f1))
                fs2, aud2 = wavfile.read(BytesIO(f2))
                print("label: {}".format(label))
                print("audio1: {},{}".format(fs1, aud1.shape))
                print("audio2: {},{}".format(fs2, aud2.shape))


def main(args):
    # Main function runs locally or remotely
    print("Test folder: {}".format(args.test_pipe))
    show_path(args.test_pipe)
    print("Test S3 file pipe manifest: {}-manifest".format(args.test_pipe))
    show_path("{}-manifest".format(args.test_pipe))
    print("Input path: {}".format(os.path.dirname(args.test_pipe)))
    show_path(os.path.dirname(args.test_pipe))
    print("Test S3 file pipe 0: {}_0".format(args.test_pipe))
    read_pipe(args.test_pipe)


if __name__ == '__main__':
    sagemaker_training_main(
        main=main,  # main function for local execution
        inputs={
            'test_pipe': PathArgument(
                'demo/test_folder/manifest-audio.json',
                mode='PipeAugmentedManifest',
                attributes=['label', 'audio1-ref', 'audio2-ref']
            )
        },
        dependencies={
            # Add a module to SageMaker
            # module name: module path
            'aws_sagemaker_remote': aws_sagemaker_remote
        },
        #configuration_command='pip3 install --upgrade sagemaker sagemaker-experiments',
        # Name the job
        base_job_name='demo-training-pipe'
    )

"""
split-lines --input demo/test_folder/manifest-speakers.json --output output/manifest-speakers --splits 2 --size 2

aws s3 sync demo/test_folder s3://sagemaker-us-east-1-683880991063/test_folder
python demo\training_inputs.py --sagemaker-run yes
"""
