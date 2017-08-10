from distutils.core import setup


setup(
    name='tci-minne',
    version='0.1',
    author='Vincent Agnano',
    license='Copyright. All right reserved.',
    long_description=open('readme.md').read(),
    install_requires=[
        'mongoengine==0.11',
        'Werkzeug==0.12',
    ]
)
