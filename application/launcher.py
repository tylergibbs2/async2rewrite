import platform
import os


if __name__ == '__main__':
    if platform.system() == 'Linux':
        os.system('nohup ./core.py &')
    elif platform.system() == 'Windows':
        os.system('start pythonw ./core.py')