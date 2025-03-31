INSTRUCTION_PENALTY = -0.1


def levenshtein_distance(s1, s2):
    # Create a matrix to store distances
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize the matrix
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Compute the distances
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,        # Deletion
                dp[i][j - 1] + 1,        # Insertion
                dp[i - 1][j - 1] + cost  # Substitution
            )

    return dp[m][n]


if __name__ == '__main__':
    print(levenshtein_distance(
        'test1',
        'test2'
    ))
