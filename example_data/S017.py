n, m = map(int, input().split())
B = [int(i) for i in input().split()]
cnt = 0
for i in range(m):
    a = [int(i) for i in input().split()]
    dlina = a[0]
    a.pop(0)
    for i in range(len(B) - dlina + 1):
        if B[i: i + dlina] == a:
            cnt += 1
            break

print(cnt)