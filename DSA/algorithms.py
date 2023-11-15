import math
import random
import time


class Algorithm():
	def __init__(self, function, checker, order):
		self.function = function
		self.checker = checker
		self.order = order


class Complexity():
	def __init__(self):
		self.count = 0  # steps count

	def start_steps(self, n):
		# start Complexity, set size n, save orders array
		self.n = n
		self.orders = [
			{'calc': 1, 'name': 'O(1) Constant'},
			{'calc': self.n, 'name': 'O(n) Linear'},
			{'calc': self.n * math.log(self.n) / math.log(2), 'name': 'O(n*log(n)) Logarithmic'},
			{'calc': pow(self.n, 2), 'name': 'O(n^2) Quadratic'},
			{'calc': pow(2, self.n), 'name': 'O(2^n) Exponential'},
			{'calc': math.factorial(self.n), 'name': 'O(n!) Factorial'},
		]

	def start_timing(self):
		self.start_time = time.time()

	def end_timing(self):
		self.total_time = time.time() - self.start_time

	def add_step(self):  # add to steps count
		self.count += 1
	
	def get_order_level(self, count=None, prnt=None):
		if not count: count = self.count  # use input count if exists, otherwise use count from self
		for i in range(1, len(self.orders)):  # go thru the 6 orders
			if self.orders[i-1]['calc'] <= count <= self.orders[i]['calc']:  # find where count fits between two orders
				# print details of this run only if prnt exists
				text = f"{prnt}\t\t\t\t{self.orders[i-1]['name']} {round(self.orders[i-1]['calc'], 1)} <= "
				text += f"**{count}** <= {self.orders[i]['name']} {round(self.orders[i]['calc'], 1)}"
				if prnt: print()
				# return the interpolation of the order "level" based on the where count lies between two orders
				return i - 1 / (self.orders[i]['calc'] - self.orders[i-1]['calc']) * (self.orders[i]['calc'] - count)


def tab_no(item):  # get the number of 4-space tabs that fit within the length of this item (rounds down)
	return int(len(item.expandtabs(4))/4)


class PrintData():
	# use PrintData to add rows to print over time, and print them all pretty at the end
	def __init__(self):
		self.data = []
		self.__row_length = 0
		self.__max_tab_num = None

	def add(self, row):
		# add rows to print to data, check row length, check max number of tabs for each item for when printing later
		if len(self.data):  # if at least 1 row has been added
			if self.__row_length == len(row):  # check the new row is the right length
				for i, item in enumerate(row):  # check max item lengths and add new max if larger
					if tab_no(item) > self.__max_tab_num[i]:
						self.__max_tab_num[i] = tab_no(item)
			else:  # if not the right length
				raise Exception("Newly added row length doesn't match other data's row length.")  # error if not
		else:  # if now rows have been added yet
			self.__row_length = len(row)  # set the row length
			self.__max_tab_num = [tab_no(item) for item in row]  # set initial __max_tab_num
		self.data += [row]  # add the new row to the data

	def get_pretty_print(self):
		# return pretty print text which will print all rows of the data all pretty with correct tab spacing
		tab = '\t'
		text = ''
		for i, row in enumerate(self.data):
			for j, item in enumerate(row):
				# add the item to print, and the correct number of tabs after it to line up with others in this column
				text += item + tab * (self.__max_tab_num[j] + 1 - tab_no(item))
			# add a new line at the end of each row (except for the last row)
			if i != len(self.data) - 1:
				text += '\n'
		return text.expandtabs(4)  # expandtabs forces all tabs to be specifit length (4)


def make_array(min_size=10, max_size=1000, seed=None):
	if seed:
		random.seed(seed)
	n = random.randrange(min_size, max_size+1)  # with random array size
	arr = []
	for _ in range(n):
		arr += [random.randrange(-max_size, max_size+1)]  # and random array elements
	return arr


def sort_checker(comp, function, min_size=100, max_size=1000, seed=None, prnt=None):
	arr = make_array(min_size, max_size, seed)
	comp.start_steps(n=len(arr))
	start_arr = arr.copy()
	result = function(comp, arr)
	expected = start_arr.copy()
	expected.sort()
	error_check(start=start_arr, expected=expected, result=result, prnt=prnt)


def error_check(start, expected, result, prnt=False):
	if result != expected:  # if result is different than expected
		print(f"----------------------------------ERROR----------------------------------")  # print an ERROR
	if prnt:
		print(f"{start=}\n{result=}\n{expected=}")


def simple_check(algo_list):
	seed = random.randrange(0, 100)
	for algorithm in algo_list:
		comp = Complexity()
		print_data = PrintData()
		prnt = algorithm.function.__name__
		algorithm.checker(comp, algorithm.function, min_size=10, max_size=10, seed=seed, prnt=prnt)
		order_level = round(comp.get_order_level(prnt=prnt), 3)
		order_int = math.ceil(order_level)
		order_level_str = str(order_level)
		print_data.add([
			algorithm.function.__name__,
			f"{round(comp.total_time, 5)}s",
			comp.orders[order_int]['name'] + '\t',
			comp.orders[order_int-1]['name'],
			f"= lv {order_int-1} < avg lv **{order_level_str + '0' * (5 - len(order_level_str))}** <= lv {order_int} =",
			comp.orders[order_int]['name'],
		])
		print(print_data.get_pretty_print())


def deep_dive(run_list):
	# run all algorithms 20 times each, count steps, get Complexity results. save results to be printed out at the end
	run_times = 50
	seed_list = [random.randrange(0, 100) for _ in range(run_times)]
	print_data = PrintData()
	for algorithm in run_list:  # for every algorithm in run_list
		avg_total_time = 0
		avg_order_level = 0
		for i in range(run_times):  # run times
			comp = Complexity()  # Complexity is used to count steps over time and get the order level etc. at the end
			algorithm.checker(comp, algorithm.function, seed=seed_list[i])
			total_time = comp.total_time
			order_level = comp.get_order_level()
			# this is a simple add-to-average calculation: (average * current_length + new_item) / new_length
			avg_total_time = (avg_total_time * i + total_time) / (i + 1)  # caluclate average total time
			avg_order_level = (avg_order_level * i + order_level) / (i + 1)  # caluclate average order level
		print(algorithm.function.__name__, 'DONE')
		# after running 20 times, output the average order level and a bit of info about that
		order_int = math.ceil(avg_order_level)
		assert order_int == algorithm.order
		avg_order_level = str(round(avg_order_level, 3))
		print_data.add([
			algorithm.function.__name__,
			f"{round(avg_total_time, 7)}s",
			comp.orders[order_int]['name'] + '\t',
			comp.orders[order_int-1]['name'],
			f"= lv {order_int-1} < avg lv {avg_order_level + '0' * (5 - len(avg_order_level))} <= lv {order_int} =",
			comp.orders[order_int]['name'],
		])
	print(print_data.get_pretty_print())
	return 'SUCCESS!'


#####ALGORITHMS##########ALGORITHMS##########ALGORITHMS##########ALGORITHMS##########ALGORITHMS##########ALGORITHMS#####
##########ALGORITHMS##########ALGORITHMS##########ALGORITHMS##########ALGORITHMS##########ALGORITHMS##########ALGORITHMS


def selection_sort(comp, arr):
	# function: sort a given array arr in ascending order
	# approach: incremental
	# methodology: search for the minimum element, set it at the start of the array,
	# and put the element that was at the start of the array up into the leftover elements to be sorted later, repeat
	comp.start_timing()
	for i in range(len(arr) - 1):  # for every element in arr (can skip last one, because all will be set at that point)
		min_j = i  # every time, reset the min_j, the index of the min element, which we will search for
		for j in range(i, len(arr)):  # check all from i (earlier i have already been set)
			comp.add_step()
			if arr[j] < arr[min_j]:  # set min_j = j if arr[j] < arr[min_j] OR if min_j not set yet
				min_j = j
		# after we've check all leftovers and found the min, swap the min and the current.
		# note: this could be done by slowly building a result array, and removing elements from a left-overs array,
		# but to store less arrays, we can do it with one array, there the result array is like from 0 to current i,
		# and the left-overs array is from i+1 to len(arr)-1. the order of the leftovers don't matter, so swapping to
		# that location isnt important, the point is to take the current and leave it in leftovers, then set current to
		# minimum, which is adding to the results array. same thing just doing it in one array.
		arr[i], arr[min_j] = arr[min_j], arr[i]  # swap. note: its possible the current was the min, in which case this really does nothing
	comp.end_timing()
	return arr


def modified_selection_sort(comp, arr):
	# function: sort a given array arr in ascending order
	# approach: incremental
	# methodology: 
	comp.start_timing()
	for i in range(len(arr) - 1):  # for every element in arr (can skip last one, because all will be set at that point)
		for j in range(i+1, len(arr)):  # check all after i
			comp.add_step()
			if arr[i] > arr[j]:  # if earlier element arr[i] > later element arr[j], swap them
				arr[i], arr[j] = arr[j], arr[i]
				# doesn't stop here, it'll keep swapping arr[i] with everything lower than it until reaching the end,
				# so at the end arr[i] will be set to whatever the lowest was of the remaining elements.
				# achieved the same as selection_sort, but without setting a minimum.
				# its faster than selection_sort because selection_sort has to check the whole leftovers every time for a min,
				# but modified_selection_sort checks leftovers minus current, and is comparing to current
	comp.end_timing()
	return arr


def bubble_sort(comp, arr):
	# function: sort a given array arr in ascending order
	# approach: incremental
	# methodology: checks two adjacent and swaps lower to earlier, checks the next 2 adjacent and next 2, repeating.
	# after reaching the end, you just start again from the beginning. You stop once youve made one full pass no swaps.
	comp.start_timing()
	swapped = True
	while swapped:  # this has the worst time, it doesn't decrease checks over time, it checks whole array every time
		swapped = False  # set to False before new sweep
		for i in range(1, len(arr)):  # check all
			comp.add_step()
			if arr[i-1] > arr[i]:  # if earlier element arr[i-1] > later element arr[i], swap them
				arr[i], arr[i-1] = arr[i-1], arr[i]
				swapped = True  # flag to keep while looping. if there was no swap for a whole for loop break while
				# doesn't stop here, it'll keep swapping arr[j] with everything lower than it until reaching the end,
				# so at the end arr[i] will be set to whatever the lowest was of the remaining elements.
	comp.end_timing()
	return arr


def like_insertion_sort(comp, arr):
	# function: sort a given array arr in ascending order
	# approach: incremental
	# methodology: for each element, move it down until it's its between two that are less and greater than it
	# note: does exact same thing as insertion_sort, same number of steps, just changed i's and j's to how I like it
	comp.start_timing()
	for i in range(1, len(arr)):
		arr_i = arr[i]
		for j in reversed(range(1, i+1)):  # j counts down from i to 1 (checks j-1 so can't go down to 0)
			comp.add_step()
			if arr[j-1] > arr_i:  # if earlier element arr[j-1] is greater than current element arr_i
				arr[j] = arr[j-1]  # swap them (then move down one more and swap those two, until no longer larger)
				if j-1 == 0:  # last possible loop
					arr[j-1] = arr_i  # don't need to set the earlier one every time, just set once at the end
			else:  # if earlier element less than current element, don't swap, done moving current element down, break
				arr[j] = arr_i  # don't forget to do the 'set once at the end'
				break
		# note, the one in the book doesn't use j and j-1 comparisons, it uses j+1 and j comparisons.
		# for me that was less intuitive since we are moving down, checking j-1 felt more intuitive for me.
		# this results in a difference tho at the end of the for loop; my for loop can only go down to j = 1, not j = 0.
		# in book version if it breaks because j = -1 or if it breaks because current is no longer less than earlier,
		# either way in the end j+1=-1+1=0 or j+1=current is the element to be set in the end. so they have one line.
		# however for me, if i break at j = 1, j-1=0 must be set at the end, but if i break at no longer less than,
		# j=current must be set at the end. which is why i have end setting in to places, in 'if' and in 'else'.
		# but this doesn't increase time or space, it just increases lines of code.
		# i'll show and explain the book way too, which is fine, but id like to show if you follow intuition
		# you can still get the same result and its possible to do it multiple ways without hurting step count etc.
	comp.end_timing()
	return arr


def insertion_sort(comp, arr):
	# function: sort a given array arr in ascending order
	# approach: incremental
	# methodology: for each element, move it down until it's its sandwiched by two that are less and greater than it
	comp.start_timing()
	for j in range(1, len(arr)):
		arr_j = arr[j]
		# i counts down from j-1 to 0. book used while loop, but difficult to count execution. this is the same though
		for i in reversed(range(j)):
			comp.add_step()
			if arr[i] > arr_j:  # if earlier element arr[i] is greater than current element arr_j
				arr[i+1] = arr[i]  # swap them (then move down one more and swap those two, until no longer larger)
				if i == 0:
					i -= 1  # book has a while loop, so it subtracts one the last time at the end
			else:  # if earlier element arr[i] is NOT greater than current element arr_j, found a good sandwich, break
				break
		arr[i+1] = arr_j  # when swaping, don't need to set earlier one every time, just once at the end
	comp.end_timing()
	return arr


def like_merge_sort(comp, arr, start=True):

	def merge(arr_1, arr_2):
		# function: merge together two already sorted arrays, but make sure the final array is also sorted
		# approach: incremental
		# methodology: grab the first (lowest) element of each, and put the lowest of the 2 into the merge_result array,
		# pull another, repeat
		a = len(arr_1)
		b = len(arr_2)
		n = a + b
		i, j = 0, 0
		merge_result = []
		if arr_1[a-1] <= arr_2[0]:  # if last element of arr_1 is less than first element of arr_2
			comp.add_step()
			merge_result = arr_1 + arr_2  # that means all of arr_1 is less than all of arr_2, so result is just this
		elif arr_2[b-1] <= arr_1[0]:  # same idea
			comp.add_step()
			merge_result = arr_2 + arr_1
		else:  # if one array is not totally lower than another array, do the methodology described above
			for _ in range(n):
				comp.add_step()
				# if reached the end of arr_2 (j>=b), just set arr_1 values every time
				# or if (making sure still i < a) arr_1's current element < arr_2's current element
				if j >= b or (i < a and arr_1[i] < arr_2[j]):
					merge_result += [arr_1[i]]  # put arr_1's element into the results
					i += 1  # and pull another from arr_1
				elif i >= a or (j < b and arr_1[i] >= arr_2[j]):  # same idea
					merge_result += [arr_2[j]]
					j += 1
		return merge_result

	# merge_sort
	# function: sort a given array arr in ascending order
	# approach: divide and conquer (recursive)
	# methodology: merge merges 2 sorted arrays. assuming merge_sort sorts arrays, split arr into 2, merge_sort each,
	# then merge them. when you break it down, what happens is it divides and divides arr into a bunch of 1 or 2-element
	# arrays, swaps lower to earlier, merges into a few 4 or 5-element sorted arrays and come out to arr_a arr_b,
	# which merge into 8 or 9-element arrays, repeating
	if start:
		comp.start_timing()
	n = len(arr)
	if n <= 1:  # if down to 1-element array, it is sorted, just set it, this ends the recursion
		result = arr.copy()
	else:  # if 2 or more elements, divide into 2 arrays and sort (merge_sort) them each and merge them 
		a = int(n / 2)  # this rounds down
		arr_a = like_merge_sort(comp, arr[:a], start=False)
		arr_b = like_merge_sort(comp, arr[a:], start=False)
		result = merge(arr_a, arr_b)
	if start:
		comp.end_timing()
	return result


def merge_sort(comp, arr, p=None, r=None):

	def merge(arr, p_m, q_m, r_m):
		# function: merge together two already sorted arrays, but make sure the final array is also sorted
		# approach: incremental
		# methodology: 
		print(arr[p_m:q_m+1], arr[q_m+1:r_m+1])
		if arr[q_m] <= arr[q_m+1]:
			#print('HERE1')
			comp.add_step()
			return
		#elif arr[p_m] >= arr[r_m]:
		#	print('HERE2')
		#	comp.add_step()
		#	arr1, arr2 = arr[p_m:q_m+1], arr[q_m+1:r_m+1]
		#	arr = arr2 + arr1
		#	return
		i, j = 0, 0
		n1, n2 = q_m - p_m, r_m - (q_m + 1)
		arr1, arr2 = arr[p_m:q_m+1], arr[q_m+1:r_m+1]
		for k in range(p_m, r_m+1):
			comp.add_step()
			if j >= n2 or (i < n1 and arr1[i] <= arr2[j]):
				#print('HERE3')
				print(len(arr)-1, k, len(arr1)-1, n1, i, j, n2)
				arr[k] = arr1[i]
				i += 1
			elif i >= n1 or (j < n2 and arr1[i] > arr2[j]):
				#print('HERE4')
				arr[k] = arr2[j]
				j += 1
		return

	# merge_sort
	# function: sort a given array arr in ascending order
	# approach: divide and conquer (recursive)
	# methodology: 
	if p is None and r is None:
		comp.start_timing()
		p_new, r_new = 0, len(arr)-1
	else:
		p_new, r_new = p, r
	if p_new < r_new:
		q = int((p_new + r_new) / 2)
		merge_sort(comp, arr, p_new, q)
		merge_sort(comp, arr, q+1, r_new)
		merge(arr, p_new, q, r_new)
	if p is None and r is None:
		comp.end_timing()
	return arr



def quick_sort(comp, arr, left=None, right=None):

	def partition(arr, left_p, right_p):
		arr_right_p = arr[right_p]
		i = left_p - 1
		for j in range(left_p, right_p):
			comp.add_step()
			if arr[j] < arr_right_p:
				i += 1
				arr[i], arr[j] = arr[j], arr[i]
		arr[right_p], arr[i+1] = arr[i+1], arr[right_p]
		return i + 1

	if left is None and right is None:
		comp.start_timing()
		left_new, right_new = 0, len(arr)-1
	else:
		left_new, right_new = left, right

	if left_new < right_new:
		pivot = partition(arr, left_new, right_new)
		quick_sort(comp, arr, left_new, pivot-1)
		quick_sort(comp, arr, pivot+1, right_new)
	if left is None and right is None:
		comp.end_timing()
	return arr


def test(simple=False):
	algo_list = [
		#Algorithm(function=selection_sort, checker=sort_checker, order=3),
		#Algorithm(function=modified_selection_sort, checker=sort_checker, order=3),
		#Algorithm(function=bubble_sort, checker=sort_checker, order=3),
		#Algorithm(function=like_insertion_sort, checker=sort_checker, order=3),
		#Algorithm(function=insertion_sort, checker=sort_checker, order=3),
		#Algorithm(function=like_merge_sort, checker=sort_checker, order=2),
		Algorithm(function=merge_sort, checker=sort_checker, order=2),
		#Algorithm(function=quick_sort, checker=sort_checker, order=2),
	]
	if simple:
		return simple_check(algo_list)
	else:
		return deep_dive(algo_list)
