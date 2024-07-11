def single_root_words(root_word: str, *other_words):
    """Finds same words with given root word and returns list of them"""
    same_words = []
    for word in other_words:
        if root_word.lower() in str(word).lower() or str(word).lower() in root_word.lower():
            same_words.append(word)
    return same_words


# test
result1 = single_root_words('rich', 'richiest', 'orichalcum', 'cheers', 'richies')
result2 = single_root_words('Disablement', 'Able', 'Mable', 'Disable', 'Bagel')
print(result1)
print(result2)
