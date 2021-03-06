from fabric.api import (sudo, env, local, run, put, settings)
from fabric.contrib import django
from fabric_utils.utils import pgreen, pred, pcyan
from fabric_utils.django.server.utils import sudo_command
import sys
import time


def generate_release_path():
    pgreen("*** Generating release path...")
    env.release = time.strftime('%Y%m%d%H%M%S')
    env.release_path = '%s/releases/%s' % (env.path, env.release)


def upload_source():
    try:
        pgreen("*** Uploading source...")
        local('hg archive %s.tar.gz' % env.release)
        run('mkdir -p %s' % env.release_path)
        put(env.release + '.tar.gz', env.path + '/packages/')
        run(('cd {release_path}; '
            'tar --strip-components 1 -zxf ../../packages/{release}.tar.gz').
            format(release_path=env.release_path, release=env.release))
        local('rm %s.tar.gz' % (env.release))
    except:
        local('rm %s.tar.gz' % (env.release))


def symlink_current_release():
    pgreen("*** Symlink current release...")
    with settings(warn_only=True):
        run(('cd %s; '
             'rm releases/previous; mv releases/current releases/previous;')
            % env.path)
    run(('cd %s/releases; '
         'ln -s %s current; ') % (env.path, env.release))


def install_requirements():
    pgreen("*** Installing python packages...")
    # TODO: set as optional reinstall all packages through:
    # 'pip freeze | xargs pip uninstall -y; '
    sudo(('source {www}/env/bin/activate; '
          'pip install -r {release_path}/requirements.txt; ').
         format(www=env.www_path, release_path=env.release_path))

    pgreen("*** Installing bower packages...")
    run('cd %s; bower install;' % env.release_path)


def migrate():
    pgreen("*** Database migrations...")
    command = ('python manage.py syncdb --noinput --settings="config.settings.{environment}";'
               'python manage.py migrate --settings="config.settings.{environment}"; ').format(environment=env.environment)
    sudo_command(command, ())


def install_static():
    pgreen("*** Collecting static resources...")
    command = ('python manage.py collectstatic --noinput --verbosity=0 --clear'
               ' --settings="config.settings.%s"; ')
    command_params = (env.environment, )
    sudo_command(command, command_params)
    pred("Setting group ownership of static resources (www-data)...")
    sudo('chown -R www-data:www-data /var/www/cirujanos')


def compress_static():
    pgreen('*** Check compress static files...')
    # Add project dir to PYTHONPATH so "config.settings" object is found

    # TODO: Since this code is extracted from project it doesn't work anymore
    # trying to get project path relative to python package path. Refactor!!
    # sys.path.append(os.path.join(
    #     os.path.dirname(os.path.realpath(__file__)),
    #     os.pardir,
    #     os.pardir))
    current_path = '/home/vagrant/Development/projects/cirujanos'
    sys.path.append(current_path)

    django.settings_module('config.settings.%s' % env.environment)
    from django.conf import settings as django_settings

    # current_path = os.path.dirname(os.path.realpath(__file__))
    pcyan('CURRENT PATH: %s\n' % current_path)
    pcyan('COMPRESS_ENABLED: %s\n' % django_settings.COMPRESS_ENABLED)
    pcyan('DEBUG: %s\n' % django_settings.DEBUG)

    if (django_settings.COMPRESS_ENABLED and not django_settings.DEBUG):
        pred('Compressing files..')
        command = './manage.py compress --settings="config.settings.%s"; '
        command_params = (env.environment, )
        sudo_command(command, command_params)
    else:
        pred('WARNING: Django settings NOT allow compression')


def compile_messages(app_paths):
    """
    Compiles messages for the list of application paths
    Parameters:
        - app_paths: array of strings with paths of django applications inside
            project which need to compile messages. Paths are relative to
            release path
    """
    pgreen("*** Compiling messages...")
    django_bin_path = 'lib/python2.7/site-packages/django/bin'
    command = env.www_path + '/env/' + django_bin_path + '/django-admin.py'

    script = 'source %s/env/bin/activate; ' % env.www_path
    for app_path in app_paths:
        script += ('cd {release_path}/{app_path}; '
                   '{command} compilemessages; ').format(
                       release_path=env.release_path,
                       app_path=app_path,
                       command=command)
    sudo(script)


def install_site():
    pgreen("*** Configuring apache server...")
    apache_path = '%s/config/apache/%s' % (env.release_path, env.environment)
    pcyan('Create symlinks...')
    sudo(('ln -s -f %s/cirujanos /etc/apache2/sites-available/cirujanos; '
          'ln -s -f %s/cirujanos.wsgi /var/www/cirujanos/cirujanos.wsgi; ')
         % (apache_path, apache_path))
    pcyan('Enable apache site...')
    sudo(('cd /etc/apache2/sites-available/; '
          'a2ensite %s; ')
         % env.project_name)


def restart_webserver():
    pgreen("*** Restarting web server...")
    sudo('service apache2 restart; service apache2 reload; ')


def www_folder_permissions():
    pgreen("*** Permission www folder...")
    sudo('chown www-data:www-data -R /var/www/cirujanos')
