import setuptools

setuptools.setup(
    name='helpers',
    version='0.0.1',
    install_requires=[
        'requests',
        'lxml',
        'toolz',
        'importlib-metadata; python_version == "3.10"',
    ],
)
