#!/usr/bin/env python3

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    shape_path = args.path
    print(shape_path)


if __name__ == '__main__':
    main()
