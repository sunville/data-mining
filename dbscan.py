# import matplotlib.pyplot as plt #for visualizing the result

parameter = {
	'theta':2.0,
	'MinPts':3,
}


def ball(point, theta, dataset):
	count = 0
	for p in dataset:
		dist = pow(p[0] - point[0], 2) + pow(p[1] - point[1], 2)
		if dist <= pow(theta, 2):
			count += 1

	return count


def ballNeighbors(point, theta, corePoints):
	localCluster = []
	for p in corePoints:
		dist = pow(p[0] - point[0], 2) + pow(p[1] - point[1], 2)
		if dist <= pow(theta, 2) and dist > 0:
			localCluster.append(p)
	return localCluster


def find_start(clusters, corePoints):
	union = set()
	for cluster in clusters:
		union |= cluster
	for point in corePoints:
		p = str(point[0])+','+str(point[1])
		if len(union) == 0 or p not in union:
			return point


def dbscan(dataset):
	corePoints=[]
	noncorePoints=[]
	clusters = []
	noise = []
	# divide points into core and noncore points
	for point in dataset:
		if ball(point,parameter['theta'],dataset) >= parameter['MinPts'] :
			corePoints.append(point)
		else:
			noncorePoints.append(point)
	#cluster core points using bfs
	count = 0
	while count < len(corePoints):
		start_point = find_start(clusters, corePoints)
		visited, stack = set(), [start_point]
		while stack:
			point = stack.pop()
			str_point = str(point[0])+','+str(point[1])
			if str_point not in visited:
				visited.add(str_point)
				localCluster = ballNeighbors(point,parameter['theta'], corePoints)
				stack.extend(localCluster)
				count += 1
		clusters.append(visited)

	for point in noncorePoints:
		localCluster = ballNeighbors(point,parameter['theta'], corePoints)
		if len(localCluster) == 0:
			# The point is noise
			noise.append(point)
			continue
		else:
			str_point = str(point[0])+','+str(point[1])
			for p in localCluster:
				str_p = str(p[0])+','+str(p[1])
				for cluster in clusters:
					if str_p in cluster:
						cluster.add(str_point)

	print("Noise points:")
	print(noise)
	index = 1
	for cluster in clusters:
		print("Cluster " + str(index))
		cluster_points = [[float(p.split(',')[0]), float(p.split(',')[1])] for p in cluster]
		print(cluster_points)
		index += 1


	# For visualizing result
	# cmap = ['b','g','r','c','m','y']
	# for i in range(0,len(clusters)):
	# 	cluster_points = [[float(p.split(',')[0]), float(p.split(',')[1])] for p in clusters[i]]
	# 	plt.scatter([p[0] for p in cluster_points], [p[1] for p in cluster_points], color=cmap[i])
	# plt.show()


def main():
	dataset=[]
	with open('data.txt') as f:
		for line in f:
			dataset.append([float(x) for x in line.split('\t')])
	f.close()
	dbscan(dataset)



if __name__ == '__main__':
	main()