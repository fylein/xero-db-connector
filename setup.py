"""
Build the PyPi package.
"""

import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='xero-db-connector',
    version='0.2.0',
    author='Siva Narayanan',
    author_email='siva@fyle.in',
    description='Connects Xero to a database connector to transfer information to and fro.',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['xero', 'db', 'python', 'sdk', 'sqlite', 'postgres'],
    url='https://github.com/fylein/xero-db-connector',
    packages=setuptools.find_packages(),
    install_requires=[
        'typing==3.7.4.1',
        'pandas==0.25.2',
        'logger==1.4'
    ],
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
