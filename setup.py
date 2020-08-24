from setuptools import setup

setup(
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    entry_points={"console_scripts": ["rexpy = rexpy.__main__:cli"]}
)
