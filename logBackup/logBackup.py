#!/usr/bin/env python

#imports modules
import os, os.path, zipfile, zlib, socket, datetime, paramiko, sys

#Logserver Parameters
logserver=(sys.argv[1])
uname=(sys.argv[2])
pword=(sys.argv[3])

#creates zipfile backup
hostname = socket.gethostname()
today = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")

zf = zipfile.ZipFile("/tmp/%s_%s_logbackup.zip" %(hostname,today) , "w", zipfile.ZIP_DEFLATED)
for dirname, subdirs, files in os.walk("/var/log"):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
zf.close()

#ssh file to remote server
zf_name_path=zf.filename
zf_name_nopath = os.path.basename(zf_name_path)
dest= '/tmp/' + zf_name_nopath

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(logserver, username=uname, password=pword)
sftp = ssh.open_sftp()
sftp.put(zf_name_path,dest)
sftp.close()
ssh.close()
exit()









