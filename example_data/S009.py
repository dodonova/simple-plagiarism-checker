import itertools
n, m = map(int, input().split())
pixels = []
colors = {}
for i in range(n):
    pixels_sub = []
    for j, c in enumerate(list(map(int, input().split()))):
        if c in colors.keys():
            colors[c].append((i, j))
        else:
            colors[c] = [(i, j)]
        pixels_sub.append(c)
    pixels.append(pixels_sub)
count = 0
for c in colors.keys():
    for el in itertools.combinations(colors[c], r=3):
        f, s, t = el
        f_s = (f[0] - s[0]) ** 2 + (f[1] - s[1]) ** 2
        s_s = (f[0] - t[0]) ** 2 + (f[1] - t[1]) ** 2
        t_s = (t[0] - s[0]) ** 2 + (t[1] - s[1]) ** 2
        try:
            k = (s[1] - f[1]) / (s[0]-f[0])
            b = f[1] - k*f[0]
            if (f_s + s_s < t_s or f_s + t_s < s_s or s_s + t_s < f_s) and t[1] != (k * t[0] + b):
                count += 1
        except ZeroDivisionError:
            if (f_s + s_s < t_s or f_s + t_s < s_s or s_s + t_s < f_s) and t[0] != f[0]:
                count += 1

print(count)