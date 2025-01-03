from setuptools import setup, find_packages

setup(
    name='aminoacid_tsr_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'joblib',
    ],
    author='Krishna Rauniyar',
    author_email='krishna.rauniyar1@louisiana.edu',
    description='A package for retrieving PDB files and generating key/triplet files for Amino Acid Protein and Mirror, Non-Mirror analysis.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KrishnaRauniyar/TSR_AMINOACID_PACKAGE.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)