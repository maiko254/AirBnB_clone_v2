#!/usr/bin/python3
"""
   A fabric script that compresses the contents of web_static into a .tgz
   archive to be deployed to a web server
"""
from fabric.api import local
from datetime import datetime


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
