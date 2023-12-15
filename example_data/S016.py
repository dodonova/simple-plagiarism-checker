n, m, k = map(int, input().split())
vector = [i for i in range(0, k + 1)]
cnt = (k + 1) ** n
cnt_sum = 0
num = 0
lst_vector = []

while len(str(num)) <= n:
    lst = [int(i) for i in list(str(num))]
    if max(lst) <= k:
        if sum(lst) == m:
            cnt_sum += 1
    num += 1

print(round(cnt_sum / cnt, 6))