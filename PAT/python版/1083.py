n = input()
dd = {}
num = input().split()
for i in range(len(num)):
    num[i] = abs(int(num[i])-(i+1))
for i in num:
    if i in dd.keys():
        dd[i]+=1
    else:
        dd[i] = 1
tt = list(dd.keys())
tt.sort(reverse = True)
for i in tt:
    if dd[i]>1:
        print(i,dd[i])

