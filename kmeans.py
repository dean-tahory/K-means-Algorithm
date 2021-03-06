
import sys
import math


def invalid_input():
    print("Invalid Input!")
    exit()


def other_error():
    print("An Error Has Occurred")
    exit()


def is_valid_path(path):
    if len(path.split('.')) == 2:
        if path.split('.')[1] == 'txt':
            return True
    return False


def distance(u, v):
    """calculating euclidean distance of given vectors"""
    if len(u) != len(v):
        other_error()
    d = 0
    for i in range(len(u)):
        d += (u[i] - v[i]) * (u[i] - v[i])
    return math.sqrt(d)


def points_sum(u, v):
    """summarises the given vector points"""
    if len(u) != len(v):
        other_error()
    s = [0.0]*len(u)
    for i in range(len(u)):
        s[i] = u[i] + v[i]
    return s


def sum_vector(u, v):
    if(len(u) != len(v)):
        other_error()
    s = [0]*len(u)
    for i in range(len(u)):
        s[i] = u[i]+v[i]


# correct format: K max_iter(optional) input.txt output.txt
# first step: validate command line foramt :
if len(sys.argv) == 4:
    if not sys.argv[1].isnumeric():
        invalid_input()
    K = int(sys.argv[1])
    max_iter = 200
    input_path = sys.argv[2]
    output_path = sys.argv[3]
    if not is_valid_path(input_path) or not is_valid_path(output_path):
        invalid_input()

elif len(sys.argv) == 5:
    if (not sys.argv[1].isnumeric() or not sys.argv[2].isnumeric()):
        invalid_input()
    K = int(sys.argv[1])
    max_iter = int(sys.argv[2])
    if max_iter == 0:
        invalid_input()
    input_path = sys.argv[3]
    output_path = sys.argv[4]
    if not is_valid_path(input_path) or not is_valid_path(output_path):
        invalid_input()
else:
    invalid_input()

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
        invalid_input()
except FileNotFoundError as fnf_error:
    other_error()


# third step: the algorithm itself
def k_means(K, max_iter, points):

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


# fourth step: writing output
centroids = k_means(K, max_iter, points)
for c in centroids:
    for i in range(len(c)):
        c[i] = f'{c[i]:.4f}'
centroids = [','.join(c) for c in centroids]

try:
    with open(output_path, 'w') as f:
        for c in centroids:
            f.write(f'{c}\n')
except FileNotFoundError as fnf_error:
    other_error()
