n = int(input())
dir = {}
for i in range(n):
    s = input().split()
    dir[s[0]] = s[1]
a = input()
num = set(input().split())
for k,v in dir.items():
    if((k in num) and (v in num)):
        num.remove(k)
        num.remove(v)
num = list(num)
num.sort()
sign = 0
print(len(num))
if num:
  print(" ".join(num))
