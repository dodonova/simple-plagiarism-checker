N, K = map(int, input().split())
B = map(int, input().split())
C = map(int, input().split())
zp = list(zip(B, C))
zpc = zp.copy()
ans = []
for i in range(K):
    ind = zp.index(max(zp, key=lambda x: x[0] / x[1]))
    # del zpl[zpl.index(ind)]
    ans.append(zp[ind])
    del zp[ind]
print(*sorted((map(lambda x: zpc.index(x)+1, ans))))