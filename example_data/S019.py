# put your python code here
n, m = map(int, input().split())
b = input()
polz = []
for i in range(m):
    s = input()
    if s not in polz:
        polz.append(s)
sum = 0
for i in range(m):
    s = b.count(polz[i][2:-1])
    if s != 0:
        sum += s**2
print(sum)