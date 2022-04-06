import shutil
import os
 
def remove_file(old_path, new_path):
    filelist = os.listdir(old_path) #列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
    for dirs in filelist:
        old_dir = os.path.join(old_path,dirs)
        print(old_dir)
        if os.path.isdir(old_dir):
            for files in os.listdir(old_dir):
                old_file = os.path.join(old_dir,files)
                if os.path.isdir(old_file):
                    file_name = files[:-5]+".tif"
                    old_tif = os.path.join(old_dir,file_name)
                    print(old_tif)
                    dst = os.path.join(new_path,file_name)
                    print(dst)
                    shutil.move(old_tif, dst)
 
if __name__ == '__main__':
    path = os.getcwd()
    remove_file(path, r"C:\Users\dell\Desktop\image")