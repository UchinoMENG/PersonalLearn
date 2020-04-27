import math
def Prime(num,flag):
    p = 2
    while(p<=num):
        for i in range(2*p,num+1,p):
            flag[i] = 0
        while True:
            p+=1
            if(flag[p]==1):
                break
            
n = int(input())
visit = [1]*(n+2)
Prime(n,visit)
cnt = 0
for i in range(5,n+1):
    if(visit[i]==1 and visit[i-2]==1):
        cnt+=1
print(cnt)
