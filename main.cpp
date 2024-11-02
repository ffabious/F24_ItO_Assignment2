#include <bits/stdc++.h>

using namespace std;


class Matrix {
private:
    int n; // rows
    int m; // cols
    vector <vector<double>> data;

public:
    Matrix(int numberOfRows, int numberOfColumns) : n(numberOfRows), m(numberOfColumns) {
        data.resize(n);
        for (auto &el : data) {
            el.resize(m);
        }
    }

    void inputData() {
        for (int i = 0; i < n; i++)
            for (int j = 0; j < m; j++) {
                cin >> data[i][j];
            }
    }

    void printData() {
        cout << fixed << setprecision(3);
        for (auto &row : data) {
            for (auto &el : row) cout << el << "\t";
            cout << '\n';
        }
    }
    
    void gaussJordanIteration(int rowId, int changerId, double coefficient) {
        for (int j = 0; j < m; j++) {
            data[rowId][j] += data[changerId][j] * coefficient;
        }
    }
};

class Vector : public Matrix {
public:
    Vector(int numberOfElements) : Matrix(numberOfElements, 1) {}
};

class InteriorPoint {
private:
    Vector C;
    Matrix A;
    Vector b;
    double alpha = 0.5;
    double eps = 0.01;
public:
    InteriorPoint(int numberOfCoefficients, int numOfRowsA, int numOfColsA) {
        Vector C(numberOfCoefficients);
        Matrix A(numOfRowsA, numOfColsA);
        Vector b(numOfRowsA);
    }

    void inputC() {
        C.inputData();
    }
    
};


int main() {
    int a, b;
    cin >> a >> b;
    Matrix matrix(a, b);
    matrix.inputData();
    matrix.printData();
}