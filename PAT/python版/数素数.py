import math
def Prime(num1,num2):
    visit = [0]*110000
    print(visit)
    n = 2
    visit[2] = 1
    while(n<=110000):
        for i in range(2*n,110000,n):
            visit[i] = 1
        while True:
            n+=1
            if visit[n]==1:
                break
    for i in range(110000):
        if(visit[i]==1):
            cnt+=1
        if cnt>=num1 and cnt<=num2:
            print(i,end=' ')
        if(cnt>num2):
            break
    
n = input().split()
num1 = int(n[0])
num2 = int(n[1])
Prime(num1,num2)
