from distutils.core import setup

setup(
    name='fabric-utils',
    version='0.0.2',
    author='David Saenz Tagarro',
    author_email='david.saenz.tagarro@gmail.com',
    packages=['lib', 'lib.fabric'],
    url='https://github.com/dsaenztagarro/fabric-utils',
    license='LICENSE.txt',
    description='Fabric utils for deployment management',
    long_description=open('README.txt').read(),
)
