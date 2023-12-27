import os
from setuptools import setup

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()


setup(name='gonit',
version='0.3',
description='This is an simple mathematical visualization Package for python',
url='https://github.com/ipritom/gonit-opengl',
author='ipritom',
author_email='pritom.blue2@gmail.com',
license='MIT',
packages=['gonit'],
install_requires=install_requires,
zip_safe=False)