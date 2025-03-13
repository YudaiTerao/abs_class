
from setuptools import setup, find_packages

setup(
    name="abs_class",
    version="0.0.0",
    author="YudaiTerao",
    author_email="terao.yudai.s4@dc.tohoku.ac.jp",
    #entry_points={
    #    'console_scripts':[
    #        'bz = BZplot.bzcell_exe:bz',
    #    ],
    #},
    package_dir = {"":"src"},
    packages=find_packages(where="src"),  # 使うモジュール一覧を指定する
)



