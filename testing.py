import argparse

parser = argparse.ArgumentParser()
parser.add_argument("serving",help="runs serving test")
args = parser.parse_args()
print args.