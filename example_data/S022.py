# put your python code here
n, m = map(int, input().split())

tr = input()
count = 0
for i in range(m):
    s = input()[2:-1]
    if s in tr:
        count += 1
print(count)