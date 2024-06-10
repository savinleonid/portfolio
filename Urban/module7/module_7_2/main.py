"""File read test with preloaded test.txt file with context manager 'with'."""

file_name = "test.txt"
with open(file_name, mode="r", encoding="utf8") as f:  # open file with context manager
    for line in f:
        print(line, end="")

# Context manager 'with' ensures file closure at the end of the work to prevent memory leaking if some errors occurs.
# Normally, we need to put close() function at the end, but here context manager makes it for us.
