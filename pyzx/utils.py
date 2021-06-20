def get_closest(n, l):
    return min(l, key=lambda x: abs(x - n))
