#!/usr/bin/python3
"""
   A fabric script that compresses the contents of web_static into a .tgz
   archive and deploys it to a web server
"""
from fabric.api import *
from datetime import datetime
from os.path import exists


env.hosts = ['52.87.216.43', '100.25.180.60']


def do_pack():
    """
       Generates a .tgz archvive containing all the files in web_static
       directory
    """
    try:
        local('mkdir -p versions')
        now = datetime.now()

        timestamp = now.strftime("%Y%m%d%H%M%S")
        archive_name = "web_static" + timestamp + ".tgz"

        local("tar -cvzf versions/{} web_static".format(archive_name))

        filename = "versions/{}".format(archive_name)
        local(print("web_static packed: {}".format(filename)))
        return filename
    except Exception:
        return None


def do_deploy(archive_path):
    """ Deploys a .tgz archive to the path specified in archive_path """
    if not exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        archive = archive_path.split("/")[-1]
        archive_name = archive.split(".")[0]
        path = "/data/web_static/releases/"
        run("mkdir -p /data/web_static/releases/{}".format(archive_name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive, archive_name))
        run("rm /tmp/{}".format(archive))
        run("mv {1}{0}/web_static/* {1}{0}".format(archive_name, path))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_name))
        run("rm -rf /data/web_static/current")
        run("ln -sf /data/web_static/releases/{} /data/web_static/current"
            .format(archive_name))
        return True
    except Exception:
        return False


def deploy():
    """
       Creates a .tgz archive of the files in web_static directory
       and deploys it to a webserver
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    """ Deletes out of date archives """
    number = int(number)
    if number == 0:
        number = 1
    recent = local("ls -t versions/", capture=True).split("\n")
    archive_delete = recent[number:]
    for archive in archive_delete:
        local(f"rm -f versions/{archive}")

    with cd("/data/web_static/releases/"):
        remote_archives = run("ls -t").split("\n")

    archives_to_delete = remote_archives[number:]
    for arch in archives_to_delete:
        run(f"rm -rf /data/web_static/releases/{arch}")
