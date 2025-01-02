from setuptools import setup, find_packages

setup(
    name='jsonmodeler',
    version='0.2.2',
    description='A tool to convert JSON to model code in various languages',
    long_description=open('README.md', encoding="UTF8").read(),
    long_description_content_type='text/markdown',
    author='Yu Wen',
    author_email='cn.signal.hugo@gmail.com',
    url='https://github.com/CN-WenYu/JsonModeler',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'jsonmodeler=scripts.convert:main',
        ],
    },
)
