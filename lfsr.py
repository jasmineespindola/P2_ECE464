def lfsr(S):
    if(len(S)!=8):
        return "Invalid Input"
        
    elif(S[7] == '0'):
        print(S[7])
        S=S[7]+S
        S=S[0:7]
        
    elif(S[7] == '1'):
        S1=""
        if(S[1]=='0'):
            S1=S1+'1'
        else:
            S1=S1+'0'

        if(S[2]=='0'):
            S1=S1+'1'
        else:
            S1=S1+'0'

        if(S[3]=='0'):
            S1=S1+'1'
        else:
            S1=S1+'0'
        
        S1=S[7]+S1
        S1=S1+S[3:7]
    else:
        return "Invalid input"
    return S1

            
        
    
        
        
    
