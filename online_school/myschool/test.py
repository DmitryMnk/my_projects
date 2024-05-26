list1 = [i for i in range(1, 101)]
k = 15
count = 0
find = 0
left = 0
right = 100

while find != k:
    mid = (left + right) // 2
    if mid == k:
        find = mid
    elif k < mid:
        right = mid
    else:
        left = mid
    count += 1

print(count)