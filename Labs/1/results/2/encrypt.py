import subprocess
import os
import sys

def run_openssl_command(cipher_type, operation, input_file, output_file, key, iv):
    """Run OpenSSL command"""
    try:
        cmd = [
            'openssl', 'enc',
            cipher_type,
            operation,
            '-in', input_file,
            '-out', output_file,
            '-K', key,
            '-iv', iv
        ]
        
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        return True, result.stdout
    
    except subprocess.CalledProcessError as e:
        return False, f"OpenSSL Error: {e.stderr}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def encrypt_and_decrypt_file(cipher_type, input_file, key, iv):
    """Encrypt and then decrypt a file using specified cipher"""
    
    encrypted_file = f"cipher_{cipher_type.replace('-', '_')}.bin"
    decrypted_file = f"decrypted_{cipher_type.replace('-', '_')}.txt"
    
    print(f"\nTesting {cipher_type}:")
    print("-" * 50)
    
    print(f"Encrypting {input_file} to {encrypted_file}")
    success, message = run_openssl_command(
        cipher_type,
        '-e',
        input_file,
        encrypted_file,
        key,
        iv
    )
    
    if(not success):
        print(f"Encryption failed: {message}")
        return False
    
    print(f"Decrypting {encrypted_file} to {decrypted_file}")
    success, message = run_openssl_command(
        cipher_type,
        '-d',
        encrypted_file,
        decrypted_file,
        key,
        iv
    )
    
    if(not success):
        print(f"Decryption failed: {message}")
        return False
    
    try:
        with open(input_file, 'rb') as f1, open(decrypted_file, 'rb') as f2:
            original = f1.read()
            decrypted = f2.read()
            
            if(original == decrypted):
                print("✓ Verification successful - decrypted file matches original")
                return True
            else:
                print("✗ Verification failed - decrypted file differs from original")
                return False
    
    except Exception as e:
        print(f"Verification error: {str(e)}")
        return False

def main():
    INPUT_FILE = "plaintext.txt"
    KEY = "00112233445566778889aabbccddeeff"
    IV = "0102030405060708"
    
    CIPHERS = [
        '-aes-128-cbc',    ## AES with 128-bit key in CBC mode
        '-aes-256-cbc',    ## AES with 256-bit key in CBC mode
        '-bf-cbc',         ## Blowfish in CBC mode
        '-aes-128-cfb',    ## AES with 128-bit key in CFB mode
        '-des-ede3-cbc'    ## Triple DES in CBC mode
    ]
    
    if(not os.path.exists(INPUT_FILE)):
        print(f"Error: Input file '{INPUT_FILE}' not found")
        sys.exit(1)
    
    print("Starting encryption tests...")
    print(f"Input file: {INPUT_FILE}")
    print(f"Key: {KEY}")
    print(f"IV: {IV}")
    
    results = []
    for cipher in CIPHERS:
        success = encrypt_and_decrypt_file(cipher, INPUT_FILE, KEY, IV)
        results.append((cipher, success))
    
    print("\nTest Summary:")
    print("-" * 50)
    for cipher, success in results:
        status = "✓ Passed" if success else "✗ Failed"
        print(f"{cipher}: {status}")

if(__name__ == "__main__"):
    main()
