import subprocess
import os
import struct

def get_bmp_header_size(filename):
    """Get the actual header size from BMP file"""
    try:
        with open(filename, 'rb') as f:
            header = f.read(14)
            if(len(header) < 14):
                return None
            
            pixel_offset = struct.unpack('<I', header[10:14])[0]
            return pixel_offset
            
    except Exception as e:
        print(f"Error reading header size: {str(e)}")
        return None

def encrypt_image(input_file, output_file, mode, key, iv=None):
    """Encrypt image using specified mode (ECB or CBC)"""
    try:
        header_size = get_bmp_header_size(input_file)
        if(not header_size):
            print(f"Could not determine header size for {input_file}")
            return False
            
        with open(input_file, 'rb') as f:
            header = f.read(header_size)

        cmd = ['openssl', 'enc', f'-aes-128-{mode.lower()}']
        cmd.extend(['-e', '-in', input_file, '-out', 'temp.bin', '-K', key])
        
        if(mode == 'CBC'):
            cmd.extend(['-iv', iv])
        
        subprocess.run(cmd, check=True)
        
        with open('temp.bin', 'rb') as f:
            encrypted_body = f.read()[header_size:]  ## Skip header of encrypted file
        
        with open(output_file, 'wb') as f:
            f.write(header)
            f.write(encrypted_body)
        
        os.remove('temp.bin')
        return True
        
    except Exception as e:
        print(f"Error encrypting {input_file} with {mode}: {str(e)}")
        return False

def process_image(image_name):
    """Process a single image with both ECB and CBC modes"""
    KEY = "00112233445566778889aabbccddeeff"
    IV = "0102030405060708"
    
    print(f"\nProcessing {image_name}:")
    print("-" * 50)
    
    ecb_output = f"{image_name.rsplit('.', 1)[0]}_ecb.bmp"
    if(encrypt_image(image_name, ecb_output, 'ECB', KEY)):
        print(f"✓ ECB encryption successful: {ecb_output}")
    
    cbc_output = f"{image_name.rsplit('.', 1)[0]}_cbc.bmp"
    if(encrypt_image(image_name, cbc_output, 'CBC', KEY, IV)):
        print(f"✓ CBC encryption successful: {cbc_output}")

def main():
    process_image("pic_original.bmp")
    process_image("custom_photo.bmp")
    
    print("\nEncryption complete. Please view the output files with an image viewer.")
    print("Note: Original headers have been preserved to maintain BMP format.")

if(__name__ == "__main__"):
    main() 