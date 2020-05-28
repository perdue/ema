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

    def gzip_exists(self, filename):
        file_exists = False
        for root, dirs, files in os.walk(self._dir):
            if filename in files:
               file_exists = True

        return file_exists

    def write_gzip(self, content, filename):
        builder.mkdirs(filename)
        print("Writing to 'file:" + filename + "'")
        with gzip.open(filename, 'wb+') as f:
            f.write(content.encode('utf-8'))