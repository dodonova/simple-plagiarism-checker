import copy
inp = input().split()

a = int(inp[0])
b = int(inp[1])

m = list(map(int, input().split()))
c = list(map(int, input().split()))

res = [m[i]/c[i] for i in range(len(m))]
copRes = copy.copy(res)

ans = ''

for i in range(b):
    mx = max(res)
    ind = copRes.index(mx)
    ans = str(ind+1)+ ' ' + ans
    copRes[ind] = 1000000000
    ind2 = res.index(mx)
    res = res[:ind2]+res[ind2+1:]

print(' '.join(list(map(str,sorted(list(map(int, ans[:-1].split(' '))))))))