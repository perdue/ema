import os
import io
import gzip
import builder

"""Local file access"""

class LocalDrive:
    def __init__(self, persist_dir):
        self._dir = persist_dir
        builder.mkdirs(self._dir)

    def outdir(self):
        return self._dir

    def write(self, content, filename):
        gzip_fn = filename + '.gz'
        builder.mkdirs(gzip_fn)
        print("Writing to 'file:" + gzip_fn + "'")
        with gzip.open(gzip_fn, 'wb+') as f:
            f.write(content.encode('utf-8'))