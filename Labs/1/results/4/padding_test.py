import subprocess
import os

def create_test_files():
    """Create test files of different sizes"""
    files = {
        'f1.txt': '12345',          ## 5 bytes
        'f2.txt': '1234567890',     ## 10 bytes
        'f3.txt': '1234567890123456' ## 16 bytes
    }
    
    for filename, content in files.items():
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Created {filename} with size {len(content)} bytes")

def test_encryption_modes(input_file):
    """Test different encryption modes on a file"""
    KEY = "00112233445566778889aabbccddeeff"
    IV = "0102030405060708"
    
    modes = ['ecb', 'cbc', 'cfb', 'ofb']
    
    print(f"\nTesting encryption modes on {input_file}:")
    print("-" * 50)
    
    for mode in modes:
        output = f"encrypted_{mode}.bin"
        cmd = [
            'openssl', 'enc',
            f'-aes-128-{mode}',
            '-e',
            '-in', input_file,
            '-out', output,
            '-K', KEY,
            '-iv', IV
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            size = os.path.getsize(output)
            print(f"{mode.upper()}: Output size = {size} bytes")
            os.remove(output)
        except Exception as e:
            print(f"Error with {mode}: {str(e)}")

def examine_padding(filename):
    """Examine padding by encrypting and decrypting without padding removal"""
    KEY = "00112233445566778889aabbccddeeff"
    IV = "0102030405060708"
    
    print(f"\nExamining padding for {filename}:")
    print("-" * 50)
    
    encrypted = f"{filename}_encrypted.bin"
    cmd_encrypt = [
        'openssl', 'enc',
        '-aes-128-cbc',
        '-e',
        '-in', filename,
        '-out', encrypted,
        '-K', KEY,
        '-iv', IV
    ]
    
    decrypted = f"{filename}_decrypted.bin"
    cmd_decrypt = [
        'openssl', 'enc',
        '-aes-128-cbc',
        '-d',
        '-nopad',
        '-in', encrypted,
        '-out', decrypted,
        '-K', KEY,
        '-iv', IV
    ]
    
    try:
        subprocess.run(cmd_encrypt, check=True)
        enc_size = os.path.getsize(encrypted)
        print(f"Encrypted size: {enc_size} bytes")
        
        subprocess.run(cmd_decrypt, check=True)
        
        result = subprocess.run(['xxd', decrypted], capture_output=True, text=True)
        print("\nHex dump of decrypted file (with padding):")
        print(result.stdout)
        
        os.remove(encrypted)
        os.remove(decrypted)
        
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    create_test_files()
    
    test_encryption_modes('f2.txt')  ## Using 10-byte file for mode testing
    
    for filename in ['f1.txt', 'f2.txt', 'f3.txt']:
        examine_padding(filename)
    
    for f in ['f1.txt', 'f2.txt', 'f3.txt']:
        os.remove(f)

if(__name__ == "__main__"):
    main() 