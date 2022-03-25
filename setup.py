from setuptools import setup

version = "1.0.1"

long_description = """
	PayPalHttp is a generic http client designed to be used with code-generated projects.
"""

setup(
    name="paypalhttp",
    long_description=long_description,
    version=version,
    author="PayPal",
    packages=["paypalhttp", "paypalhttp/testutils", "paypalhttp/serializers"],
    install_requires=['requests>=2.0.0', 'six>=1.0.0', 'pyopenssl>=0.15', 'typing>=3.10.0.0'],
    license="MIT",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
