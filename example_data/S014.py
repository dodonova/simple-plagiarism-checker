n, k = list(map(int, input().split()))
b = list(map(int, input().split()))
c = list(map(int, input().split()))
res = []
for i in range(n):
    res.append(b[i] / c[i])
save = res.copy()
ans = []
for i in range(k+1):
    a = min(res)
    if i != 0:
        ans.append(res.index(a) + 1)
    res[res.index(a)] = 99999
print(*ans)