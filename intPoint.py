import numpy as np
from numpy.linalg import norm


eps = 0.00001
alpha = 0.5

# c = np.array(input(), float)

# A = np.array([[]], float)

# n = int(input())

class Matrix:
    rowCount : int
    colCount : int
    data : list
    def __init__(self, data : list):
        self.data = data
        self.rowCount = len(data)
        self.colCount = len(data[0])

class MatrixOperations:
    
    def diag(vector : list):
        result = [[0.0] * len(vector) for _ in range(len(vector))]
        for i in range(len(vector)):
            result[i][i] = vector[i]
        return Matrix(result)
    def eye(n : int) -> Matrix:
        result = [[0.0] * n for _ in range(n)]
        for i in range(n):
            result[i][i] = 1
        return Matrix(result)
    def add(a : Matrix, b : Matrix):
        result = [[0.0] * a.colCount for _ in range(a.rowCount)]
        for i in range(a.rowCount):
            for j in range(a.colCount):
                result[i][j] = a.data[i][j] + b.data[i][j]
        return Matrix(result)
    def subtract(a : Matrix, b : Matrix):
        result = [[0.0] * a.colCount for _ in range(a.rowCount)]
        for i in range(a.rowCount):
            for j in range(a.colCount):
                result[i][j] = a.data[i][j] - b.data[i][j]
        return Matrix(result)
    def findNu(vector : Matrix):
        return abs(min(vector.data))
    def ones(n : int):
        return Matrix([1] * n)
    def dot(a : Matrix, b : Matrix):
        result = [[0.0] * b.colCount for _ in range(a.rowCount)]
        for i in range(a.rowCount):
            for j in range(b.colCount):
                temp = 0.0
                for k in range(b.rowCount):
                    temp += a.data[i][k] * b.data[k][j]
                result[i][j] = temp
        return result
    def transpose(a : Matrix):
        result = [[0.0] * a.rowCount for _ in range(a.colCount)]
        for i in range(a.rowCount):
            for j in range(a.colCount):
                result[j][i] = a.data[i][j]
        return Matrix(result)
    def inverse(self, a : Matrix):
        identity = [[0.0] * a.rowCount for _ in range(a.rowCount)]
        for i in range(a.rowCount):
            identity[i][i] = 1
        
        augmented = [a.data[i] + identity[i] for i in range(a.rowCount)]
        for i in range(a.rowCount):
            pivot = augmented[i][i]
            if pivot == 0:
                print("Matrix has no inverse")
                exit()
            for j in range(2 * a.colCount):
                augmented[i][j] /= pivot

            for k in range(a.rowCount):
                if k == i:
                    continue
                factor = augmented[k][i]
                for j in range(2 * a.colCount):
                    augmented[k][j] -= factor * augmented[i][j]
        inverse = [row[a.colCount:] for row in augmented]
        return Matrix(inverse)
    def norm(a : Matrix):
        return (sum(sum(el ** 2 for el in row) for row in a.data)) ** 0.5
    
    

class InteriorPoint:
    n: int
    rowCount : int
    colCount: int
    type: str
    eps: int
    xList: list
    AList: list
    bList: list
    cList: list
    mo : MatrixOperations

    def __init__(self, n: int, rowCount : int, colCount: int, type: str, eps: int = 0.00001):
        self.n = n
        self.rowCount = rowCount
        self.colCount = colCount
        self.xList = list()
        self.cList = list()
        self.AList = list()
        self.bList = list()
        self.type = type
        self.eps = eps

    def inputData(self):
        self.cList = list(map(float, input("Enter coefficients of the objective function: ").split()))
        if len(self.cList) != n:
            print("Error: incorrect number of coefficients in the objective function!")
            exit()
        print("Enter the matrix of coefficients of constraint functions (line by line with single space as separator):")
        for i in range(self.rowCount):
            temp_arr = list(map(float, input().split()))
            if len(temp_arr) != self.colCount:
                print("Error: incorrect number of elements in a row")
                exit()
            self.AList.append(temp_arr.copy())
            temp_arr.clear()
        self.b = list(map(float, input("Enter right-hand side values for the constraint functions (one line with space as separator): ").split()))
        if len(self.b) != self.rowCount:
            print(self.rowCount, len(self.b))
            print("Error: incorrect number of values!")
            exit()
        print("Enter the approximation accuracy or -1 to use default eps=0.00001: ", end='')
        new_eps = float(input())
        if new_eps == -1:
            pass
        elif new_eps < 0.0:
            print("Error: incorrect value of approximation accuracy!")
            exit()
        else:
            self.eps = new_eps

        self.xList = list(map(float, input("Enter initial solution: ").split()))

    def iteration(self):
        D = np.diag(self.x)
        AA = np.dot(self.A, D)
        cc = np.dot(D, self.c)
        I = np.eye(self.n)
        F = np.dot(AA, np.transpose(AA))
        FI = np.linalg.inv(F)
        H = np.dot(np.transpose(AA), FI)
        P = np.subtract(I, np.dot(H, AA))
        cp = np.dot(P, cc)
        nu = np.absolute(np.min(cp))
        y = np.add(np.ones(self.n, float), (alpha / nu) * cp)
        yy = np.dot(D, y)
        return yy
    
    def solve(self):
        self.x = np.array(self.xList, float)
        self.A = np.array(self.AList, float)
        self.b = np.array(self.bList, float)
        self.c = np.array(self.cList, float)

        new = self.iteration()
        while norm(np.subtract(self.x, new), ord = 2) >= self.eps:
            self.x = new
            new = self.iteration()
        
        for i in range(len(self.x) - self.rowCount):
            print(round(self.x[i], 2), end=' ')

if __name__ == "__main__":
    n = int(input("Enter the number of variables: "))
    rowCount, colCount = list(map(int, input("Enter row & col count: ").split()))
    ip = InteriorPoint(n, rowCount, colCount, "max")
    ip.inputData()
    ip.solve()
