import os
signals = None

# HACKED TO JUST GET IT WORKING THE WAY I NEED - DO NOT USE
SIGNAL_SUPPORT = False

def exec_hook(hook_name, self, *args, **kwargs):
    pass

def hooks(fn):

    def hooked(self, *args, **kwargs):
        fn_name = fn.func_name if hasattr(fn, 'func_name') else fn.__name__


        val = fn(self, *args, **kwargs)



        return val

    return hooked