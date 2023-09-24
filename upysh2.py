# enhanced upysh file, adds disk usage, du() and tree()
# https://forum.micropython.org/viewtopic.php?t=7550
import sys
import os


# added from reference above
class DISK_USAGE:

    def __repr__(self):
        self.__call__()
        return ""

    def __call__(self, path=".", dlev=0, max_dlev=0, hidden=False):
        if path != ".":
            if not os.stat(path)[0] & 0x4000:
                print('{:9} {}'.format(self.print_filesys_info(os.stat(path)[6]), path))
            else:
                if hidden:
                    resp = {path+'/'+dir: os.stat(path+'/'+dir)[6] for dir in os.listdir(path)}
                else:
                    resp = {path+'/'+dir: os.stat(path+'/'+dir)[6] for dir in os.listdir(path) if not dir.startswith('.')}
                for dir in resp.keys():

                    if not os.stat(dir)[0] & 0x4000:
                        print('{:9} {}'.format(self.print_filesys_info(resp[dir]), dir))

                    else:
                        if dlev < max_dlev:
                            dlev += 1
                            self.__call__(path=dir, dlev=dlev, max_dlev=max_dlev, hidden=hidden)
                            dlev += (-1)
                        else:
                            print('{:9} {} {}'.format(self.print_filesys_info(self.get_dir_size_recursive(dir)), dir, '<dir>'))
        else:
            if hidden:
                resp = {path+'/'+dir: os.stat(path+'/'+dir)[6] for dir in os.listdir(path)}
            else:
                resp = {path+'/'+dir: os.stat(path+'/'+dir)[6] for dir in os.listdir(path) if not dir.startswith('.')}
            for dir in resp.keys():

                if not os.stat(dir)[0] & 0x4000:
                    print('{:9} {}'.format(self.print_filesys_info(resp[dir]), dir))

                else:
                    if dlev < max_dlev:
                        dlev += 1
                        self.__call__(path=dir, dlev=dlev, max_dlev=max_dlev, hidden=hidden)
                        dlev += (-1)
                    else:
                        print('{:9} {} {}'.format(self.print_filesys_info(self.get_dir_size_recursive(dir)), dir, '<dir>'))

    def print_filesys_info(self, filesize):
        _kB = 1024
        if filesize < _kB:
            sizestr = str(filesize) + " by"
        elif filesize < _kB**2:
            sizestr = "%0.1f KB" % (filesize / _kB)
        elif filesize < _kB**3:
            sizestr = "%0.1f MB" % (filesize / _kB**2)
        else:
            sizestr = "%0.1f GB" % (filesize / _kB**3)
        return sizestr

    def get_dir_size_recursive(self, dir):
        return sum([os.stat(dir+'/'+f)[6] if not os.stat(dir+'/'+f)[0] & 0x4000 else self.get_dir_size_recursive(dir+'/'+f) for f in os.listdir(dir)])


# added from reference above
class TREE:

    def __repr__(self):
        self.__call__()
        return ""

    def __call__(self, path=".", level=0, is_last=False, is_root=True,
                 carrier="    "):
        l = os.listdir(path)
        nf = len([file for file in os.listdir(path) if not os.stat(file)[0] & 0x4000])
        nd = len(l) - nf
        ns_f, ns_d = 0, 0
        l.sort()
        if len(l) > 0:
            last_file = l[-1]
        else:
            last_file = ''
        for f in l:
            st = os.stat("%s/%s" % (path, f))
            if st[0] & 0x4000:  # stat.S_IFDIR
                print(self._treeindent(level, f, last_file, is_last=is_last, carrier=carrier) + "  %s <dir>" % f)
                os.chdir(f)
                level += 1
                lf = last_file == f
                if level > 1:
                    if lf:
                        carrier += "     "
                    else:
                        carrier += "    │"
                ns_f, ns_d = self.__call__(level=level, is_last=lf,
                                           is_root=False, carrier=carrier)
                if level > 1:
                    carrier = carrier[:-5]
                os.chdir('..')
                level += (-1)
                nf += ns_f
                nd += ns_d
            else:
                print(self._treeindent(level, f, last_file, is_last=is_last, carrier=carrier) + "  %s" % (f))
        if is_root:
            print('{} directories, {} files'.format(nd, nf))
        else:
            return (nf, nd)

    def _treeindent(self, lev, f, lastfile, is_last=False, carrier=None):
        if lev == 0:
            return ""
        else:
            if f != lastfile:
                return carrier + "    ├────"
            else:
                return carrier + "    └────"


class LS:
    def __repr__(self):
        self.__call__()
        return ""

    def __call__(self, path="."):
        l = list(os.ilistdir(path))
        l.sort()
        for f in l:
            if f[1] == 0x4000:  # stat.S_IFDIR
                print("    <dir> %s" % f[0])
        for f in l:
            if f[1] != 0x4000:
                if len(f) > 3:
                    print("% 9d %s" % (f[3], f[0]))
                else:
                    print("          %s" % f[0])
        try:
            st = os.statvfs(path)
            print("\n{:,d}k free".format(st[1] * st[3] // 1024))
        except:
            pass


class PWD:
    def __repr__(self):
        return os.getcwd()

    def __call__(self):
        return self.__repr__()


class CLEAR:
    def __repr__(self):
        return "\x1b[2J\x1b[H"

    def __call__(self):
        return self.__repr__()


def head(f, n=10):
    with open(f) as f:
        for i in range(n):
            l = f.readline()
            if not l:
                break
            sys.stdout.write(l)


def cat(f):
    head(f, 1 << 30)


def cp(s, t):
    try:
        if os.stat(t)[0] & 0x4000:  # is directory
            t = t.rstrip("/") + "/" + s
    except OSError:
        pass
    buf = bytearray(512)
    buf_mv = memoryview(buf)
    with open(s, "rb") as s, open(t, "wb") as t:
        while True:
            n = s.readinto(buf)
            if n <= 0:
                break
            t.write(buf_mv[:n])


def newfile(path):
    print("Type file contents line by line, finish with EOF (Ctrl+D).")
    with open(path, "w") as f:
        while 1:
            try:
                l = input()
            except EOFError:
                break
            f.write(l)
            f.write("\n")


def rm(d, recursive=False):  # Remove file or tree
    try:
        if (os.stat(d)[0] & 0x4000) and recursive:  # Dir
            for f in os.ilistdir(d):
                if f[0] != "." and f[0] != "..":
                    rm("/".join((d, f[0])))  # File or Dir
            os.rmdir(d)
        else:  # File
            os.remove(d)
    except:
        print("rm of '%s' failed" % d)


class Man:
    def __repr__(self):
        return """
upysh is intended to be imported using:
from upysh import *

To see this help text again, type "man".

upysh2 commands:
clear, ls, ls(...), head(...), cat(...), newfile(...)
cp('src', 'dest'), mv('old', 'new'), rm(...)
pwd, cd(...), mkdir(...), rmdir(...), du(...), tree(...)
"""


man = Man()
pwd = PWD()
ls = LS()
clear = CLEAR()
du = DISK_USAGE()
tree = TREE()

cd = os.chdir
mkdir = os.mkdir
mv = os.rename
rmdir = os.rmdir

print(man)
