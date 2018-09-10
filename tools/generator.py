"""Script for generating recommendation k-d tree.

This script extracts features from images using chosen model and then generates
k-d tree with this extracted tensors. As input it takes csv file where each
line contains id, path to image and the output is pickled tree. ID can be
integer or string.

CSV file example:
    0, path/to/image/0.jpg
    1, path/to/image/1.jpg
    2, path/to/image/2.jpg
    3, path/to/image/3.jpg
    .
    .
    .

Example:
    Generate k-d tree from list of images in images.txt using InceptionV3 model:

        $ python generator.py images.csv --model inception
"""
import os
import csv
import argparse
import pickle
from shutil import copy

import numpy as np
from sklearn.neighbors import KDTree
from tqdm import tqdm

from scda import scda
from scda import vgg16_extractor as vgg16
from scda import inception_v3_extractor as inception
from scda import inception_resnet_v2_extractor as inception_resnet

models = {
    'vgg16': {
        'extractor': vgg16.get_extractor(),
        'preprocess': vgg16.preprocess_input
    },
    'inception': {
        'extractor': inception.get_extractor(),
        'preprocess': inception.preprocess_input
    },
    'inception_resnet': {
        'extractor': inception_resnet.get_extractor(),
        'preprocess': inception_resnet.preprocess_input
    }
}


def main(args):
    with open(args.images, 'r') as images_list:
        reader = csv.reader(images_list)
        images = [row[1] for row in reader]
    print(len(images), 'images found')

    copy(args.images, os.path.join(args.output, 'imgs.csv'))

    print('Extracting features...')
    extractor = models[args.model]['extractor']
    preprocess = models[args.model]['preprocess']
    descriptions = []
    for file in tqdm(images):
        img = scda.load_img(file)
        activations = scda.extract_features(extractor, img, preprocess)
        mask = None
        if args.scda:
            aggregation_map, threshold = scda.aggregate(activations)
            mask = scda.get_mask(aggregation_map, threshold)
        description = scda.aggregate_descriptors(activations, mask=mask)
        descriptions.append(description)

    print('Saving features...')
    with open(os.path.join(args.output, 'features.pickle'), 'wb') as f:
        pickle.dump(descriptions, f, pickle.HIGHEST_PROTOCOL)
        print('Features saved.')

    print('Creating k-d tree...')
    tree = KDTree(descriptions)

    print('Pickling tree...')
    with open(os.path.join(args.output, 'tree.pickle'), 'wb') as f:
        pickle.dump(tree, f, pickle.HIGHEST_PROTOCOL)
        print('Tree saved.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script for generating recommendation k-d tree')
    parser.add_argument(
        'images',
        help='Path to text file with paths to images')
    parser.add_argument(
        '--model',
        choices=['vgg16', 'inception', 'inception_resnet'],
        default='inception_resnet',
        help='Model which will be used as feature extractor'
    )
    parser.add_argument(
        '--output',
        default='../application/sirp/data',
        help='Path to where output should be saved.'
    )
    parser.add_argument(
        '--scda',
        action='store_true',
        help='Activates Selective Convolutional Descriptor Aggregation'

    )
    args = parser.parse_args()
    main(args)