n = int(input().split()[1])
track = '_' + '_'.join(input().split()) + '_'
s = 0
for _ in range(n):
    frag = '_' + '_'.join(input().split()[1:]) + '_'
    s += track.count(frag)**2
print(s)