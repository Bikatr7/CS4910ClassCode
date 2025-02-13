def xor(first, second):
    """XOR two bytearrays"""
    return bytearray(x^y for x,y in zip(first, second))

def decrypt_ofb(p1, c1, c2):
    """Decrypt C2 using known P1 and C1 in OFB mode"""
    c1_bytes = bytearray.fromhex(c1)
    c2_bytes = bytearray.fromhex(c2)
    p1_bytes = bytes(p1, 'utf-8')
    
    ## In OFB mode, C = P ⊕ keystream
    # So, keystream = P ⊕ C
    keystream = xor(p1_bytes, c1_bytes)
    
    ## Since same IV means same keystream,
    ## P2 = C2 ⊕ keystream
    p2_bytes = xor(c2_bytes, keystream)
    
    return p2_bytes.decode('utf-8')

def main():
    P1 = "This is a known message!"
    C1 = "a469b1c502c1cab966965e50425438e1bb1b5f9037a4c159"
    C2 = "bf73bcd3509299d566c35b5d450337e1bb175f903fafc159"
    
    P2 = decrypt_ofb(P1, C1, C2)
    print(f"Decrypted P2: {P2}")

if(__name__ == "__main__"):
    main() 