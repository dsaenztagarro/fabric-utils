### Introduction

This python package allows me to manage deployments of Django application into
Apache `mod_wsgi` server. Also it brings to me utils for local tasks.

### How to upload python package

```shell
python setup.py sdist upload
```

### Install package from source

```shell
pip install <PYTHON PACKAGE DIR>/dist/fabric-utils-0.0.2.tar.gz
```

### Todo

- [ ] Refactoring to remove references to own projects
- [ ] Document available tasks
- [ ] Add tests through travis

```shell
fab compress_static -c .fabricrc
```

### Requirements

Install `pandoc` 
