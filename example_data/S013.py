N, M = map(int, input().split())
music = input()
res = 0
for i in range(M):
    frag = input()
    frag = frag[frag.find(' ')+1:]
    #print(frag)
    res += music.count(frag)**2
print(res)