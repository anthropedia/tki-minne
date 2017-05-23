from distutils.core import setup


setup(
    name='tci-database',
    version='0.4',
    author='Vincent Agnano',
    license='Copyright. All right reserved.',
    long_description=open('readme.md').read(),
    install_requires=[
        'mongoengine==0.11',
        'Werkzeug==0.12',
        'Flask-Login==0.4.0',
    ]
)
