import argparse
parser = argparse.ArgumentParser()
parser.add_argument("trueFalse", type=bool,
                    help="Chose either true or false")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
def main():
    args = parser.parse_args()
    answer = args.trueFalse
    if args.verbose:
        print "Yeah that is {}".format(answer)
    else:
        print answer

if __name__ == '__main__':
    main()
