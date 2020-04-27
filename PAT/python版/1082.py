n = int(input())
ll = []
for i in range(n):
    peo={}
    temp = input().split()
    n = int(temp[1])**2+int(temp[2])**2
    peo[n] = temp[0]
    ll.append(peo)
print(ll)

