n = int(input())
dir = {}
li = []
for i in range(n):
    a = input().split()
    dir[int(a[2])] = a[0]+' '+a[1]
for key in dir:
    li.append(key)
print(dir[max(li)])
print(dir[min(li)])
