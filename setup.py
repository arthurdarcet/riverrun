#!/usr/bin/env python
# coding: utf-8

import setuptools


setuptools.setup(
    name='riverrun',
    version='0.1',
    author='Arthur Darcet',
    author_email='arthur@darcet.fr',
    description="A minimalist book library web interface.",
    license='MIT',
    keywords=['ebook', 'epub', 'library', 'daemon', 'webui'],
    url='http://github.com/arthurdarcet/riverrun',
    download_url='http://pypi.python.org/pypi/riverrun',
    packages=['riverrun', 'riverrun.book', 'riverrun.http'],
    package_data={'riverrun': ['config.yaml', 'http/static/*']},
    install_requires=open('requirements.pip').read().split('\n'),
    entry_points = {'console_scripts': ['riverrun = riverrun.__main__',]},
    test_suite='test',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
    ],
    include_package_data=True,
)
