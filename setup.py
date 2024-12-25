from platform import python_version
from setuptools import setup


def readme():
    with open('README.md') as readme_file:
        return readme_file.read()


setup(
    name='comment_parser',
    version='1.2.5',
    description='Parse comments from various source files.',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License'
    ],
    url='http://github.com/jeanralphaviles/comment_parser',
    author='Jean-Ralph Aviles',
    author_email='jeanralph.aviles+pypi@gmail.com',
    license='MIT',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=['comment_parser', 'comment_parser.parsers'],
    install_requires=['python-magic>=0.4.27'],
    zip_safe=False,
    python_requires='>=3.13',
)
