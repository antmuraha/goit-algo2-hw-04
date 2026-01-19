from pygtrie import Trie


class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        """Count the number of words ending with a given pattern.

        Args:
            pattern: A string pattern to match at the end of words.

        Returns:
            The number of words ending with the pattern (case-sensitive).

        Raises:
            TypeError: If pattern is not a string.
        """
        if not isinstance(pattern, str):
            raise TypeError(f"pattern must be a string, not {type(pattern).__name__}")

        # Handle empty pattern - counts all words
        if not pattern:
            return sum(1 for _ in self.iterkeys())

        count = 0
        # Convert pattern to internal path representation
        pattern_path = tuple(self._path_from_key(pattern))
        pattern_len = len(pattern_path)

        # Iterate through all keys and check if they end with the pattern
        for key in self.iterkeys():
            key_path = tuple(self._path_from_key(key))
            # Check if key ends with pattern
            if len(key_path) >= pattern_len and key_path[-pattern_len:] == pattern_path:
                count += 1

        return count

    def has_prefix(self, prefix) -> bool:
        """Check if there is at least one word with the given prefix.

        Args:
            prefix: A string prefix to search for.

        Returns:
            True if at least one word starts with the prefix (case-sensitive), False otherwise.

        Raises:
            TypeError: If prefix is not a string.
        """
        if not isinstance(prefix, str):
            raise TypeError(f"prefix must be a string, not {type(prefix).__name__}")

        # Empty prefix matches all words
        if not prefix:
            return bool(list(self.iterkeys()))

        try:
            # Try to navigate to the prefix node
            node, _ = self._get_node(prefix)
            # If we reach here, the prefix exists as a node in the trie
            return True
        except KeyError:
            # Prefix path doesn't exist in trie
            return False


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie[word] = i

    # Checking the number of words ending with a given suffix
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Checking the presence of a prefix
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat
