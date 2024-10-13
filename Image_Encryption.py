from Crypto.Cipher import RC5
from Crypto.Random import get_random_bytes
from PIL import Image
import os

def encrypt_image(image_path, key):
    # Membaca gambar dan mengubahnya menjadi byte
    with open(image_path, 'rb') as img_file:
        image_data = img_file.read()

    # Generate initialization vector (IV) untuk mode CBC
    iv = get_random_bytes(RC5.block_size)
    
    # Membuat cipher RC5 dengan mode CBC
    cipher = RC5.new(key, RC5.MODE_CBC, iv)
    
    # Padding jika ukuran gambar tidak sesuai dengan block size
    padding_length = RC5.block_size - len(image_data) % RC5.block_size
    image_data += bytes([padding_length]) * padding_length

    # Enkripsi gambar
    encrypted_image_data = cipher.encrypt(image_data)
    
    return iv, encrypted_image_data

def decrypt_image(encrypted_image_data, key, iv):
    # Membuat cipher RC5 dengan mode CBC untuk dekripsi
    cipher = RC5.new(key, RC5.MODE_CBC, iv)
    
    # Dekripsi data gambar
    decrypted_image_data = cipher.decrypt(encrypted_image_data)
    
    # Menghilangkan padding
    padding_length = decrypted_image_data[-1]
    decrypted_image_data = decrypted_image_data[:-padding_length]
    
    return decrypted_image_data

# Contoh penggunaan
image_path = 'Assets/image.jpg'
key = get_random_bytes(16)  # Kunci 128-bit (panjang kunci yang disarankan untuk RC5)

# Enkripsi gambar
iv, encrypted_image_data = encrypt_image(image_path, key)

# Simpan gambar yang terenkripsi
with open('encrypted_image.bin', 'wb') as f:
    f.write(iv + encrypted_image_data)

# Dekripsi gambar
with open('encrypted_image.bin', 'rb') as f:
    iv = f.read(RC5.block_size)
    encrypted_image_data = f.read()

decrypted_image_data = decrypt_image(encrypted_image_data, key, iv)

# Simpan gambar yang telah didekripsi
with open('decrypted_image.jpg', 'wb') as f:
    f.write(decrypted_image_data)
