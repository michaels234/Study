class Node:
	def __init__(self, value, next=None):
		self.value = value
		self.next = next


class LinkedList:
	def __init__(self, value):
		self.__head = Node(value)
		self.__length = 1
	
	def add(self, value):
		node = self.__head
		while node.next:
			node = node.next
		node.next = Node(value)
		self.__length += 1

	def __len__(self):
		return self.__length
	
	def check_index_out_of_bounds(self, index):
		if index >= self.__length:
			raise Exception(f"Index {index} out of bounds")
	
	def list_all(self, print_only=False):
		node = self.__head
		if not print_only:
			output = []
		while 1:
			if node.next:
				if print_only:
					print(node.value, end=', ')
				else:
					output += [node.value]
				node = node.next
			else:
				if print_only:
					print(node.value)
					return
				else:
					output += [node.value]
					return output

	def __get_node_from_index(self, index):
		node = self.__head
		i = 0
		while 1:
			if i == index:
				return node
			elif node.next:
				i += 1
				node = node.next

	def __getitem__(self, index):
		self.check_index_out_of_bounds(index)
		node = self.__get_node_from_index(index)
		return node.value
		
	def __setitem__(self, index, value):
		self.check_index_out_of_bounds(index)
		node = self.__get_node_from_index(index)
		node.value = value

	def insert(self, index, value):
		self.check_index_out_of_bounds(index)
		if index == 0:
			self.__head = Node(value, next=self.__head)
		else:
			prev = self.__get_node_from_index(index-1)
			prev.next = Node(value, next=prev.next)
		self.__length += 1

	def delete(self, index):
		self.check_index_out_of_bounds(index)
		if index == 0:
			self.__head = self.__head.next
		else:
			prev = self.__get_node_from_index(index-1)
			prev.next = prev.next.next
		self.__length -= 1
	
	def __contains__(self, value):
		node = self.__head
		while 1:
			if node.value == value:
				return True
			elif node.next:
				node = node.next
			else:
				return False
	
	def find(self, value, which=1):
		node = self.__head
		found = 0
		i = 0
		while 1:
			if found + 1 == which and node.value == value:
				return i
			elif node.next:
				if node.value == value:
					found += 1
				i += 1
				node = node.next
			else:
				return None


def test():
	# test __init__ and list_all
	linked_list = LinkedList(6)
	assert linked_list.list_all() == [6]

	# test add
	linked_list.add(10)
	linked_list.add(-3)
	linked_list.add(2)
	assert linked_list.list_all() == [6, 10, -3, 2]

	# test __getitem__
	assert linked_list[2] == -3
	try:
		linked_list[4]
	except Exception as e:
		assert str(e) == 'Index 4 out of bounds'

	# test __setitem__
	linked_list[2] = 5
	assert linked_list[2] == 5
	assert linked_list.list_all() == [6, 10, 5, 2]
	try:
		linked_list[4] = 15
	except Exception as e:
		assert str(e) == 'Index 4 out of bounds'
	assert linked_list.list_all() == [6, 10, 5, 2]

	# test __contains__
	assert 5 in linked_list
	assert -15 not in linked_list

	# test insert
	linked_list.insert(index=1, value=31)
	assert linked_list.list_all() == [6, 31, 10, 5, 2]
	linked_list.insert(index=0, value=9)
	assert linked_list.list_all() == [9, 6, 31, 10, 5, 2]
	linked_list.insert(index=5, value=6)
	assert linked_list.list_all() == [9, 6, 31, 10, 5, 6, 2]
	try:
		linked_list.insert(index=7, value=13)
	except Exception as e:
		assert str(e) == 'Index 7 out of bounds'
	assert linked_list.list_all() == [9, 6, 31, 10, 5, 6, 2]

	# test 
	assert linked_list.find(6) == 1
	assert linked_list.find(6, 2) == 5

	# test __len__
	assert len(linked_list) == 7

	# SUCCESS!
	return 'SUCCESS!'