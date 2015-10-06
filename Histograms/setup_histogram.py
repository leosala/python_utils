from distutils.core import setup
from Cython.Build import cythonize
import numpy as np
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[ Extension("histogram",
              ["histogram.pyx"],
              libraries=["m"],
              extra_compile_args = ["-ffast-math"])]
setup(
  name = 'histogram',
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules,  #cythonize("histogram.pyx"),
  include_dirs = [np.get_include()],
)
