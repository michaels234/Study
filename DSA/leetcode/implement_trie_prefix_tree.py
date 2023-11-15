#208. Implement Trie (Prefix Tree)
#Medium
#A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings.
#There are various applications of this data structure, such as autocomplete and spellchecker.

#Implement the Trie class:

#Trie() Initializes the trie object.
#void insert(String word) Inserts the string word into the trie.
#boolean search(String word) Returns true if the string word is in the trie (i.e., was inserted before), and false otherwise.
#boolean startsWith(String prefix) Returns true if there is a previously inserted string word that has the prefix prefix, and false otherwise.
 

#Example 1:

#Input
#["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
#[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
#Output
#[null, null, true, false, true, null, true]

#Explanation
#Trie trie = new Trie();
#trie.insert("apple");
#trie.search("apple");   // return True
#trie.search("app");     // return False
#trie.startsWith("app"); // return True
#trie.insert("app");
#trie.search("app");     // return True
 

#Constraints:

#1 <= word.length, prefix.length <= 2000
#word and prefix consist only of lowercase English letters.
#At most 3 * 104 calls in total will be made to insert, search, and startsWith.


class TrieNode():
	def __init__(self):
		self.children = {}
		self.terminal = False


class Trie():
	def __init__(self):
		self.root = TrieNode()
		self.root.terminal = True  # initial TrieNode has no characters (blank quotes) and finishes there

	def insert(self, word):
		node = self.root  # always start with root
		for char in word:
			if char not in node.children:  # this char hasn't been added at this location yet, so add it as a new node
				node.children[char] = TrieNode()
			node = node.children[char]  # get the next node from this node's child, and check the next char
		node.terminal = True  # mark that this last node was the end of the word

	def search(self, word):
		# each node is 1 character and has children which are the next characters in whatever words have been inserted
		node = self.root  # always start with root
		for char in word:
			if char in node.children:  # this char exists
				node = node.children[char]  # get the next node from this node's child, and check the next char
			else:
				return False  # if any char in word is not in this trie, the word isn't inserted, return False
		# after checking all chars, this word is only in this trie if that last char is the end of the word
		# eg. im searching walk, and walking is in the trie, i return False because walk hasn't been inserted
		return node.terminal

	def starts_with(self, prefix):
		node = self.root  # always start with root
		for char in prefix:
			if char in node.children:  # this char exists
				node = node.children[char]  # get the next node from this node's child, and check the next char
			else:
				return False  # if any char in prefix is not in this trie, the prefix isn't inserted, return False
		return True  # don't worry about terminal here, just return True of all the chars in prefix have been in trie


def test():
	print()
	try:
		trie = Trie()
		assert (
			trie.search('')
			and not trie.search('hello')
			and not trie.starts_with('hel')
		)
		trie.insert('hello')
		assert (
			trie.search('hello')
			and trie.starts_with('hel')
			and not trie.starts_with('helloworld')
			and not trie.search('hel')
			and not trie.search('helloworld')
		)
		print()
	except AssertionError as e:
		print(f"Error: {e}")
