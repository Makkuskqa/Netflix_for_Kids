# run program with parameters

import argparse


def etl(day):
  print(f"starting etl for execution day: {day} ")


def main():
  args = get_arguments()
  print(args.name)
  print(args.age)
  print(args.job)


def get_arguments():
  # Create an ArgumentParser object
  parser = argparse.ArgumentParser(description='Description of your program.')

  # Add input arguments
  parser.add_argument('--name',
                      type=str,
                      help='Description of argument 1',
                      required=True)
  parser.add_argument('--age',
                      type=str,
                      help='Description of argument 1',
                      required=True)
  parser.add_argument('--job', type=str, help='Description of argument 1')

  # Parse the input arguments
  args = parser.parse_args()
  return args


if __name__ == "__main__":
  main()
