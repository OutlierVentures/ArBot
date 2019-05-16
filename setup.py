from setuptools import setup

setup(
    name='dlm',
    version='0.0.1',
    description='Data Liquidity Module: Web 3.0 data liquidity with Fetch.AI and Ocean Protocol. Requires a running Ocean Protocol and Fetch.AI node.',
    license='Apache License 2.0',
    packages=['dlm'],
    install_requires=['oef', 'fetchai-ledger-api', 'squid-py'],
    author='Theo Turner',
    author_email='theo@outlierventures.io',
    keywords=['blockchain', 'web3', 'crypto', 'cryptocurrency', 'data', 'liquidity', 'fetchai', 'ocean'],
    url='https://github.com/OutlierVentures/Data-Liquidity-Module',
    classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)