__version__ = '0.1'

import sys
if sys.version_info < (2, 7):
    print('This program requires Python 2.7 or newer.')
    sys.exit(1)

if sys.version_info >= (2, 7):
    import logging
    logger = logging.getLogger(__name__)
    loghandler=logging.StreamHandler()
    loghandler.setFormatter(logging.Formatter("Maintenance: %(levelname)s: %(asctime)s: %(filename)s(%(lineno)d): %(message)s"))
    logger.addHandler(loghandler)
    loghandler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)


import argparse
import handlers


def main(argv=None, parser=None):
    if argv == None:
        argv = sys.argv[1:]

    if parser == None:
        parser = argparse.ArgumentParser(description='Perform maintenance tasks for AWS accounts')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__version__))
    parser.add_argument('profile', metavar='PROFILE', nargs='+', help='The AWS profile(s) that require maintenance (default: ALL)')

    subparsers = parser.add_subparsers(dest='cmd')

    args = parser.parse_args(argv)

    print(args.profile)

if __name__ == '__main__':
    main()
