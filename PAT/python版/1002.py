sign = ["ling","yi","er","san","si","wu","liu","qi","ba","jiu"]
num = input()
sum = 0
for i in num:
    sum+=int(i)
string = str(sum)
length = len(string)

for i in string:
    print(sign[int(i)],end='')
    length=length-1
    if(length>0):
        print(end=' ')

