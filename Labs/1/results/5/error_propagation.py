import subprocess
import os

def create_test_file(filename, size=1000):
    """Create a test file of 1000 bytes"""
    with open(filename, 'w') as f:
        content = ''.join(chr((i % 26) + 65) for i in range(size))
        f.write(content)
    print(f"Created {filename} with size {len(content)} bytes")

def corrupt_byte(filename, position=54):
    """Corrupt a single bit in the specified byte"""
    with open(filename, 'rb') as f:
        data = bytearray(f.read())
    
    ## Flip the least significant bit of the specified byte
    data[position] ^= 1
    
    with open(filename, 'wb') as f:
        f.write(data)
    print(f"Corrupted bit in byte {position} of {filename}")

def test_mode(mode, input_file):
    """Test error propagation for a specific mode"""
    KEY = "00112233445566778889aabbccddeeff"
    IV = "0102030405060708"
    
    print(f"\nTesting {mode.upper()} mode:")
    print("-" * 50)
    
    encrypted = f"encrypted_{mode}.bin"
    cmd_encrypt = [
        'openssl', 'enc',
        f'-aes-128-{mode}',
        '-e',
        '-in', input_file,
        '-out', encrypted,
        '-K', KEY,
        '-iv', IV
    ]
    
    decrypted = f"decrypted_{mode}.txt"
    cmd_decrypt = [
        'openssl', 'enc',
        f'-aes-128-{mode}',
        '-d',
        '-in', encrypted,
        '-out', decrypted,
        '-K', KEY,
        '-iv', IV
    ]
    
    try:
        subprocess.run(cmd_encrypt, check=True)

        corrupt_byte(encrypted, 54)
        
        subprocess.run(cmd_decrypt, check=True)
        
        with open(input_file, 'rb') as f1, open(decrypted, 'rb') as f2:
            original = f1.read()
            corrupted = f2.read()
            
            differences = []
            for i, (o, c) in enumerate(zip(original, corrupted)):
                if(o != c):
                    differences.append(i)
            
            print(f"Affected bytes: {len(differences)}")
            print(f"First affected byte: {min(differences) if differences else 'None'}")
            print(f"Last affected byte: {max(differences) if differences else 'None'}")
        
        os.remove(encrypted)
        os.remove(decrypted)
        
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    input_file = "plaintext.txt"
    
    create_test_file(input_file)
    
    modes = ['ecb', 'cbc', 'cfb', 'ofb']
    for mode in modes:
        test_mode(mode, input_file)
    
    os.remove(input_file)

if(__name__ == "__main__"):
    main() 