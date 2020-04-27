n1 = input()
n2 = input()
n3 = input()
n4 = input()
day = ['MON','TUE','WED','THU','FRI','SAT','SUN']
sign = 1
for i in range(len(n1)):
    if(n1[i].isupper() and n2[i].isupper() and sign==1):
       if(n1[i]==n2[i] and n1[i]>='A' and n1[i]<='G'):
            print(day[ord(n1[i])-ord('A')],end=' ')
            sign=2
    elif(sign==2 and n1[i]==n2[i]):
        if(n1[i].isdigit()):
            print("%02d"%(int(n1[i])),end='')
            break
        elif(n1[i]>='A' and n1[i]<='N'):
            print(ord(n1[i])-ord('A')+10,end='')
            break        
print(':',end='')
for i in range(len(n3)):
    if(n3[i].isalpha() and n4[i].isalpha() and n3[i]==n4[i]):
        print("%02d"%i)
        break

            
                

       
