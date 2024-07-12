def all_variants(text: str):
    """All possible subsequence generator."""
    for i in range(len(text)):
        for j in range(i, len(text)):
            if i == 0:
                yield text[j]
            else:
                yield text[j - i:j + 1]


# test
for x in all_variants("abc"):
    print(x)
