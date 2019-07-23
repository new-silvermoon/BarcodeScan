
L_dict = {
    "0001101": 0,
    "0011001": 1,
    "0010011": 2,
    "0111101": 3,
    "0100011": 4,
    "0110001": 5,
    "0101111": 6,
    "0111011": 7,
    "0110111": 8,
    "0001011": 9
}

G_dict = {
    "0100111": 0,
    "0110011": 1,
    "0011011": 2,
    "0100001": 3,
    "0011101": 4,
    "0111001": 5,
    "0000101": 6,
    "0010001": 7,
    "0001001": 8,
    "0010111": 9
}
R_dict = {
    "1110010": 0,
    "1100110": 1,
    "1101100": 2,
    "1000010": 3,
    "1011100": 4,
    "1001110": 5,
    "1010000": 6,
    "1000100": 7,
    "1001000": 8,
    "1110100": 9
}

first_six_digits = {
    1: L_dict,
    2: G_dict,
    3: L_dict,
    4: G_dict,
    5: G_dict,
    6: L_dict
}

def decode(bar_widths):
    global L_dict,G_dict,R_dict,first_six_digits

    #Decoding
    count = 0
    for i in range(3, len(bar_widths),4):
        count+=1
        widths = bar_widths[i:i+4]
        if count <= 6:
            code = ""
            for j,val in enumerate(widths):
                code += '1' * val if (j+1) % 2 ==0 else '0'*val
            mode_dict = first_six_digits.get(count)

            #print(code)
            print(mode_dict.get(code))
        else:
            code = ""
            for j, val in enumerate(widths):
                code += '0' * val if (j + 1) % 2 == 0 else '1' * val
            #print(code)
            print(R_dict.get(code))



