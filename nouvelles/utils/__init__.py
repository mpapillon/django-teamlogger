def sizeof_fmt(size, suffix='B'):
    """
    Convert the byte size into binary human readable size.
    :param size: The size
    :param suffix: Suffix of size, default is Bytes (B)
    :return: the converted size.
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(size) < 1024.0:
            return "%3.1f%s%s" % (size, unit, suffix)
        size /= 1024.0
    return "%.1f%s%s" % (size, 'Yi', suffix)
