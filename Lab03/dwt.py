def dynamicTimeWarping(x, y):
    n, m = len(x), len(y)
    
    dtw = [[float('inf') for _ in range(m+1)] for _ in range(n+1)]
    dtw[0][0] = 0
    
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = abs(x[i-1] - y[j-1])
            
            dtw[i][j] = cost + min(dtw[i-1][j],    # repeat y_j
                                  dtw[i][j-1],     # repeat x_i
                                  dtw[i-1][j-1])   # repeat neither
    
    path = []
    i, j = n, m
    
    while i > 0 or j > 0:
        path.append((i-1, j-1))
        
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        else:
            min_val = min(dtw[i-1][j], dtw[i][j-1], dtw[i-1][j-1])
            
            if min_val == dtw[i-1][j-1]:
                i -= 1
                j -= 1
            elif min_val == dtw[i-1][j]:
                i -= 1
            else:
                j -= 1
    
    
    values = [dtw[i+1][j+1] for i, j in path]
    
    return dtw[n][m], path, values

if __name__ == "__main__":
    series1 = [1, 7, 4, 8, 2, 9, 6, 5, 2, 0]
    series2 = [1, 2, 8, 5, 5, 1, 9, 4, 6, 5]

    # Tính DTW
    distance, path, values = dynamicTimeWarping(series1, series2)
    
    print(f"Khoảng cách DTW: {distance}")
    print(f"Đường dẫn căn chỉnh: {path}")
    print(f"Các giá trị DTW: {values}")