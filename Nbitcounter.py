def decimalToBinary(n): 
    return bin(n).replace("0b","")

def Nbitcounter(N,S):
    x=S
    count=0
    for i in range(255):
        b=decimalToBinary(x)
        rem=N-len(b)
        b='0'*rem + b
        print(b)
        x+=1
        count+=1
Nbitcounter(10,10)
