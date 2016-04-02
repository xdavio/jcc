from setuptools import setup

setup(
    name='jcc',
    version='0.1',
    py_modules=['commands'],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        jcc=commands:cli
    ''',
)
