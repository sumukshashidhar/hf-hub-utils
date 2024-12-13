from setuptools import setup, find_packages

setup(
    name="hf-hub-utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "huggingface-hub>=0.19.0",
        "python-dotenv>=1.0.0",
        "loguru>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
            "mypy>=0.900",
        ]
    },
    entry_points={
        'console_scripts': [
            'hf-hub-utils=hf_hub_utils.cli:main',
        ],
    },
    author="Sumuk Shashidhar",
    author_email="github@sumuk.org",
    description="Tools for managing Hugging Face datasets and models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sumukshashidhar/hf-hub-utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)