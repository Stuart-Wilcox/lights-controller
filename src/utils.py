def clamp_int(value, low=0, high=0):
    value = int(value)
    low = int(low)
    high = int(high)
    return min(high, max(low, value))
