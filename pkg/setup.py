"""Setup file for s23finalproject package"""
from setuptools import setup

setup(
    name="s23finalproject",
    version="0.0.1",
    description="OpenAlex Works class for 06-682 final project",
    maintainer="Jason Yao",
    maintainer_email="jasonyao@andrew.cmu.edu",
    license="MIT",
    packages=["s23finalproject"],
    entry_points={
        "console_scripts": [
            "oaw = s23finalproject.oaw:main",
        ]
    },
    long_description="""Open Alex works class with helpful methods""",
)
