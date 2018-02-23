import logging

import boto3
from boto3.session import Session

class SecurityGroupIngressUpdater:
    NAME = 'update-security-group-ingress'

    def configure_parser(self, parser):
        pass

    def handle(self, session):
        print('Updating IP address for {}'.format(session.profile_name))


def getClass():
    return SecurityGroupIngressUpdater

