import platform
import os


if __name__ == '__main__':
    if platform.system() == 'Linux':
        os.system('python3 ./core.py')
    elif platform.system() == 'Windows':
        os.system('python ./core.py')
