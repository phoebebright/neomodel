import os
signals = None
try:
    if not 'DJANGO_SETTINGS_MODULE' in os.environ:
        from django.conf import settings
        settings.configure()
        SIGNAL_SUPPORT = settings.SIGNAL_SUPPORT
    else:
        from django.db.models import signals
        SIGNAL_SUPPORT = True
except ImportError:
    SIGNAL_SUPPORT = False


def exec_hook(hook_name, self, *args, **kwargs):
    if SIGNAL_SUPPORT:
        if hasattr(self, hook_name):
            getattr(self, hook_name)(*args, **kwargs)
        if signals and hasattr(signals, hook_name):
            sig = getattr(signals, hook_name)
            sig.send(sender=self.__class__, instance=self)


def hooks(fn):

    def hooked(self, *args, **kwargs):
        fn_name = fn.func_name if hasattr(fn, 'func_name') else fn.__name__

        if SIGNAL_SUPPORT:
            exec_hook('pre_' + fn_name, self, *args, **kwargs)

        val = fn(self, *args, **kwargs)

        if SIGNAL_SUPPORT:
            exec_hook('post_' + fn_name, self, *args, **kwargs)

        return val

    return hooked