num = input().split()
for i in range(len(num)):
    num[i] = int(num[i])
result = []
sign = 0
hh=0
for i in range(num[0]):
    name = input()
    if i+1==num[2] and sign==0:
        sign=1
        result.append(name)
        continue
    elif sign==1:
        hh+=1
        if(hh==num[1]):
            if name not in result:
                result.append(name)
                hh=0
            else:
                hh-=1
                continue
if sign==0:
    print("Keep going...")
else:
    for i in result:
        print(i)
                        
