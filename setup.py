from distutils.core import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='fabric-utils',
    version='0.0.2',
    author='David Saenz Tagarro',
    author_email='david.saenz.tagarro@gmail.com',
    packages=['lib', 'lib.fabric'],
    url='https://github.com/dsaenztagarro/fabric-utils',
    license='LICENSE.txt',
    description='Fabric utils for deployment management',
    long_description=long_description
)
