from copy import deepcopy


class Matrix:
    def __init__(self, matrix_list):
        self.matrix = deepcopy(matrix_list)
        self.sz = (len(matrix_list), len(matrix_list[0]))
        for i in range(self.sz[0]):
            for j in range(self.sz[1]):
                self.matrix[i][j] = self.matrix[i][j]

    def size(self):
        return self.sz

    @staticmethod
    def zero_matrix(n, m):
        return [[0 for __ in range(m)] for _ in range(n)]

    @staticmethod
    def E_matrix(n):
        new_matrix = Matrix.zero_matrix(n, n)
        for i in range(n):
            new_matrix[i][i] = 1
        return Matrix(new_matrix)

    def __str__(self):
        str_matr = ''
        for line in self.matrix:
            for el in line:
                str_matr += str(el)
                str_matr += '\t'
            str_matr = str_matr[:-1]
            str_matr += '\n'
        str_matr = str_matr[:-1]
        return str_matr

    def __add__(self, other):
        n, m = self.size()
        n_, m_ = other.size()
        if n != n_ or m != m_:
            raise MatrixError(self, other)
        new_matrix = Matrix.zero_matrix(n, m)
        for i in range(n):
            for j in range(m):
                new_matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]
        return Matrix(new_matrix)

    def __iadd__(self, other):
        n, m = self.size()
        n_, m_ = other.size()
        if n != n_ or m != m_:
            raise MatrixError(self, other)
        for i in range(n):
            for j in range(m):
                self.matrix[i][j] += other.matrix[i][j]
        return self

    def __mul__(self, other):
        n, m = self.size()

        if isinstance(other, int):
            new_matrix = Matrix.zero_matrix(n, m)
            for i in range(n):
                for j in range(m):
                    new_matrix[i][j] = other * self.matrix[i][j]
            return Matrix(new_matrix)

        if isinstance(other, Matrix):
            n_, m_ = other.size()
            if m != n_:
                raise MatrixError(self, other)
            new_n = n
            new_m = m_
            len_ = m
            new_matrix = Matrix.zero_matrix(new_n, new_m)
            for i in range(new_n):
                for j in range(new_m):
                    value = 0
                    for k in range(len_):
                        value += self.matrix[i][k] * other.matrix[k][j]
                    new_matrix[i][j] = value
            return Matrix(new_matrix)

    def __rmul__(self, other):
        n, m = self.size()
        new_matrix = Matrix.zero_matrix(n, m)
        for i in range(n):
            for j in range(m):
                new_matrix[i][j] = other * self.matrix[i][j]
        return Matrix(new_matrix)

    def __imul__(self, other):
        n, m = self.size()

        if isinstance(other, int):
            for i in range(n):
                for j in range(m):
                    self.matrix[i][j] *= other
            return self

        if isinstance(other, Matrix):
            n_, m_ = other.size()
            if m != n_:
                raise MatrixError(self, other)
            new_n = n
            new_m = m_
            len_ = m
            new_matrix = Matrix.zero_matrix(new_n, new_m)
            for i in range(new_n):
                for j in range(new_m):
                    value = 0
                    for k in range(len_):
                        value += self.matrix[i][k] * other.matrix[k][j]
                    new_matrix[i][j] = value
            self.matrix = deepcopy(new_matrix)
            self.sz = (new_n, new_m)
            return self

    def __pow__(self, power, modulo=None):
        n, m = self.size()
        new_matrix = deepcopy(self)
        res_matrix = Matrix.E_matrix(n)
        while power:
            if power % 2 == 1:
                res_matrix *= new_matrix
                power -= 1
            new_matrix *= new_matrix
            power /= 2
        return res_matrix

    def __eq__(self, other):
        return self.matrix == other.matrix

    def transpose(self):
        n, m = self.size()
        new_matrix = Matrix.zero_matrix(n, m)
        for i in range(m):
            for j in range(n):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = deepcopy(new_matrix)
        self.sz = (m, n)
        return self

    def tr(self):
        n, m = self.size()
        res = 0
        for i in range(n):
            res += self.matrix[i][i]
        return res

    @staticmethod
    def transposed(matrix):
        n, m = matrix.size()
        new_matrix = Matrix.zero_matrix(n, m)
        for i in range(m):
            for j in range(n):
                new_matrix[i][j] = matrix.matrix[j][i]
        return Matrix(new_matrix)


class Polynomial:
    def __init__(self, power, *coefficients):
        self.power = power
        self.coef = coefficients

    def __call__(self, x):
        res = self.coef[self.power] * x**self.power
        for i in range(self.power):
            res += self.coef[i] * x**i
        return res


class MatrixError(Exception):
    def __init__(self, m1, m2):
        self.matrix1 = m1
        self.matrix2 = m2
