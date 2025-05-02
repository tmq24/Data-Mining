def longestCommonSubsequence(X, Y):
    m = len(X)
    n = len(Y)
    
    # Initialize the LCS matrix and direction matrix for backtracking
    LCS = [[0] * (n + 1) for _ in range(m + 1)]
    direction = [[None] * (n + 1) for _ in range(m + 1)]
    
    # Initialize the first row and the first column to 0
    for i in range(m + 1):
        LCS[i][0] = 0
    for j in range(n + 1):
        LCS[0][j] = 0
    
    # Fill the LCS matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                LCS[i][j] = LCS[i - 1][j - 1] + 1
                direction[i][j] = 'DIAGONAL' 
            else:
                if LCS[i - 1][j] >= LCS[i][j - 1]:
                    LCS[i][j] = LCS[i - 1][j]
                    direction[i][j] = 'UP'
                else:
                    LCS[i][j] = LCS[i][j - 1]
                    direction[i][j] = 'LEFT' 
    
    # Backtrack to find the common subsequence
    lcss_sequence = []
    i, j = m, n
    while i > 0 and j > 0:
        if direction[i][j] == 'DIAGONAL':
            lcss_sequence.append(X[i - 1])
            i -= 1
            j -= 1
        elif direction[i][j] == 'UP':
            i -= 1
        else: 
            j -= 1
    lcss_sequence.reverse()
    
    return LCS[m][n], lcss_sequence

if __name__ == "__main__":
    print("text X:")
    X = input().strip()
    print("text Y:")
    Y = input().strip()
    
    length, sequence = longestCommonSubsequence(X, Y)
    
    print(f"LCS length: {length}")
    print(f"Longest common subsequence: {''.join(sequence)}")
