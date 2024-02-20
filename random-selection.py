import numpy as np

project_numbers = [0, 1, 2, 3, 5, 6, 7]
# sizes = [3, 3, 3, 3, 4, 3, 3, 3, 4]
sizes = 4 * np.ones(9, dtype=int)
preferences = np.array([
  [1000, 1000, 3, 1000, 1, 1000, 1000, 2, 1000],
  [1000, 1000, 1000, 2, 3, 1000, 4, 1000, 1],
  [4, 1000, 1000, 1000, 2, 1000, 1000, 3, 1],
  [1000, 1000, 1000, 1000, 2, 1000, 3, 4, 1],
  [1000, 1000, 1000, 1000, 1, 1000, 1000, 3, 2],
  [3, 1000, 1000, 1000, 1, 1000, 2, 1000, 1000],
  [2, 1000, 1000, 1, 1000, 3, 1000, 4, 1000],
  [3, 1000, 2, 1000, 1000, 4, 1, 1000, 1000],
  [1000, 1000, 1000, 1000, 4, 1000, 3, 1000, 1],
  [1000, 1000, 1000, 1000, 3, 1000, 4, 1000, 1],
  [2, 1000, 1000, 1000, 1, 4, 3, 1000, 1000],
  [1000, 2, 1000, 1000, 1000, 3, 1000, 1, 1000],
  [2, 1000, 1000, 1000, 1000, 3, 1, 1000, 1000],
  [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1],
  [1000, 2, 1, 1000, 1000, 4, 3, 1000, 1000],
  [3, 1000, 1000, 2, 1000, 1000, 1, 1000, 1000],
  [1000, 1000, 1, 1000, 1000, 1000, 2, 1000, 1000],
  [1000, 1000, 1000, 1, 1000, 1000, 2, 1000, 1000],
  [1000, 1000, 1000, 1000, 1000, 1000, 1, 1000, 1000],
])

combinations = []

for i in range(len(project_numbers)):
    for j in range(i + 1, len(project_numbers)):
        for k in range(j + 1, len(project_numbers)):
            combinations.append((project_numbers[i], project_numbers[j], project_numbers[k], 4, 8))

def attempt_swap(assignments, preferences, combination):
    for j in range(5):
        for k in assignments[j]:
            for l in range(j+1, 5):
                for m in assignments[l]:
                    if preferences[k, combination[j]] + preferences[m, combination[l]] > preferences[k, combination[l]] + preferences[m, combination[j]]:
                        assignments[j].remove(k)
                        assignments[l].remove(m)
                        assignments[j].append(m)
                        assignments[l].append(k)
                        score_delta = ((preferences[k, combination[j]] + preferences[m, combination[l]]) - (preferences[k, combination[l]] + preferences[m, combination[j]]))
                        return True, score_delta
    return False, 0

overall_best_combination = None
overall_best_assignments = None
overall_best_score = 9999
max_iterations = 100

while max_iterations > 0:
    randomly_generated_student_order = np.random.permutation(preferences.shape[0])
    # randomly_generated_student_order = np.range(preferences.shape[0])

    flag = False
    best_combination = None
    best_assignments = None
    best_score = 9999

    for combination in combinations:
        score = 0
        assignments = [[], [], [], [], []]
        reduced_preferences = preferences[:, combination]
        reduced_sizes = [sizes[i] for i in combination]
        for row_index in randomly_generated_student_order:
            flag = False
            for i in [1, 2, 3, 4, 1000]:
                if flag:
                    break
                for j, element in enumerate(reduced_preferences[row_index]):
                    if element == i:
                        if (len(assignments[j]) < reduced_sizes[j]):
                            assignments[j].append(row_index)
                            score += i
                            flag = True
                            break

        swap_possible = True
        while swap_possible:
            swap_possible, score_delta = attempt_swap(assignments, preferences, combination)
            score -= score_delta

        if score < best_score:
            best_combination = combination
            best_assignments = assignments
            best_score = score

    # print(best_combination)
    # print(best_assignments)
    # print(best_score)
            
    if best_score < overall_best_score:
        overall_best_combination = best_combination
        overall_best_assignments = best_assignments
        overall_best_score = best_score
    max_iterations -= 1

print(overall_best_combination)
print(overall_best_assignments)
print(overall_best_score)

# for i in range(5):
#     for j in overall_best_assignments[i]:
#         if preferences[j, overall_best_combination[i]] > 2:
#             print(f"Student {j} is not happy with their assignment.")