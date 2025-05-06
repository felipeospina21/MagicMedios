import os

if os.name == "nt":
    import msvcrt

    def lock_file(f):
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)

    def unlock_file(f):
        f.seek(0)
        msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)

else:
    import fcntl

    def lock_file(f):
        fcntl.flock(f, fcntl.LOCK_EX)

    def unlock_file(f):
        fcntl.flock(f, fcntl.LOCK_UN)
