from setuptools import setup, find_packages

setup(
    name="x86_emulator",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'emu-cli=cli.main:main',
        ],
    },
)
