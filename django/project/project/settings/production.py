# settings/production.py

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# After got my own host, set it up
ALLOWED_HOSTS = ['ec2-13-114-190-242.ap-northeast-1.compute.amazonaws.com']

