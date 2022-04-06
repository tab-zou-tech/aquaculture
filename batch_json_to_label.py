import os

path = os.getcwd()
pathDir_new = os.listdir(path)
# pathDir_old = os.listdir('E:\data\lansat\jpg_label') 
i = 0
for filds in pathDir_new:
    if "." not in filds:
        os.chdir(path+"\\"+filds)
        print(filds)
        for tif in os.listdir(path+"\\"+filds): 
            if '.'  in tif :
                filename , filetype = tif.split('.')[0] , tif.split('.')[1]
                if filetype == 'json':
                    filename_new = filename + '_' + filetype
                    if filename_new in pathDir_new:
                        print("----------------------------------")
                        print(filename_new+" has been conversion!")
                    else:
                        print(filename_new,'can do')
                        cmd = "labelme_json_to_dataset "+filename+".json "
                        print("----------------------------------")
                        print(cmd)
                        try:
                           result = os.system(cmd)
                        except:
                            print("failed")
                        else:
                            print("next!")
                            i = i + 1
                else:
                    print("----------------------------------")
                    print("Dont Need File Conversion: "+filename+'.'+filetype)
print("----------------------------------")
print("Number of files success : ", i)
print('file conversion has been finished')