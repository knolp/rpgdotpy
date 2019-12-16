		if state_handler.gamemap:
			for item in state_handler.gamemap.game_map.objects:
					print("checking monsters")
					if item.type == "monster":
						#check target
						target_direction = False
						breakable = False
						_directions = {
							"d" : (1,0),
							"u" : (-1, 0),
							"l" : (0,-1),
							"r" : (0, 1)
						}
						original_position = (item.x, item.y)

						for k,v in _directions.items():
							check = [original_position[0], original_position[1]]
							for i in range(5):
								check[0] += v[0]
								check[1] += v[1]

								if check[0] == state_handler.player.x and check[1] == state_handler.player.y:
									target_direction = k
									breakable = True
									break
							if breakable:
								break

		# 				print(breakable)
		# 				if breakable:
		# 					check = [original_position[0], original_position[1]]
		# 					while check[0] != state_handler.player.x or check[1] != state_handler.player.y:
		# 						print(check[0])
		# 						item.path_to_target.append((check[0],check[1]))
		# 						check[0] += _directions[target_direction][0]
		# 						check[1] += _directions[target_direction][1]