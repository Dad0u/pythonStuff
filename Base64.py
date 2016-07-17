base64_list = []
for i in range(26):
    base64_list.append(chr(65+i))
for i in range(26):
    base64_list.append(chr(97+i))
for i in range(0,10):
    base64_list.append(str(i))
base64_list.extend(['+','/','='])
base64_dict = dict()

for i in range(65):
    base64_dict[base64_list[i]] = i
    
def toBase64(by):
    out = ''
    fin = len(by)%3
    for i,j,k in zip(by[0::3], by[1::3], by[2::3]):
        out += base64_list[i>>2]
        out += base64_list[((i&3)<<4)+(j>>4)]
        out += base64_list[((j&15)<<2)+(k>>6)]
        out += base64_list[k&63]
    if fin == 1:
        out += base64_list[by[-1]>>2]
        out += base64_list[((by[-1]&3)<<4)]
        out += '=='
    elif fin == 2:
        out += base64_list[by[-2]>>2]
        out += base64_list[((by[-2]&3)<<4)+(by[-1]>>4)]
        out += base64_list[((by[-1]&15)<<2)]
        out += '='
    return out

def bytesFromBase64(s):
    if len(s)%4 == 1:
        print("Invalid length !")
        return None
    elif len(s)%4 == 2:
        s += '=='
    elif len(s)%4 == 3:
        s += '='
    out = b''
    for i,j,k,l in zip(s[0::4], s[1::4], s[2::4], s[3::4]):
        i,j,k,l = base64_dict[i],base64_dict[j],base64_dict[k],base64_dict[l]
        if l != 64:
            out += bytes([(i<<2)+(j>>4)])
            out += bytes([((j&15)<<4)+(k>>2)])
            out += bytes([((k&3)<<6)+(l)])
        elif k != 64:
            out += bytes([(i<<2)+(j>>4)])
            out += bytes([((j&15)<<4)+(k>>2)])
        else:
            out += bytes([(i<<2)+(j>>4)])
    return out
