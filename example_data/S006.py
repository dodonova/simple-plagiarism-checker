# put your python code here

from math import sqrt
N, M = map(int, input().split())
s = []
for i in range(N):
    s.append(list(map(int, input().split())))

ans = 0
for i in range(N*M):
    x1 = i//M
    y1 = i%M
    c = s[x1][y1]
    if 1:
        for j in range(i+1, N*M):
            x2 = j//M
            y2 = j%M
            if s[x2][y2]==c:
                for k in range(j+1, N*M):
                    x3 = k//M
                    y3 = k%M
                    if s[x3][y3]==c:
                        a1 = (x1 - x2)**2 + (y1-y2)**2
                        a2 = (x2 - x3)**2 + (y2-y3)**2
                        a3 = (x1 - x3)**2 + (y1-y3)**2
                        if (-1 < (a1 + a2 - a3)/(2*sqrt(a1*a2)) < 0) or (-1 < (a1 + a3 - a2)/(2*sqrt(a1*a3)) < 0) or (-1 < (a3 + a2 - a1)/(2*sqrt(a2*a3)) < 0):
                            ans+=1
print(ans)