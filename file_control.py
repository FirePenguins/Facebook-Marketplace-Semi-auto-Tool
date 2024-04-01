import os
import shutil

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        return True
    else:
        return False

def create_file(file_path):
    with open(file_path,mode='a+',encoding='utf-8') as cf:
        pass

def update_file(file_path,content):
    with open(file_path,mode='a+',encoding='utf-8') as cf:
        pass

def filestatus(filename):#文件存在且不为空则为真
    return os.stat(filename).st_size != 0 and os.path.exists(filename)

def show_dir(dir_path):#展示当前目录下的所有文件夹
    subdirLists = []
    for root, dirs, files in os.walk(dir_path):
        if os.path.abspath(root)==os.path.abspath(dir_path):
            for dir_name in dirs:
                subdirLists.append(dir_name)
            break
    return subdirLists

def move_file(src,dst):
    pass

def copy_file(src,dst):
    shutil.copy(src,dst)

def removedir(path):
    shutil.rmtree(path)

def DirFile_creation(dir_list=[],file_list=[]):
    for i in dir_list:
        create_dir(i)
    for i in file_list:
        create_file(i)