def test(a):
    if a == 0:
        return
    else:
        return test(a - 1)
