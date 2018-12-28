import argparse
import cProfile
import json
import sys
import os
# Add cpt to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cpt.Cpt import Cpt  # pylint: disable=wrong-import-position


def main():
    parser = argparse.ArgumentParser(description='Profile code for train or predict with cpt')
    parser.add_argument(choices=['train', 'predict'], dest='mode',
                        help='mode should be either train or predict')
    parser.add_argument(dest='data_path', help='the data path file')
    parser.add_argument(dest='profile_path',
                        help='the output path file for the profile')

    args = parser.parse_args()

    if args.data_path.endswith('.json'):
        with open(args.data_path) as file:
            data = list(json.load(file).values())
    else:
        with open(args.data_path) as file:
            data = map(lambda l: [int(x) for x in l.rstrip().split()],
                       file.readlines())

    cpt = Cpt()

    if args.mode == 'predict':
        data = [sequence[-10:] for sequence in data]
        cpt.train(data)

    cProfile.runctx('cpt.{}(data)'.format(args.mode), None, locals(), args.profile_path)


if __name__ == '__main__':
    main()