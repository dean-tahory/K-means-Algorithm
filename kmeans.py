from operator import le
import sys
import math


def terminate():
    print("Invalid Input!")
    exit()


def is_valid_path(path):
    if isinstance(path, str):
        if len(path.split('.')) == 2:
            if path.split('.')[1] == 'txt':
                return True
    return False


def distance(u: list[float], v: list[float]) -> float:
    """calculating euclidean distance of given vectors"""
    if len(u) != len(v):
        print("the vectors aren't the same size")
        terminate()
    d = 0
    for i in range(len(u)):
        d += (u[i] - v[i]) * (u[i] - v[i])
    return math.sqrt(d)


def points_sum(u: list[float], v: list[float]) -> list[float]:
    """summarises the given vector points"""
    if len(u) != len(v):
        print("the vectors aren't the same size")
        terminate()
    s = [0.0]*len(u)
    for i in range(len(u)):
        s[i] = u[i] + v[i]
    return s


# correct format: K max_iter(optional) input.txt output.txt
# first step: validate command line foramt :
if len(sys.argv) == 4:
    if not sys.argv[1].isnumeric():
        terminate()
    K = int(sys.argv[1])
    max_iter = 200
    input_path = sys.argv[2]
    output_path = sys.argv[3]
    if not is_valid_path(input_path) or not is_valid_path(output_path):
        terminate()

elif len(sys.argv) == 5:
    if (not sys.argv[1].isnumeric() or not sys.argv[2].isnumeric()):
        terminate()
    K = int(sys.argv[1])
    max_iter = int(sys.argv[2])
    if max_iter == 0:
        terminate()
    input_path = sys.argv[3]
    output_path = sys.argv[4]
    if not is_valid_path(input_path) or not is_valid_path(output_path):
        terminate()
else:
    terminate()

# second step: reading the input, checking if K < N
points, centroids = [], []
try:
    with open(input_path) as file:
        line = file.readline()
        while line:
            line = line.split(',')
            line.append(line.pop().strip())
            points.append([float(e) for e in line])
            line = file.readline()
    if K >= len(points):
        terminate()
except FileNotFoundError as fnf_error:
    print("An Error Has Occurred")
    file.close()


# third step: the algorithm itself
def k_means(K, max_iter, points: list[list[float]]):

    centroids = [points[i] for i in range(K)]

    # dict mapping points indexes to centroids indexes
    points_to_centroids = {i: 0 for i in range(len(points))}

    diff_small = [True]*len(centroids)

    for l in range(max_iter):
        # iterating points and update their centorid's index
        # for point_index, centroid_index in points_to_centroids.items():
        for i in range(len(points_to_centroids)):
            new_centroid = points_to_centroids[i]
            for j in range(K):
                if distance(centroids[j], points[i]) < distance(centroids[new_centroid], points[i]):
                    new_centroid = j
            points_to_centroids[i] = new_centroid

        # calculating new centroids
        for i in range(K):
            diff_small[i] = False
            total = [0.0] * len(points[0])
            counter = 0
            for j in range(len(points_to_centroids)):
                if points_to_centroids[j] == i:
                    total = points_sum(points[j], total)
                    counter += 1.0
            if(counter > 0):
                new_centroid = [total[j]/counter for j in range(len(total))]
                if (distance(centroids[i], new_centroid) < 0.001):
                    diff_small[i] = True
                centroids[i] = new_centroid
        if all(diff_small[i] for i in range(len(diff_small))):
            break
    return centroids


def k_means_v2(K, max_iter, points):
    centroids = [points[i] for i in range(K)]

    # array where the indexes are points and the entries are centroids indexes
    points_to_centroids = [0]*len(points)

    small_delta = False

    for l in range(max_iter):
        # iterating points and update their centorid's index
        for i in range(len(points)):
            new_centroid = points_to_centroids[i]
            for j in range(K):
                if distance(centroids[j], points[i]) < distance(centroids[new_centroid], points[i]):
                    new_centroid = j
            points_to_centroids[i] = new_centroid

        # calculating new centroids
        for i in range(K):
            small_delta = True
            total = [0.0] * len(points[0])
            counter = 0
            for j in range(len(points)):
                if points_to_centroids[j] == i:
                    total = points_sum(points[j], total)
                    counter += 1.0

            if(counter > 0):
                new_centroid = [total[j]/counter for j in range(len(total))]
                if (distance(centroids[i], new_centroid) < 0.001):
                    small_delta = False
                centroids[i] = new_centroid
        if not small_delta:
            break
    return centroids


# fourth step: writing output
centroids = k_means(K, max_iter, points)
for c in centroids:
    for i in range(len(c)):
        c[i] = f'{c[i]:.4f}'
centroids = [','.join(c) for c in centroids]
with open('output.txt', 'w') as f:
    for c in centroids:
        f.write(f'{c}\n')
