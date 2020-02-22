import ctypes
import threading


class Thread(threading.Thread):

    def terminate(self):
        self.raise_exc(SystemExit)

    def raise_exc(self, exctype):
        self._async_raise(exctype)

    def _async_raise(self, exctype):
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")
        tid = ctypes.c_long(self.ident)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")
