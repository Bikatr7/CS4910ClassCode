import socket
import subprocess
import time

def xor_bytes(a, b):
    """XOR two byte sequences"""
    return bytes(x ^ y for x, y in zip(a, b))

def padded_candidate(candidate):
    """Return the PKCS#7 padded version (16 bytes) of the candidate string"""
    candidate_bytes = candidate.encode()
    pad_length = 16 - len(candidate_bytes)
    pad = bytes([pad_length] * pad_length)
    return candidate_bytes + pad

def craft_attack_plaintext(bob_iv, next_iv, candidate):
    """
    Compute the plaintext P such that when using IV₂ (next_iv) the oracle produces:
      E( P ⊕ IV₂ ) = E( M ⊕ IV₁ )
    where M is the padded candidate message.
    
    Thus: P = M ⊕ IV₁ ⊕ IV₂.
    """
    M = padded_candidate(candidate)      ## 16 bytes padded candidate
    iv1 = bytes.fromhex(bob_iv)           ## original IV (16 bytes)
    iv2 = bytes.fromhex(next_iv)          ## next IV (16 bytes)
    
    P = xor_bytes(M, iv1)
    P = xor_bytes(P, iv2)
    
    return P.hex()

def setup_docker():
    """Build and run the Docker container"""
    print("Setting up encryption oracle...")
    
    subprocess.run(['docker-compose', 'up', '-d'], 
                  stdout=subprocess.DEVNULL)
    
    time.sleep(2)
    print("Oracle ready!")

def connect_to_oracle(host='localhost', port=3000):
    """Connect to the encryption oracle"""
    print(f"Connecting to {host}:{port}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    try:
        s.connect((host, port))
        print("Connected!")
        return s
    except Exception as e:
        print(f"Connection failed: {e}")
        raise

def get_oracle_response(sock):
    """Get response from oracle until prompt"""
    response = ""
    print("Waiting for oracle response...")
    
    while True:
        try:
            data = sock.recv(1024).decode()
            print(f"Received: {data}")
            if(not data):
                print("Connection closed by server")
                break
            response += data
            if("Your plaintext :" in data):
                break
        except socket.timeout:
            print("Socket timeout")
            break
    return response

def cleanup_docker():
    """Stop and remove the Docker container"""
    print("\nCleaning up...")
    subprocess.run(['docker-compose', 'down'], 
                  stdout=subprocess.DEVNULL)

def main():
    try:
        setup_docker()
        sock = connect_to_oracle()
        response = get_oracle_response(sock)
        print(response)
        
        for line in response.split('\n'):
            if("Bob's ciphertex:" in line):
                bob_cipher = line.split(': ')[1].strip()
            elif("The IV used" in line):
                bob_iv = line.split(': ')[1].strip()
            elif("Next IV" in line):
                next_iv = line.split(': ')[1].strip()
        
        print(f"Candidate details:\n Bob's ciphertex: {bob_cipher}\n IV used: {bob_iv}\n Next IV: {next_iv}")
        
        for i in range(5):
            print(f"\n=== Round {i+1} ===")
            candidate = "Yes"
            print(f"Trying candidate: '{candidate}'")
            plaintext = craft_attack_plaintext(bob_iv, next_iv, candidate)
            print(f"Crafted plaintext (hex): {plaintext}")
            sock.send(f"{plaintext}\n".encode())
            
            response = get_oracle_response(sock)
            our_cipher = response.split("Your ciphertext: ")[1].split('\n')[0]
            
            if(our_cipher[:len(bob_cipher)] == bob_cipher):
                print("\nBob's message is 'Yes'")
                next_iv = response.split("Next IV        : ")[1].split('\n')[0]
            else:
                next_iv = response.split("Next IV        : ")[1].split('\n')[0]
                candidate = "No"
                print(f"Trying candidate: '{candidate}'")
                plaintext = craft_attack_plaintext(bob_iv, next_iv, candidate)
                print(f"Crafted plaintext (hex): {plaintext}")
                sock.send(f"{plaintext}\n".encode())
                
                response = get_oracle_response(sock)
                our_cipher = response.split("Your ciphertext: ")[1].split('\n')[0]
                
                if(our_cipher[:len(bob_cipher)] == bob_cipher):
                    print("\nBob's message is 'No'")
                else:
                    print("\nError: Could not determine Bob's message")
                next_iv = response.split("Next IV        : ")[1].split('\n')[0]
        sock.close()
    
    finally:
        cleanup_docker()

if(__name__ == "__main__"):
    main() 