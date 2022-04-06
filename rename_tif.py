import os
 
def remove_file(old_path, new_path):
    print(old_path)
    print(new_path)
    filelist = os.listdir(old_path) #列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
    print(filelist)
    for file in filelist:
        src = os.path.join(old_path, file)
        dst = os.path.join(new_path, file)
        print('src:', src)
        print('dst:', dst)
        shutil.move(src, dst)
 
def rename(path):
    old_name = os.listdir(path)
    for label in old_name:
        old_label = os.path.join(path,label)
        if  os.path.isdir(old_label):
            for png in os.listdir(os.path.join(old_label)):
                old_png = os.path.join(old_label,png)
                print(old_png)
                if ".json" in png:
                    print("--------------------------------------")
                    print(old_png)
                    filename,filetype = os.path.splitext(png)
                    new_name = os.path.join(old_label,label+"_"+filename+filetype)
                    os.rename(old_png,new_name)
                    print("    to   "+ new_name)
                    print()

if __name__ == "__main__":
    path = os.getcwd()
    rename(path)