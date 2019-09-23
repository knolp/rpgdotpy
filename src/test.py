def calc2(N, D):
    rotate = {
        "6" : "9",
        "9" : "6"
    }
    convert = {
        "0" : "0",
        "1" : "1",
        "2" : "2",
        "5" : "3",
        "6" : "4",
        "8" : "5",
        "9" : "6"
    }
    N = sum([int(convert[item]) * (7 ** idx)  for idx, item in enumerate([rotate[x] if x in rotate.keys() else x for x in N[::-1]][::-1])]) - sum([int(convert[D[i]]) * (7 ** i)  for i in range(len(D))])
    return N



D, N = input().split()
print(calc2(N, D))
