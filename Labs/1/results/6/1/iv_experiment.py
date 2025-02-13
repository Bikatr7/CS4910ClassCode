import subprocess
import os

def encrypt_with_iv(plaintext, output_file, iv, key="00112233445566778889aabbccddeeff"):
    """Encrypt plaintext using CBC mode with specified IV"""
    with open('temp.txt', 'w') as f:
        f.write(plaintext)
    
    cmd = [
        'openssl', 'enc',
        '-aes-128-cbc',
        '-e',
        '-in', 'temp.txt',
        '-out', output_file,
        '-K', key,
        '-iv', iv
    ]
    
    subprocess.run(cmd, check=True)
    os.remove('temp.txt')

def main():
    PLAINTEXT = "This is a secret message that we will encrypt multiple times!"
    IV1 = "0102030405060708"
    IV2 = "0102030405060709"  ## Different last byte
    
    ## Test 1: Same plaintext, different IVs
    encrypt_with_iv(PLAINTEXT, 'cipher1.bin', IV1)
    encrypt_with_iv(PLAINTEXT, 'cipher2.bin', IV2)
    
    ## Test 2: Same plaintext, same IV
    encrypt_with_iv(PLAINTEXT, 'cipher3.bin', IV1)
    
    with open('cipher1.bin', 'rb') as f1, \
         open('cipher2.bin', 'rb') as f2, \
         open('cipher3.bin', 'rb') as f3:
        c1 = f1.read()
        c2 = f2.read()
        c3 = f3.read()
        
        print("\nResults:")
        print("Different IVs - ciphertexts match?", c1 == c2)
        print("Same IV - ciphertexts match?", c1 == c3)
    
    os.remove('cipher1.bin')
    os.remove('cipher2.bin')
    os.remove('cipher3.bin')

if(__name__ == "__main__"):
    main() 