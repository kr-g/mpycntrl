import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mpycntrl-pkg-kr-g", 
    version="0.01",
    author="k.r. goger",
    author_email="k.r.goger+mpycntrl@gmail.com",
    description="Control MicroPython with your own code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kr-g/mpycntrl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

