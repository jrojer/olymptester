import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="olymptester",
    version="1.0",
    author="Alexey Roussanov",
    author_email="cibid@yandex.ru",
    description="Competitive programming testing tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrojer/olymptester/",
    project_urls={
        "Bug Tracker": "https://github.com/jrojer/olymptester/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)