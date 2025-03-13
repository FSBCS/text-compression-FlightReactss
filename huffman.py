from friendsbalt.acs import MinPQ

class HuffmanEncoding:
    def __init__(self, src=None, encoded_text=None, root=None):
        """
        Initializes a new Huffman Encoding. Either source text or encoded text and root must be provided.
        If source text is provided, it builds the Huffman tree and dictionary, and encodes the text.
        If encoded text and root are provided, it decodes the text.
        Args:
            src (str, optional): The source text to be encoded.
            encoded_text (str, optional): The encoded text to be decoded.
            root (Node, optional): The root node of the Huffman tree for decoding.
        """
        self.root_node = None
        self.encoded_text = encoded_text
        self.source_text = src
        self.codes = {}

        if src is not None:
            # Build Huffman Tree from source text
            self._build_huffman_tree(src)
        elif encoded_text is not None and root is not None:
            # Decode the encoded text using the provided Huffman tree root
            self.root_node = root
            self.source_text = self._decode_encoded_text(encoded_text, root)

    class Node:
        def __init__(self, freq, char=None, left=None, right=None):
            self.char = char
            self.freq = freq
            self.left = left
            self.right = right
        
        def is_leaf(self):
            return self.char is not None

    def _build_huffman_tree(self, src):
        """Builds the Huffman tree based on the frequency of characters in the source text."""
        # Frequency table for characters
        freq_table = {}
        for char in src:
            if char in freq_table:
                freq_table[char] += 1
            else:
                freq_table[char] = 1
        
        # Create a priority queue (min-heap)
        pq = MinPQ()
        for char, freq in freq_table.items():
            pq.insert(self.Node(freq, char))

        # Build the tree by combining the two nodes with the smallest frequency
        while len(pq) > 1:
            left = pq.del_min()
            right = pq.del_min()
            merged_node = self.Node(left.freq + right.freq, left=left, right=right)
            pq.insert(merged_node)

        # The last node in the priority queue is the root of the Huffman tree
        self.root_node = pq.del_min()

        # Build the dictionary mapping characters to Huffman codes
        self.codes = self._build_dictionary(self.root_node)

    def encoding(self):
        """
        Returns the encoded text.
        Returns:
            str: The encoded text as a string of 0s and 1s.
        """
        if self.source_text is None:
            return ''
        encoded_text = ''.join(self.codes[char] for char in self.source_text)
        return encoded_text

    def source_text(self):
        """
        Returns the original source text.
        Returns:
            str: The original source text.
        """
        return self.source_text

    def root(self):
        """
        Returns the root node of the Huffman tree.
        Returns:
            Node: The root node of the Huffman tree.
        """
        return self.root_node

    def _decode_encoded_text(self, encoded_text, root):
        """Decodes the encoded text using the Huffman tree."""
        decoded_text = []
        node = root
        for bit in encoded_text:
            if bit == '0':
                node = node.left
            else:
                node = node.right
            if node.is_leaf():
                decoded_text.append(node.char)
                node = root  # Start over from the root node
        return ''.join(decoded_text)

    def _build_dictionary(self, node=None, prefix=''):
        """
        Recursively builds a dictionary that maps characters to their corresponding
        Huffman codes based on the Huffman tree.
        Args:
            node (Node, optional): The current node in the Huffman tree. Defaults to None,
                                   which means the function will start from the root node.
            prefix (str, optional): The current Huffman code prefix. Defaults to an empty string.
        Returns:
            dict: A dictionary where keys are characters and values are their corresponding
                  Huffman codes.
        """
        if node is None:
            node = self.root_node
        
        if node.is_leaf():
            return {node.char: prefix}
        
        dictionary = {}
        dictionary.update(self._build_dictionary(node.left, prefix + '0'))
        dictionary.update(self._build_dictionary(node.right, prefix + '1'))
        return dictionary
