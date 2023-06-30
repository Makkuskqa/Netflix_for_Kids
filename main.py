import argparse


def etl(day):
  print(f"starting etl for execution day: {day} ")


def main():
  args = get_arguments()
  etl(args.execution_day)


def get_arguments():
  # Create an ArgumentParser object
  parser = argparse.ArgumentParser(description='Description of your program.')

  # Add input arguments
  parser.add_argument('execution_day',
                      type=str,
                      help='Description of argument 1')

  # Parse the input arguments
  args = parser.parse_args()
  return args


if __name__ == "__main__":
  main()
