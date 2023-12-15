import itertools as it
l = list(map(int, input().split()))
val = "".join(list(map(str, [x for x in range(0, l[2] + 1)])))
arr = [x for x in it.product(val, repeat=l[0])]
good_arr = [x for x in arr if sum(list(map(int, x))) == l[1]]
rounded = str(round((len(good_arr) * (1 / len(arr))), 6))
print(rounded+"0"*(8-len(rounded)))