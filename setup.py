import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IntegrityHackerProUltimate",
    version="0.1.0",
    author="Nama Anda",
    author_email="your.email@example.com",
    description="Alat bug bounty untuk reconnaissance dan vulnerability assessment dengan integrasi DeepSeek",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/IntegrityHackerProUltimate",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Security :: Vulnerability Assessment",
    ],
    python_requires=">=3.9",
    install_requires=[
        "aiohttp>=3.8.1",
        "aiofiles>=23.1.0",
        "openai>=0.27.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.1",
            "pytest-asyncio>=0.20.2",
            "coverage>=6.3.2",
        ],
    },
)
