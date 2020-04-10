#!/usr/bin/env python3

import argparse
from pathlib import Path

import shapefile


def main():
    # Settings for Argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    # Open shape file
    shape_path = Path(args.path)
    shape_file = shapefile.Reader(shp=shape_path.open('rb'))

    # get shapes
    shapes = shape_file.shapes()
    for shape in shapes:
        print(shape.shapeType)


if __name__ == '__main__':
    main()
