import setuptools as s

s.setup(
    name='molo',
    version='1.0',
    description='Compile for visual novels',
    author='HaxiDenti',
    install_requires=[
        # "lispy @ git+https://github.com/AldieNightStar/lispy.git"
    ],
    packages=["molo"],
    package_data={"": ["*.js"]}
)
