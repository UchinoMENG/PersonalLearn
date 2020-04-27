n = input().split()
n.reverse()
sign =1;
for i in range(len(n)):
    if(sign==0):
        print(end=' ')
    sign = 0
    print(n[i],end='')
