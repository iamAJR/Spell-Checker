def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


def save_to_dictionary(file_path, word):
    with open(file_path, 'a') as file:
        file.write(word + "\n")

#this uses a O(m*n) space so by not using the matrix instead just two arrays we can reduce it to linear time
'''def edit_distance(s1, s2):
    x, y = len(s1), len(s2)
    matrix = [[0] * (y + 1) for _ in range(x + 1)]
    for i in range(x + 1):
        matrix[i][0] = i

    for j in range(y + 1):
        matrix[0][j] = j

    for i in range(1, x + 1):
        for j in range(1, y + 1):
            if s1[i - 1] == s2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                matrix[i][j] = 1 + min(matrix[i - 1][j - 1], matrix[i][j - 1], matrix[i - 1][j])

    return matrix[x][y]'''
def edit_distance(s1, s2):
    x, y = len(s1), len(s2)

    # Initialize the previous row
    prev = list(range(y + 1))

    # Iterate over each character in s1
    for i in range(1, x + 1):
        current = [0] * (y + 1)
        current[0] = i
        for j in range(1, y + 1):
            if s1[i - 1] == s2[j - 1]:
                current[j] = prev[j - 1]
            else:
                current[j] = 1 + min(prev[j - 1], current[j - 1], prev[j])
        prev = current

    return prev[y]

def check(w, dict_list):
    suggestions = []

    for possible in dict_list:
        dis = edit_distance(w, possible)
        suggestions.append((possible, dis))
    suggestions.sort(key=lambda x: x[1])

    return suggestions[:8]
