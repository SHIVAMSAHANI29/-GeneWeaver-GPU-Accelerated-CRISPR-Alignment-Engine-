def iter_chunks(sequence: str, chunk_size: int, window_size: int):
    """Yield (core_start, core_end, extended_chunk).

    The extended chunk includes a right overlap so a fixed-size window crossing
    a core boundary can still be scanned. Callers should only evaluate windows
    whose start is in [core_start, core_end).
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if window_size <= 0:
        raise ValueError("window_size must be greater than zero")

    overlap = max(0, window_size - 1)
    length = len(sequence)
    for core_start in range(0, length, chunk_size):
        core_end = min(core_start + chunk_size, length)
        extended_end = min(core_end + overlap, length)
        yield core_start, core_end, sequence[core_start:extended_end]
