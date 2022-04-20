def transform_name(s, n):
    l = s.split()
    for i in range(1, len(l)+1):
        if sum(map(len, l[:i])) + i - 1 > n:
            return ' '.join(l[:i-1]) + " \n" + ' '.join(l[i-1:])
    return s


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))