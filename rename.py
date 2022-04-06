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
    filelist = os.listdir(path)
    for files in filelist:                #filelist = 654
        old_dir = os.path.join(path,files);          
        if os.path.isdir(old_dir):
            for file in os.listdir(old_dir):       #files = daishan
                old_name = os.path.join(old_dir,file)
                if os.path.isdir(old_name):             #file = json
                    for label in os.listdir(old_name):
                        old_label = os.path.join(old_name,label)
                        if  os.path.isdir(old_label):
                            for png in os.listdir(os.path.join(old_name,label)):
                                old_png = os.path.join(old_name,label,png)
                                if "label.png" in png:
                                    print("--------------------------------------")
                                    print(old_png)
                                    filename,filetype = os.path.splitext(png)
                                    new_name = r"C:\Users\dell\Desktop\train_data\label\\" + label[:-5] + filetype
                                    os.rename(old_png,new_name)
                                    print("    to   "+ path)
                                    print()

if __name__ == "__main__":
    path = os.getcwd()
    rename(path)