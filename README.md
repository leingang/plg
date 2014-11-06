PaperLess Grading with the plg package
======================================

This is a python package for managing, munging, and maintaing student data.  That data could be directory information or academic records.

### Commands ###
* **make test** - run all tests
* **make deb** - build Debian package
* **make source** - build source tarball
* **make daily** - make daily snapshot
* **make install** - install program
* **make init** - install all requirements
* **make clean** - clean project, remove *.pyc and other templorary files
* **make deploy** - create vitrual environment


        .
        |-- bin
        |   `-- my_program
        |-- docs
        |   `-- doc.txt
        |-- my_program
        |   |-- data
        |   |   `-- some_data.html
        |   |-- submodule
        |   |   `-- __init__.py
        |   |-- __init__.py
        |   |-- helpers.py
        |-- tests
        |   |-- __init__.py
        |   |-- test_helpers.py
        |-- Makefile
        |-- CHANGES.txt
        |-- LICENSE.txt
        |-- README.md
        |-- requirements-dev.txt
        |-- requirements.txt
        `-- setup.py

Layout structure cloned from [python-package-template](https://github.com/vital-fadeev/python-package-template)
