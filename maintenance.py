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

import boto3
from boto3 import session


# Read this once for the lifetime of the invocation
ALL_PROFILES = session.Session().available_profiles


def parse_aws_profiles(profile_names_str):
    """custom argparse type for validating AWS profile names. Returns a scrubbed list of strings which are guaranteed to be valid profiles"""

    profile_names = profile_names_str.rstrip(',').split(',')

    result_profiles = []
    unknown_profiles = []

    for p in profile_names:
        if p in ALL_PROFILES:
            result_profiles.append(p)
        else:
            unknown_profiles.append(p)

    if len(unknown_profiles) > 0:
        raise argparse.ArgumentTypeError('Unknown profiles {}'.format(','.join(unknown_profiles)))
    else:
        return result_profiles


def getSessions(profile_names):
    """Given a set of profiles, give us the session objects that represent them and which we can use to perform the maintenance"""
    logger.info('Profiles: %s', profile_names)

    for profile_name in profile_names:
        logger.info('Using profile: {}'.format(profile_name))
        current_session = session.Session(profile_name=profile_name)
        sts = current_session.client('sts')
        ident = sts.get_caller_identity()
        logger.info('Profile: {}, Account: {}, User:{}'.format(profile_name,ident['Account'], ident['Arn']))


def main(argv=None, parser=None):
    if argv == None:
        argv = sys.argv[1:]

    if parser == None:
        parser = argparse.ArgumentParser(description='Perform maintenance tasks for AWS accounts')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__version__))
    parser.add_argument('-p', '--profile', default=ALL_PROFILES, dest='profile_names', type=parse_aws_profiles, metavar='PROFILE', help='The AWS profile(s) that require maintenance, comma separated (default: all)')

    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.add_parser('all')

    args = parser.parse_args(argv)

    sessions = getSessions(args.profile_names)


if __name__ == '__main__':
    main()
