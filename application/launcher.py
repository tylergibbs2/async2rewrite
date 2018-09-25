import platform
import os


if __name__ == '__main__':
    try:
        if platform.system() == 'Linux':
            os.system('nohup ./core.py &')
        elif platform.system() == 'Windows':
            os.system('start pythonw ./core.py')
    except:
        if platform.system() == 'Linux':
            os.system('python3 ./core.py')
        elif platform.system() == 'Windows':
            os.system('python ./core.py')
