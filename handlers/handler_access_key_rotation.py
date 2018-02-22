import logging

import boto3
from boto3.session import Session

class KeyRotator:
    NAME = 'rotate-keys'

    def __init__(self):
        print("Init key Rotator")

    def configure_parser(self, parser):
        pass

    def handle(self, Session):
        pass


def getClass():
    return KeyRotator

