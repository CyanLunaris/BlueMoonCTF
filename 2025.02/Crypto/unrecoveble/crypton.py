import random

# Параметры для шифрования
RNG_SEED = 0x4C55464659
DENSITY_FACTOR = 8
N_LAYERS = 5

def reseed_rng():
    random.seed(a=RNG_SEED, version=2)

def iteration_encryption(src_bytes):
    src_len = len(src_bytes)
    density = src_len * DENSITY_FACTOR
    dest = bytearray(density)

    for i in range(density):
        a = random.randint(0, src_len - 1)
        b = random.randint(0, src_len - 1)
        op_type = random.randint(0, 2)

        if op_type == 0:
            dest[i] = src_bytes[a] ^ src_bytes[b]
        elif op_type == 1:
            dest[i] = (src_bytes[a] + src_bytes[b]) & 0xFF
        else:
            dest[i] = src_bytes[a] & src_bytes[b]

    return dest

def encrypt_flag(flag_bytes, layers=N_LAYERS):
    reseed_rng()
    data = bytearray(flag_bytes)
    for _ in range(layers):
        data = iteration_encryption(data)
    return data

if __name__ == "__main__":
    with open("flag.txt", "rb") as f:
        flag_original = f.read().strip()

    encrypted_flag = encrypt_flag(flag_original, N_LAYERS)

    with open("flag.enc", "wb") as f:
        f.write(encrypted_flag)

    print(f"[+] Флаг зашифрован и сохранён в flag.enc (сид = {hex(RNG_SEED)})")
