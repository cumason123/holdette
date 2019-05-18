import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-sqlite', action='store_true')
args = parser.parse_args()
print(args.sqlite)