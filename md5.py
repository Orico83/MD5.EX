import hashlib
import multiprocessing
import threading


def decrypt(start, end):
    start = start.zfill(10)
    while start != end:
        result = hashlib.md5(start)
    return result


class MD5:
    def __init__(self, start, end):
        processors = multiprocessing.cpu_count()
        for processor in processors:
            thread = threading.Thread(target=decrypt, args=(start, end))
            thread.start()

