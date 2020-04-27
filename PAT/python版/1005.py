visit = [0 for i in range(10000)]
li = []
n = int(input())
num = input().split()
for i in range(len(num)):
    num[i] = int(num[i])
for i in range(len(num)):
    nn = num[i]
    if(visit[nn]==1):
        continue
    else:
        while(nn!=1):
            if(nn%2==0):
                nn//=2
            else:
                nn = (nn*3+1)//2        #/的话会将nn变为double型
            visit[nn] = 1
num.sort(reverse = True)
sign = 0
for i in num:
    if(visit[i]==0):
        if(sign!=0):
            print(end=' ')
        sign = 1
        print(i,end='')
        
    
