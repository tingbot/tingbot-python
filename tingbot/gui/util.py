def clamp(minimum,maximum,value):
    """returns value, constrained to be within the specified minimum and maximum"""
    return max(minimum,min(maximum,value))

