def lfsr(binary_seed):
    if len(binary_seed) < 8:
        rem = 8 - len(binary_seed)
        binary_seed = '0' * rem + binary_seed
    else:
        binary_seed = binary_seed[0:8]
    if binary_seed[0] == '0':
        binary_seed = binary_seed + binary_seed[0]
        binary_seed = binary_seed[1:9]
        return int(binary_seed, 2)
        
    elif binary_seed[0] == '1':
        binary_seed1 = ""
        if binary_seed[5] == '0':
            binary_seed1 = binary_seed1 + '1'
        else:
            binary_seed1 = binary_seed1 + '0'

        if binary_seed[4] == '0':
            binary_seed1 = binary_seed1 + '1'
        else:
            binary_seed1 = binary_seed1 + '0'

        if binary_seed[3] == '0':
            binary_seed1 = binary_seed1 + '1'
        else:
            binary_seed1 = binary_seed1 + '0'

        binary_seed = binary_seed + binary_seed[0]
        binary_seed = binary_seed[1:9]
        binary_seed1 = binary_seed[0:3] + binary_seed1 + binary_seed[6:8]
    else:
        return "Invalid input"
    return int(binary_seed1, 2)


