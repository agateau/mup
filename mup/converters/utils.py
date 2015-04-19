def selectBestConverter(lst):
    """Select the best converter from lst. An offline converter is preferred to
    an online one. The reference implementation is preferred if it is
    available."""

    def keyForConverter(converter):
        weight = 1
        if converter.online:
            weight += 1
        if converter.reference:
            weight -= 1
        return '{}{}'.format(weight, converter.name.lower())

    lst = sorted(lst, key=keyForConverter)
    return lst[0]
