def feistel_cipher_encrypt(plaintext, key):
    def xor(a, b):
        return bytes(i ^ j for i, j in zip(a, b))

    def feistel_round(left, right, subkey):
        new_right = xor(left, F_function(right, subkey))
        return right, new_right

    def F_function(block, subkey):
        return xor(block, subkey)

    # تقسیم کلید اصلی به زیرکلیدها
    subkeys = [key[i:i+8] for i in range(0, len(key), 8)]

    # تبدیل متن اصلی به بلوک‌های 64 بیتی
    blocks = [plaintext[i:i+8] for i in range(0, len(plaintext), 8)]
    
    # اگر طول آخرین بلوک کمتر از 8 بایت است، پر کردن آن
    if len(blocks[-1]) < 8:
        blocks[-1] += bytes(8 - len(blocks[-1]))

    encrypted_blocks = []

    for block in blocks:
        left, right = block[:4], block[4:]
        for round in range(16):
            left, right = feistel_round(left, right, subkeys[round % len(subkeys)])
        encrypted_blocks.append(left + right)

    return b''.join(encrypted_blocks)

def feistel_cipher_decrypt(ciphertext, key):
    def xor(a, b):
        return bytes(i ^ j for i, j in zip(a, b))

    def feistel_round(left, right, subkey):
        new_right = xor(left, F_function(right, subkey))
        return right, new_right

    def F_function(block, subkey):
        return xor(block, subkey)

    # تقسیم کلید اصلی به زیرکلیدها
    subkeys = [key[i:i+8] for i in range(0, len(key), 8)]

    # تبدیل متن رمزنگاری شده به بلوک‌های 64 بیتی
    blocks = [ciphertext[i:i+8] for i in range(0, len(ciphertext), 8)]

    decrypted_blocks = []

    for block in blocks:
        left, right = block[:4], block[4:]
        for round in range(15, -1, -1):
            left, right = feistel_round(left, right, subkeys[round % len(subkeys)])
        decrypted_blocks.append(left + right)

    return b''.join(decrypted_blocks)

# کلید 128 بیتی
key = b'Sixteen byte key'

# متن اصلی
plaintext = b'Hello, World!'

# رمزگذاری
ciphertext = feistel_cipher_encrypt(plaintext, key)
print(f"Ciphertext: {ciphertext.hex()}")

# رمزگشایی
decrypted_text = feistel_cipher_decrypt(ciphertext, key)
print(f"Decrypted text: {decrypted_text.decode()}")
