file_path = r"C:\Users\dell\Desktop\demo\20220402_1358.log"
fp = open(file_path)
print("open the file " + file_path)
year_area = 0
year_index = "year"
test_ten = ["daishan","liuheng","jintang","qushan","sijiao","taohua","tushan","xiushan","zhoushan","zhujiajian","index"]
train_ten = ["index","liuheng","subset","zhujiajian"]
for line in fp.readlines():
    noread = 0
    for index in test_ten:
        if index in line:
            noread = 1
            break
    if noread:
        continue
    elif "file" in line:
        result = line[60:]
        year = result[7:16]
        area = float(result.split("=")[-1])
        if year_index != year:
            with open("E:\\result3.txt","a") as fp2:
                areas = year_area
                fp2.write(year_index+" area="+str(areas)+"\n")
            print(year_index + " is finish!")
            print()
            year_index = year
            year_area = 0
        year_area = year_area + area
with open("E:\\result3.txt","a") as fp2:
    fp2.write(year_index+" area="+str(year_area)+"\n")       
print(year_index + " is finish!")    
fp.close()