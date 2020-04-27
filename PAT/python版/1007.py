import math
def Prime(n1,n2):
    cnt = 0;
    ll = []
    i = 2
    cnt = 0
    while(cnt<=num2):
        sign = 0
        for j in range(2,int(math.sqrt(i)+1)):
            if i%j==0:
               sign = 1
               break
        if(sign==0):
            cnt+=1
            if(cnt>=num1 and cnt<=num2):
                ll.append(i)
        i+=1
    if ll:
        print(" ".join(str(ll)))
n = input().split()
num1 = int(n[0])
num2 = int(n[1])
Prime(num1,num2)
