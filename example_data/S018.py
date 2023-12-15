# put your python code here
str = input().split(' ')
n = int(str[0])
k = int(str[1])
powers = [int(i) for i in input().split(' ') if i != '']
prices = [int(i) for i in input().split(' ') if i != '']
ratio = [powers[i]/prices[i] for i in range(n)]
max_ratios = sorted(range(len(ratio)), key=lambda index: ratio[index])[-k:]
max_ratios = sorted(max_ratios)
for i in range(0, len(max_ratios)):
    max_ratios[i] += 1
print(*max_ratios)