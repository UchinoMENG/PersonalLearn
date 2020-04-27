num1 = ['tret','jan','feb', 'mar', 'apr', 'may', 'jun', 'jly', 'aug', 'sep', 'oct',
        'nov', 'dec']
num2 = ['','tam', 'hel', 'maa', 'huh', 'tou', 'kes', 'hei'
        , 'elo', 'syy', 'lok', 'mer', 'jou']
n = int(input())
for i in range(n):
    temp = input()
    one = 0
    two = 0
    if temp.isdigit():
        temp = int(temp)
        one = temp//13
        two = temp%13
        if(one==0 ):
            print(num1[two])
        elif two==0:
            print(num2[one])
        else:
            print(num2[one],num1[two])
    else:
        temp = temp.split()
        if len(temp)==2:
            one = num2.index(temp[0])
            two = num1.index(temp[1])
        else:
            if temp[0] in num1:
                two = num1.index(temp[0])
            else:
                one = num2.index(temp[0])
        print((one)*13+two)
        
        
    
