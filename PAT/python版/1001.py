n = eval(input())
size = 0
while(n!=1):
    if(n%2==0):
        n/=2
    else:
        n = (3*n+1)/2;
    size = size+1
print(size)
    
