n = int(input())
n1 = n//100
n2 = (n-n//100*100)//10
n3 = n%10
str1 = ''
for i in range(n1):
    str1+='B'
for i in range(n2):
    str1+='S'
for i in range(n3):
    str1+=str(i+1)
print(str1)
    
