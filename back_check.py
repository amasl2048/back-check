#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Backup and check
    - checking files time, md5
    - log rotate
'''
import os
import shutil
import time

import yaml
from yaml.loader import SafeLoader

import f_backup

print("\nStarting... \n--- ", time.strftime("%A, %d. %B %Y %H:%M"))

dep = 5  # log rotate depth

with open("backup_cfg.yml", "r") as yml:
    DEST_DIRS = yaml.load(yml, Loader=SafeLoader)["dest_dirs"]  # config remote dirs

DEST_DIRS.sort()

with open("backup.list", "r") as bk:
    BACKUP_FILES = bk.readlines()  # list of files to backup

BACKUP_FILES.sort()

result = ""
template = '''%s:
    path: %s
    utime: %s
    mtime: %s
    md5: %s
'''

def check_files(dr, files_list, file_dat) -> None:

    global result

    for fl in file_dat.keys():

        # check mod time & md5
        full_name = os.path.join(dr, fl)
        if os.path.exists(full_name):

            t, tm, h = f_backup.create_md5(full_name)

            if round(file_dat[fl]["utime"],2) < round(t,2):  # t - should be round 2
                print("| %s\t | %s | ->  | %s |" % (fl, file_dat[fl]["mtime"], tm))

            if file_dat[fl]["md5"] != h:
                print("| %s\t | %s | -> | %s |" % (fl, file_dat[fl]["md5"], h))
                f_backup.logrotate(fl, dep, dr)
                f_backup.cp(fl, file_dat[fl]["path"], dr)

            else:
                print("| %s\t | %s | == | %s |" % (fl, file_dat[fl]["md5"], h))

            result = result + template % (fl, dr, t, tm, h)

        else:
            f_backup.cp(fl, file_dat[fl]["path"], dr)


print("\nCheck remote and copy files...")
w_dirs = f_backup.av_files(DEST_DIRS)

for dr in w_dirs.keys():

    print(dr)
    for fn in BACKUP_FILES:

        fl, path = f_backup.f_path(fn.strip())
        remote_file = os.path.join(dr, fl)

        if not os.path.exists(remote_file):

            shutil.copy2(fn.strip(), dr)
            w_dirs[dr].append(remote_file)
            print("-> copied %s \n" % remote_file)

print("\nCheck md5sums...")
file_dat = f_backup.f_dat(BACKUP_FILES)

for dr in w_dirs.keys():

    print("\n", dr)
    check_files(dr, w_dirs[dr], file_dat)

print("\n", result)
print("Done.")


