from setuptools import Extension, setup

ext_modules = [
    Extension(
        'barecat_mount.barecat_mount_cython',
        sources=['src/barecat_mount/barecat_mount_cython.pyx'],
        extra_compile_args=['-O3', '-Wno-cpp', '-Wno-unused-function', '-std=c99'],
        define_macros=[("FUSE_USE_VERSION", "39")],
        libraries=["fuse3", "c"],
    ),
]

setup(ext_modules=ext_modules)
