import os
import re
import subprocess
from subprocess import PIPE

import tomli
from setuptools import setup

project_path = os.path.realpath(os.path.split(__file__)[0])


def get_project_info():
    r = subprocess.Popen(["git", "remote", "-v"], stdout=PIPE)
    url = re.split("\s", r.stdout.readline().decode())[1]
    name = url.split("/")[-1]
    return name, url


def get_conf_files():
    r = subprocess.Popen(["ls", "conf"], stdout=PIPE)
    lst = [f"conf/{x}" for x in r.stdout.read().decode().split("\n") if x]
    return lst


def get_install_requires():
    with open(os.path.join(project_path, "pyproject.toml"), "r") as fp:
        txt = fp.read()
        rs = tomli.loads(txt)
        lst = [
            f"{k}:{v}".replace(":^", ">=").replace(":", "==")
            for k, v in rs["tool"]["poetry"]["dependencies"].items()
            if k != "python"
        ]
        return lst


name, url = get_project_info()
datafiles = get_conf_files()
install_requires = get_install_requires()

setup(
    url=url,
    name=name,
    use_scm_version={
        "version_scheme": "post-release",
        "local_scheme": "dirty-tag",
        "write_to": f"{name}/version.py",
        "write_to_template": '__version__ = "{version}"',
        "tag_regex": r"^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$",
    },
    data_files=[
        (name, datafiles),
    ],
    install_requires=install_requires,
)
