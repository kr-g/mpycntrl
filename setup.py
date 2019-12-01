import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mpycntrl", 
    version="0.0.2",
    author="k.r. goger",
    author_email="k.r.goger+mpycntrl@gmail.com",
    description="Control MicroPython with your own code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kr-g/mpycntrl",
    packages=setuptools.find_packages(),
    license = 'MIT',
    keywords = 'micropython utility shell',
    install_requires=['pyserial'],    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Terminals :: Serial',
        'Topic :: Utilities',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)

