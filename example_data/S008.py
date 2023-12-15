# put your python code here
n, m = map(int, input().split())
b = input()
k = 0
for i in range(m):
    a = input()
    a = a[2:]
    k += b.count(a) ** 2
print(k)