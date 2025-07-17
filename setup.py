from setuptools import setup, find_packages

setup(
    name='winterwebrecon',
    version='1.0.0',
    description='Advanced Web Reconnaissance Tool',
    author='Álvaro',
    author_email='godbizmusic@gmail.com',
    url='https://github.com/ItzWintr/winterwebrecon',
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'wwtool=winterwebrecon.main:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
