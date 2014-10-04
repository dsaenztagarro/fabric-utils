from fabric.api import task, env
from fabric.contrib import django
from fabric.django.server.utils import sudo_command


@task
def dumpdata():
    command = ('./manage.py dumpdata --indent=2 > /tmp/cirujanos_dump.json')
    command_params = ()
    sudo_command(command, command_params)


@task
def mysqldump():
    django.project('config.settings.%s' % env.environment)
    from django.conf import settings
    command = ('./mysqldump -u %s -p=%s %s > /tmp/cirujanos_dump.json')
    command_params = (settings.DATABASE_USER,
                      settings.DATABASE_PASSWORD,
                      settings.DATABASE_NAME)
    sudo_command(command, command_params)
