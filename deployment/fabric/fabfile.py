__author__ = 'pengfeiz'


import boto, urllib2
from boto.ec2 import connect_to_region
from fabric.api import env, run, cd, settings, sudo,local, put
from fabric.contrib.files import exists, sed
from fabric.api import parallel
import os
import csv

REGION = "us-east-1"
WEB_ROOT = "/var/www"
REPO_URL = 'git@github.com:CAFI2/auto.git'

# Server user, normally AWS Ubuntu instances have default user "ubuntu"
env.user = "ubuntu"

# List of AWS private key Files
env.key_filename = os.environ.get("AWS_KEYPATH")

@parallel
def pip_install(package):
    sudo('pip install %s' % (package, ))



@parallel
def update_node_env():
    sudo('apt-get install -y nodejs-legacy')
    sudo('apt-get install -y npm')
    sudo('npm install npm -g')
    sudo('npm install -g bower')


@parallel
def update_os():
    sudo('apt-get update -y')
    sudo('apt-get upgrade -y')

# Fabric task to reboot OS (Ubuntu), runs in parallel
# To execute task using fabric run following
# fab set_hosts:phpapp,2X,us-west-1 reboot_os
@parallel
def reboot_os():
    sudo('reboot')


@parallel
def add_users(public_key_file="/Users/pengfeiz/OneDrive/Intern/Deloitte/CAFI/AWS/public_keys.csv"):
    with open(public_key_file, 'rb') as f:
        reader = csv.reader(f)
        public_key_list = list(reader)
    for key in public_key_list:
        add_user(key[0], key[1])


@parallel
def add_user(user_name, pub_key):
    sudo('adduser {name} --disabled-password --gecos GECOS'.format(name=user_name))
    sudo('mkdir /home/{name}/.ssh'.format(name=user_name), user=user_name)
    sudo('chmod 700 /home/{name}/.ssh'.format(name=user_name), user=user_name)
    sudo('touch /home/{name}/.ssh/authorized_keys'.format(name=user_name), user=user_name)
    sudo('chmod 600 /home/{name}/.ssh/authorized_keys'.format(name=user_name),  user=user_name)
    sudo('echo "{key}" >> /home/{name}/.ssh/authorized_keys'.format(key=pub_key, name=user_name), user=user_name)


@parallel
def show_users():
    run('ls /home/')

@parallel
def delete_user(user_name):
    sudo('userdel -r {name}'.format(name=user_name))


@parallel
def apt_install(name):
    sudo('apt-get install -y {package_name}'.format(package_name=name))


@parallel
def update_code(source_folder="/home/ubuntu/cafi", branch="develop"):
    sudo('rm -rf %s' % (source_folder,))
    run('git clone -b %s %s %s' % (branch, REPO_URL, source_folder))


@parallel
def update_virtualenv(source_folder="/home/ubuntu/cafi"):
    virtualenv_folder = source_folder + '/../virtualenv'
    sudo('rm -rf %s' % (virtualenv_folder,))
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder, source_folder))


@parallel
def update_angular(source_folder="/home/ubuntu/cafi"):
    run('cd %s/static && bower install' % (source_folder,))


@parallel
def update_settings(source_folder="/home/ubuntu/cafi"):
    settings_path = source_folder + '/backend/settings/local.py'
    put('./local.py', settings_path)
    sed(settings_path, "Users/yangm/cafi/project", "home/ubuntu/cafi")


@parallel
def update_database(source_folder="/home/ubuntu/cafi"):
    sudo('cp /etc/postgresql/9.3/main/pg_hba.conf /home/ubuntu/pg_hba.conf')
    settings_path = '/home/ubuntu/pg_hba.conf'
    sudo('rm %s' %(settings_path, ))
    put('./pg_hba.conf', settings_path)
    sudo('cp /home/ubuntu/pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf')
    sudo('service postgresql restart')
    # sudo('cd %s/backend && sudo -u postgres createuser cafi' % (source_folder,))
    sudo('cd %s/backend && sudo -u postgres dropdb cafi' % (source_folder,))
    sudo('cd %s/backend && sudo -u postgres createdb cafi -O cafi' % (source_folder,))
    run('cd %s/backend && ../../virtualenv/bin/python manage.py makemigrations --noinput' % (source_folder,))
    run('cd %s/backend && ../../virtualenv/bin/python manage.py migrate --noinput' % (source_folder,))
    run('cd %s/backend && ../../virtualenv/bin/python manage.py loaddata risk/fixtures/risks.json' % (source_folder,))


@parallel
def start_django(source_folder="/home/ubuntu/cafi"):
    kill_port(8080)
    run('nohup %s/../virtualenv/bin/python %s/backend/manage.py '
        'runserver 0.0.0.0:8080 >&/home/ubuntu/log < /home/ubuntu/log &' % (source_folder, source_folder), pty=False)

@parallel
def restart_redis(source_folder="/home/ubuntu/cafi"):
    kill_all('redis-server')
    sudo('/etc/init.d/redis-server start')


@parallel
def start_celery(source_folder="/home/ubuntu/cafi"):
    put('./supervisord.conf', '%s/backend/supervisord.conf' % (source_folder, ))
    run('cd /home/ubuntu/cafi/backend && supervisord -c supervisord.conf')


@parallel
def stop_celery_workers(source_folder="/home/ubuntu/cafi"):
    run('cd %s/backend && supervisorctl -c supervisord.conf stop celeryd' %(source_folder, ))
    run('cd %s/backend && supervisorctl -c supervisord.conf shutdown' %(source_folder, ))


def kill_port(port=8080):
    with settings(warn_only=True):
        run('sudo kill $(lsof -t -i:%s) ' % (port, ))

def kill_all(process):
    with settings(warn_only=True):
        sudo('killall %s' % (process, ))

@parallel
def deploy(source_folder="/home/ubuntu/cafi"):
    stop_celery_workers(source_folder)
    update_code(source_folder)
    update_virtualenv(source_folder)
    update_settings(source_folder)
    update_angular(source_folder)
    update_database(source_folder)
    start_django(source_folder)
    restart_redis(source_folder)
    start_celery(source_folder)


def visudo(user_name):
    sudo('cp -p /etc/sudoers /etc/sudoers.bak')
    sudo('cp -p /etc/sudoers /etc/sudoers.tmp')
    sudo('sed \'$a\pezheng ALL=(ALL) ALL\' /etc/sudoers.tmp'.format(name=user_name))
    sudo('mv /etc/sudoers.tmp /etc/sudoers')


def set_hosts(tag="instance-state-code", value="16", region=REGION):
    key = tag
    env.hosts = _get_public_dns(region, key, value)


def set_host(hostUrl):
    env.hosts = [hostUrl]


# Private method to get public DNS name for instance with given tag key and value pair
def _get_public_dns(region, key, value ="*"):
    public_dns = []
    connection = _create_connection(region)
    reservations = connection.get_all_instances(filters={key: value})
    for reservation in reservations:
        for instance in reservation.instances:
            print "Instance", instance.public_dns_name
            public_dns.append(str(instance.public_dns_name))
    return public_dns


# Private method for getting AWS connection
def _create_connection(region):
    print "Connecting to ", region

    conn = connect_to_region(
        region_name = region,
        aws_access_key_id=os.environ.get("AWS_KEY"),
        aws_secret_access_key=os.environ.get("AWS_SECRET")
    )

    print "Connection with AWS established"
    return conn