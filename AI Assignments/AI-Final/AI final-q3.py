numbers=[10,-5,0,8,-2,0]
positive_count=0
negative_count=0
zero_count=0

for num in numbers:
    if num>0:
        positive_count+=1
    elif num<0:
        negative_count+=1
    else:
        zero_count+=1
print("Positive :",positive_count,"Negative:",negative_count,"Zero:",zero_count)