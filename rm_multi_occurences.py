f = open("data.csv", "r")

array=[]
times=[]
for line in f:
    sp = line.split(",")
    array.append(sp[:-1])
    times.append(sp[-1])

f.close()

k = 0
new_array = []
for i in array:
    #only add data to the new array if 
    #the SCINT1 SCINT2 coincidence and xion data combination is unique
    if i not in new_array:
        new_array.append(i)
    k += 1

f = open("new_data.csv","w")
for i in new_array:
    for j in i:
        f.write(j + ", ")
    f.write("\n")

f.close()
