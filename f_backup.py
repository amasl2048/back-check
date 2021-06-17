#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil

import hashlib

def get_dir(dir_name: str) -> list:
    '''
    Get file names list for remote dir
    '''
    out = []
    flist = os.listdir(dir_name)  #;print(dir_name, flist)

    for fl in flist:
        fname = os.path.join(dir_name, fl)
        if os.path.isfile(fname) and not ".bak" in fl[-4:]:
            out.append(fname)

    return out


def av_files(DEST_DIRS: list) -> dict:
    '''
    Return dict with avalible files for each destination
    '''

    w_dirs = {}

    for dr in DEST_DIRS:

        if os.path.exists(dr):
            w_dirs[dr] = []
        else:
            print("\nDirectory %s not available:", dr)

    for dr in w_dirs:
        w_dirs[dr] = w_dirs[dr] + get_dir(dr)

    return w_dirs


def f_path(full_name: str) -> tuple:
    '''
    return file name and path
    '''
    fname = full_name.strip()
    fl = os.path.basename(fname)
    path = os.path.dirname(fname)

    return fl, path


def create_md5(f_name: str):
    '''
    check mod time & md5
    '''
    if os.path.exists(f_name):

        t = os.path.getmtime(f_name)
        tm = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(t))

        # md5sum
        newfile = open(f_name, "rb")
        content = newfile.read()
        newfile.close()

        m = hashlib.md5()
        m.update(content)
        h = m.hexdigest()

    else:
        print("Error: %s - Not exist!" % f_name)
        sys.exit(0)

    return t, tm, h


def f_dat(BACKUP_FILES: list) -> dict:
    '''
    Create dict with data for each file from list
    '''

    file_dat = {}

    for full_name in BACKUP_FILES:

        fl, path = f_path(full_name.strip())

        file_dat[fl] = {}
        file_dat[fl]["path"] = path
        file_dat[fl]["utime"], file_dat[fl]["mtime"], file_dat[fl]["md5"] = create_md5(full_name.strip())

    return file_dat


def logrotate(fl_name, depth, dest_dir) -> None:
    '''
    rename remote files with .x.bak
    '''
    # create backup
    old = "bak"
    remote_file = dest_dir + "/" + fl_name  #+ ".xz"

    for i in range(depth, 1, -1):
        old_remote_file1 = "%s.%s.%s" % (remote_file, str(i-1), old)
        old_remote_file2 = "%s.%s.%s" % (remote_file, str(i), old)
        if os.path.exists(old_remote_file2):
            os.remove(old_remote_file2)
        if os.path.exists(old_remote_file1):
            os.rename(old_remote_file1, old_remote_file2)

    old_remote_file = "%s.%s.%s" % (remote_file, str(1), old)
    os.rename(remote_file, old_remote_file)


def cp(fl_name, local_dir, dest_dir) -> None:
    '''
    copy new file to dest
    '''
    local_file = os.path.join(local_dir, fl_name)
    shutil.copy2(local_file, dest_dir)
    print("copied %s \n" % fl_name)
