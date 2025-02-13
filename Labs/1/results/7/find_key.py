from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def pad_key(word):
    """Pad the word with # to make it 16 bytes"""
    return (word + '#' * 16)[:16].encode()

def encrypt_test(key, plaintext, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ## Add PKCS7 padding
    padding_length = 16 - (len(plaintext) % 16)
    padded = plaintext + bytes([padding_length] * padding_length)
    return encryptor.update(padded) + encryptor.finalize()

def main():
    plaintext = b'This is a top secret.'
    target = bytes.fromhex('764aa26b55a4da654df6b19e4bce00f4ed05e09346fb0e762583cb7da2ac93a2')
    iv = bytes.fromhex('aabbccddeeff00998877665544332211')

    with open('dictionary.txt', 'r') as f:
        test_words = [line.strip() for line in f if len(line.strip()) < 16]
    
    for word in test_words:
        key = pad_key(word)
        encrypted = encrypt_test(key, plaintext, iv)
        if(encrypted == target):
            print(f"Found key: {word}")
            print(f"Padded key: {word + '#' * (16-len(word))}")
            print(f"Key (hex): {key.hex()}")
            return

    print("Key not found in test words")

if(__name__ == "__main__"):
    main()