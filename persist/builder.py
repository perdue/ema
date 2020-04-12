import os
from filepersist import LocalDrive
from drivepersist import GoogleDrive

def _build_local(outdir, conf):
    return LocalDrive(outdir)

def _build_drive(outdir, conf):
    return GoogleDrive(outdir, conf)

_switcher = {
    "file": _build_local,
    "drive": _build_drive
}

def mkdirs(name):
    dirname = os.path.dirname(name)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print('Created dir: ' + dirname)

def build_drive(uri, conf):
    drive_type, outdir = uri.split(':', 1)
    build = _switcher.get(drive_type)
    return build(outdir, conf)