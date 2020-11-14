import argparse


def check_maxdepth(val):
    val = int(val)
    if val < 0:
        raise argparse.ArgumentTypeError("-maxdepth should be a non-negative integer.")
    return val

    
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--maxdepth', type=check_maxdepth, default=1, help="How deep in the directory tree to find files.")
    parser.add_argument('-p', '--path', type=str, default='.',  help="Which path to search files from.")
    return parser