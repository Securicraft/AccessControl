from setuptools import setup;
from Cython.Build import cythonize;


setup(
    name = "ControllerApp",
    ext_modules = cythonize("Controller_v2.py", compiler_directives={'language_level' : "3"} ),
    zip_safe    = False,
    
    );
