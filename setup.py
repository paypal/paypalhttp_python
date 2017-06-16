from setuptools import setup

version = "0.1.3"

long_description = """
	BraintreeHttp is a generic http client designed to be used with code-generated projects.
"""

setup(
    name="braintreehttp",
    long_description=long_description,
    version=version,
    author="Braintree",
    author_email="support@braintreepayments.com",
    packages=["braintreehttp"],
    install_requires=['requests>=2.0.0', 'six>=1.0.0', 'pyopenssl>=0.15'],
    liscene="MIT",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
