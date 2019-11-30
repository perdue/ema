import os, sys
thisdir = os.path.dirname(__file__)
libdirs = []
libdirs.append(os.path.join(thisdir, '../'))
libdirs.append(os.path.join(thisdir, '../../crypt'))
libdirs.append(os.path.join(thisdir, '../../config'))

for libdir in libdirs:
    if libdir not in sys.path:
        sys.path.insert(0, libdir)

#print(sys.path)