import argparse
import os

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dir', required="true", help="The top level directory containing all of the .cs files that need to be updated.")

    args = parser.parse_args()
    rootdir = args.dir

    for subdir, dirs, files in os.walk(rootdir):
      for file in files:
        if file.lower().endswith('.cs'):
          filename = os.path.join(subdir, file)
          processFile(filename)


def processFile(file):
  print(f'Processing {file}')
  # with open('filename') as f:
  #   lines = f.readlines()



if __name__ == "__main__":
  main()