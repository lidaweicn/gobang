from time import localtime

def get_time():
    tm = "{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}"\
        .format(*localtime()[:6])
    return tm

