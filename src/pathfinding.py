# A STAR

import math


class MapObject():
	def __init__(self, x, y, walkable=True):
		self.x = x
		self.y = y
		self.walkable = walkable
		self.position = (x,y)

class Node():
	def __init__(self, parent=None, position=None):
		self.parent = parent
		self.position = position

		self.g = 0
		self.h = 0
		self.f = 0


	def __eq__(self, other):
		return self.position == other.position

def astar(gamemap, start, end, state=False):
	counter = 0
	weight = 1
	if state:
		start = (start[0] - 1, start[1] - 1)
		end = (end[0] - 1, end[1] - 2)

	start_node = Node(position=start)
	end_node = Node(position=end)

	if gamemap[end_node.position[0]][end_node.position[1]].walkable == False:
		return []

	closed_list = []
	closed_list2 = []
	open_list = []

	if start == end:
		return []

	open_list.append(start_node)

	while len(open_list) > 0: #Medan det finns noder att kolla
		if counter > 2000:
			#for item in open_list:
				#print("Open List: f", item.f, "position: ", item.position)
			return []

		open_list.sort(key=lambda x: x.f)
		#print(open_list)
		current_index = 0
		current_node = open_list.pop(current_index)

		#for index, item in enumerate(open_list):
		#	if item.f < current_node.f:
		#		current_node = item
		#		current_index = index



		
		closed_list.append(current_node)
		closed_list2.append(current_node.position)

		#print("Current node = ", current_node.position, current_node.f)

		if current_node == end_node:
			path = []
			current = current_node
			while current is not None:
				path.append(current.position)
				current = current.parent
			for i in range(len(path)):
				if state:
					path[i] = (path[i][0] + 1, path[i][1] + 1)
				else:
					path[i] = (path[i][0], path[i][1])

			#if state:
				#path[-1] = (path[-1][0] - 1, path[-1][0] - 1)
			print(counter)
			return path[::-1]


		#Create Children
		children = []
		for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
			node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

			#if node_position in [item.position for item in closed_list]:
			if node_position in closed_list2:
				#print("Neighbour node position in closed list")
				continue

			if node_position[0] > len(gamemap) - 1 or node_position[1] > len(gamemap[0]) - 1:
				#print("out of bounds")
				continue

			if node_position[0] < 0 or node_position[1] < 0:
				#print("under 0")
				continue
			try:
				if gamemap[node_position[0]][node_position[1]].walkable == False:
					#print("Not walkable")
					continue

				if gamemap[node_position[0]][node_position[1]].executable == True:
					#print("Not walkable")
					continue

			except IndexError:
				#print(node_position)
				return []


			new_node = Node(parent=current_node, position=node_position)
			children.append(new_node)

		#Calculate g,h,f for each child
		for child in children:

			#check if it is closed list
			#if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
				#pass

			child.g = (child.parent.g + 1)
			#child.h = math.floor(math.sqrt((child.position[0] - end_node.position[0]) **2 + (child.position[1] - end_node.position[1]) **2))
			child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
			child.f = child.g + child.h

			#Check if it is in the open_list already
			if child in open_list:
				continue

			open_list.append(child)

		#for item in children:
		#	#print("ChildList",item.position, item.f)

		#for item in open_list:
		#	#print("OpenList", item.position, item.f)
		counter += 1

		#if counter == 10:
		#	break









if __name__ == '__main__':
	#maze = [[0,0,0,0,0],
	#		[0,0,0,0,0],
	#		[0,0,0,1,0],
	#		[0,0,0,1,0],
	#		[0,0,0,1,0]]

	maze = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

	maze_map = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

	for x in range(len(maze)):
		for y in range(len(maze[x])):
			if maze_map[x][y] == 0:
				maze_map[x][y] = MapObject(x,y)
			else:
				maze_map[x][y] = MapObject(x,y, walkable=False)

	#print("length",len(maze), len(maze[0]))

	path = astar(maze_map,(2,1),(15,15))

	for item in path:
		maze[item[0]][item[1]] = 3

	#for item in maze:
		#print(item)

