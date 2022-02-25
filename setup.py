from setuptools import setup;
from Cython.Build import cythonize;


setup(
    name = "ControllerApp",
    ext_modules = cythonize("Controller.pyx"),
    zip_safe=False,
    );
