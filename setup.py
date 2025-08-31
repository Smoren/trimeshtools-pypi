import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='trimeshtools',
    author='Smoren',
    author_email='ofigate@gmail.com',
    description='Trimesh tools collection',
    keywords='repo, repository, crud',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Smoren/trimeshtools-pypi',
    project_urls={
        'Documentation': 'https://github.com/Smoren/trimeshtools-pypi',
        'Bug Reports': 'https://github.com/Smoren/trimeshtools-pypi/issues',
        'Source Code': 'https://github.com/Smoren/trimeshtools-pypi',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',

        'Topic :: Software Development :: Libraries',
        'Topic :: Multimedia :: Graphics :: 3D Modeling',
        'Topic :: Utilities',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3 :: Only',

        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=["trimesh", "numpy", "scipy", "shapely"],
    extras_require={
        'dev': ['check-manifest', 'coverage'],
        'test': ['coverage'],
    },
)
