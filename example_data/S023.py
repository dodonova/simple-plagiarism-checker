N, K = map(int, input().split())
B = list(map(int, input().split()))
C = list(map(int, input().split()))
l = []
for i in range(N):
    l.append((i, B[i]/C[i]))
l.sort(key=lambda x: x[1], reverse=True)
out = []
for i in range(K):
    out.append(l[i][0] + 1)
out.sort()
print(*out)