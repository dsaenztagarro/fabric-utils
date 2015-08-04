### Introduction

This python package allows me to manage deployments of Django application into
Apache `mod_wsgi` server. Also it brings to me utils for local tasks.

### Example of usage

```python
# fabfile.py
from fabric_utils.django import deployment as dep

# ...

@task
def deploy():
    if env.environment is not "local":
        require('hosts', provided_by=[local])
        require('path')
        dep.generate_release_path()
        dep.upload_source()
        dep.symlink_current_release()

    dep.install_requirements()
    dep.migrate()
    dep.install_static()
    dep.compress_static()
    dep.compile_messages(['cirujanos/apps/media', 'cirujanos/apps/about'])
    dep.www_folder_permissions()
    dep.install_site()
    dep.restart_webserver()
```


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
- [ ] Create function export_django_admin returning string without vars to add
to the rest of the sudo_command script
- [ ] Move install_site and restart_webserver to its own package
- [ ] Decorate commands with options like "settings"
- [ ] Tasks to remove old deployments from server
- [ ] ApacheWSGIDeployer.deploy (debug option)

```shell
fab compress_static -c .fabricrc
```

### Requirements

Install `pandoc` 

### Changelog

- 0.0.3: Repackaging tasks in a more concise way.
