import argparse
from pandasgui import show


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", default="../data/response.pkl", help="Input path")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    show(args.input_path)
