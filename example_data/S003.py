N, M = map(int, input().split())
melody =  input().split()
res = 0
for i in range(M):
    bit = input().split()[1:]
    if bit[0] not in melody:
        continue
    counter = 0
    bitlen = len(bit)
    for i in range(len(melody)-bitlen):
        if melody[i:i+bitlen] == bit:
            counter+=1
    res+= counter**2
print(res)