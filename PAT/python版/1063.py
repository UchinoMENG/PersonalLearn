import math
n = eval(input())
mm = 0
for i in range(n):
    num = input().split()
    temp = pow(int(num[0]),2)+pow(int(num[1]),2)
    if temp>mm:
        mm = temp
print("%.2f"%math.sqrt(mm))
    
