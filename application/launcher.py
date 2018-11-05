import platform
import os
from application import core


def setup():
    if platform.system() == 'Linux':
        os.system('nohup {} &'.format(os.path.realpath(core.__file__)))
    elif platform.system() == 'Windows':
        os.system('start pythonw {}'.format(os.path.realpath(core.__file__)))
