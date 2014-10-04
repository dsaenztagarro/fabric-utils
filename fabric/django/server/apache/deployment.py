from fabric.api import sudo, env
from fabric.utils import pgreen, pcyan


def install_site():
    pgreen("*** Configuring apache server...")
    apache_path = '%s/config/apache/%s' % (env.release_path, env.environment)

    pcyan('Create symlinks...')
    sudo(('ln -s -f {apache_path}/cirujanos {sites_available}/cirujanos; '
          'ln -s -f {apache_path}/cirujanos.wsgi {www}/cirujanos.wsgi; ').
         format(apache_path=apache_path,
                sites_available='/etc/apache2/sites-available',
                www='/var/www/cirujanos'))

    pcyan('Enable apache site...')
    sudo('cd /etc/apache2/sites-available/; a2ensite %s; ' % env.project_name)


def restart_webserver():
    pgreen("*** Restarting web server...")
    sudo('service apache2 restart; service apache2 reload; ')
