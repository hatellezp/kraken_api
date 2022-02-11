
import os.path
from distutils.core import setup

exec(open('./kraken_api/version.py').read())

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='kraken_api',
      version=__version__,
      description='kraken.com cryptocurrency exchange API using pandas and krakenex',
      long_description=read('README.rst'),
      author='Horacio Tellez',
      author_email='hatellezp@gmail.com',
      url=__url__,
      install_requires=[
          'krakenex>=2.1.0'
      ],
      packages=['kraken_api'],
      python_requires='>=3.7',
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',

      ],
)