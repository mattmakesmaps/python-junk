from setuptools import setup, find_packages

setup(
    name='text_beginner',
    version='0.1',
    description='Text Beginnner Package',
    author='Matt',
    author_email='matt@mattsoft.com',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'logscan = logscan.cmd:main'
        ]
    },
)