from setuptools import setup

setup(name='MongoMapper.python',
      version='0.1',
      description='ORM MongoDB',
      url='https://bitbucket.org/etooltech/mongo_mapper',
      author='ETOOL Innovation',
      author_email='info@etoolinnovation.com',
      license='MIT',
      packages=['mongo_mapper'],
      zip_safe=False, install_requires=['pymongo'])