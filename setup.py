from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='NEXTIONDisplay',
      version='0.1.1',
      description='NEXTIONDisplay',
      author='Jan Battermann',
      author_email='Jan.Battermann@t-online.de',
      url='https://github.com/JamFfm/NEXTIONDisplay',
      license='GPLv3',
      keywords='globalsettings',
      packages=find_packages(),
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'NEXTIONDisplay': ['*','*.txt', '*.rst', '*.yaml']},
      install_requires=[
      ],
      long_description=long_description,
      long_description_content_type='text/markdown'
     )
