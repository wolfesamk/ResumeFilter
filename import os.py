li1 = [10, 15, 20, 25, 30, 35, 40]
li2 = [25, 40, 35]
 
temp3 = []
for element in li1:
    if element not in li2:
        temp3.append(element)
 
print(temp3)