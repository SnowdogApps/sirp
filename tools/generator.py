"""Script for generating recommendation k-d tree.

This script extracts features from images using chosen model and then generates
k-d tree with this extracted tensors. As input it takes csv file where each
line contains id and path to image and the output is pickled tree. ID can be
integer or string.

CSV file example:
    0, polyvore-dataset/images/185225843/1.jpg
    1, polyvore-dataset/images/118117317/1.jpg
    2, polyvore-dataset/images/196794889/1.jpg
    3, polyvore-dataset/images/194797482/1.jpg
    .
    .
    .

Example:
    Generate k-d tree from list of images in images.txt using InceptionV3 model:
        
        $ python generate_tree.py images.csv --model inception
"""
import csv
import argparse
import pickle

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

    print('Extracting features...')
    extractor = models[args.model]['extractor']
    preprocess = models[args.model]['preprocess']
    descriptions = []
    for file in tqdm(images):
        img = scda.load_img(file)
        activations = scda.extract_features(extractor, img, preprocess)
        description = scda.aggregate_descriptors(activations)
        descriptions.append(description)
        
    print('Saving features...')
    with open('features.pickle', 'wb') as f:
        pickle.dump(descriptions, f, pickle.HIGHEST_PROTOCOL)
    print('Features saved.')

    print('Creating k-d tree...')
    tree = KDTree(descriptions)

    print('Pickling tree...')
    with open('tree.pickle', 'wb') as f:
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
    args = parser.parse_args()
    main(args)