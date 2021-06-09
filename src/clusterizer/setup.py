from setuptools import setup, Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
# python setup.py build_ext --inplace

ext_options = {
    # 'language':"c++",
    # 'extra_compile_args':["-O3",],
    'include_dirs': ['.', '..', '../..'],
}

extensions = [
    Extension("seine_data_utils", sources=["utils/seine_data_utils.pyx"], **ext_options),
   
]

setup(
    ext_modules=cythonize(extensions, annotate=True, force=True),
)