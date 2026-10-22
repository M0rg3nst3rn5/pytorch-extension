from setuptools import find_packages, setup
from torch.utils.cpp_extension import BuildExtension, CppExtension

setup(
    name="trajectory-ops",
    version="0.1.0",
    description="A small CPU PyTorch extension for trajectory acceleration",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    ext_modules=[
        CppExtension(
            name="trajectory_ops._trajectory_ops",
            sources=["src/trajectory_ops/ops.cpp"],
        )
    ],
    cmdclass={"build_ext": BuildExtension},
    zip_safe=False,
)
