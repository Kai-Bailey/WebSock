from setuptools import setup, find_packages
import os

def read(fname):
    """
    Returns path to README
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='websock',
      version = '0.1.3',
      author = 'Kai Bailey',
      author_email = 'kbailey1@ualberta.ca',
      url = 'https://github.com/Kai-Bailey/websocket',
      description = 'Multithreaded websocket server following RFC 6455 protocol',
      long_description = read('README.md'),
      long_description_content_type='text/markdown',
      license = 'MIT', 
      keywords = 'websocket client server multithreaded', 
      packages = find_packages(exclude=['docs', 'tests']))