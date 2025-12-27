///*
//Big M Method for Linear Programming
//Complete Implementation with Step-by-Step Visualization
//C++ Version - Pure C++ with no external libraries
//
//The Big M Method handles problems with >=, <=, and = constraints by adding
//artificial variables with a large penalty M in the objective function.
//*/
//
#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <cmath>
#include <algorithm>
#include <limits>

using namespace std;

class BigMMethod {
private:
   int numVariables;
   int numConstraints;
   vector<double> objective;
   vector<vector<double>> constraints;
   vector<double> rhs;
   vector<int> constraintTypes;  // 1: <=, 2: >=, 3: =
   bool isMaximization;

   // Tableau variables
   vector<vector<double>> tableau;
   vector<string> varNames;
   vector<int> basicVars;
   double M;  // Big M value

   // Tracking
   int numSlack;
   int numSurplus;
   int numArtificial;
   vector<int> artificialIndices;
   int iteration;

   const double EPSILON = 1e-10;

public:
   BigMMethod() : numVariables(0), numConstraints(0), isMaximization(true),
       M(1000), numSlack(0), numSurplus(0), numArtificial(0), iteration(0) {
   }

   void getUserInput() {
       cout << "\n" << string(70, '=') << endl;
       cout << "              BIG M METHOD - LINEAR PROGRAMMING SOLVER" << endl;
       cout << "                   (Step-by-Step Solution)" << endl;
       cout << string(70, '=') << endl;

       // Problem type
       cout << "\nSelect Problem Type:" << endl;
       cout << "1. Maximization" << endl;
       cout << "2. Minimization" << endl;

       int choice;
       while (true) {
           cout << "\nEnter choice (1 or 2): ";
           cin >> choice;
           if (choice == 1 || choice == 2) {
               isMaximization = (choice == 1);
               break;
           }
           cout << "Please enter 1 or 2" << endl;
       }

       // Number of variables
       while (true) {
           cout << "\nEnter the number of decision variables: ";
           cin >> numVariables;
           if (numVariables > 0) break;
           cout << "Must be positive" << endl;
       }

       // Number of constraints
       while (true) {
           cout << "Enter the number of constraints: ";
           cin >> numConstraints;
           if (numConstraints > 0) break;
           cout << "Must be positive" << endl;
       }

       // Big M value
       cout << "\n--- BIG M VALUE ---" << endl;
       cout << "Enter the value of M (large positive number)" << endl;
       cout << "Recommended: Use a value much larger than your coefficients (e.g., 1000 or 10000)" << endl;
       cout << "Enter M value (press Enter for 1000): ";
       cin.ignore();
       string mInput;
       getline(cin, mInput);
       if (mInput.empty()) {
           M = 1000;
       }
       else {
           M = stod(mInput);
       }

       // Objective function
       cout << "\n--- OBJECTIVE FUNCTION ---" << endl;
       string objType = isMaximization ? "Maximize" : "Minimize";
       cout << objType << " Z = c1*x1 + c2*x2 + ... + c" << numVariables << "*x" << numVariables << endl;
       cout << "Enter the coefficients:" << endl;

       objective.resize(numVariables);
       for (int i = 0; i < numVariables; i++) {
           cout << "  Coefficient of x" << (i + 1) << ": ";
           cin >> objective[i];
       }

       // Constraints
       cout << "\n--- CONSTRAINTS ---" << endl;
       cout << "Constraint types: 1 = <=, 2 = >=, 3 = =" << endl;

       constraints.resize(numConstraints);
       constraintTypes.resize(numConstraints);
       rhs.resize(numConstraints);

       for (int i = 0; i < numConstraints; i++) {
           cout << "\nConstraint " << (i + 1) << ":" << endl;
           constraints[i].resize(numVariables);

           for (int j = 0; j < numVariables; j++) {
               cout << "  Coefficient of x" << (j + 1) << ": ";
               cin >> constraints[i][j];
           }

           while (true) {
               cout << "  Constraint type (1=<=, 2=>=, 3==): ";
               cin >> constraintTypes[i];
               if (constraintTypes[i] >= 1 && constraintTypes[i] <= 3) break;
               cout << "  Please enter 1, 2, or 3" << endl;
           }

           cout << "  Right-hand side (RHS) value: ";
           cin >> rhs[i];

           // Handle negative RHS
           if (rhs[i] < 0) {
               cout << "  Note: Negative RHS detected. Multiplying constraint by -1." << endl;
               for (int j = 0; j < numVariables; j++) {
                   constraints[i][j] = -constraints[i][j];
               }
               rhs[i] = -rhs[i];
               if (constraintTypes[i] == 1) constraintTypes[i] = 2;
               else if (constraintTypes[i] == 2) constraintTypes[i] = 1;
           }
       }

       displayProblem();
   }

   void displayProblem() {
       cout << "\n" << string(70, '=') << endl;
       cout << "                    FORMULATED LPP" << endl;
       cout << string(70, '=') << endl;

       string objType = isMaximization ? "Maximize" : "Minimize";

       // Objective function
       cout << "\n" << objType << " Z = ";
       for (int i = 0; i < numVariables; i++) {
           if (i > 0 && objective[i] >= 0) cout << "+ ";
           else if (objective[i] < 0) cout << "- ";
           cout << abs(objective[i]) << "x" << (i + 1) << " ";
       }
       cout << endl;

       // Constraints
       cout << "\nSubject to:" << endl;
       string typeSymbols[] = { "", "<=", ">=", "=" };

       for (int i = 0; i < numConstraints; i++) {
           cout << "  ";
           for (int j = 0; j < numVariables; j++) {
               if (j > 0 && constraints[i][j] >= 0) cout << "+ ";
               else if (constraints[i][j] < 0) cout << "- ";
               cout << abs(constraints[i][j]) << "x" << (j + 1) << " ";
           }
           cout << typeSymbols[constraintTypes[i]] << " " << rhs[i] << endl;
       }

       cout << "\n  x1, x2, ..., x" << numVariables << " >= 0" << endl;
       cout << "\n  Big M value = " << M << endl;
   }

   void createInitialTableau() {
       cout << "\n" << string(70, '=') << endl;
       cout << "           STEP 1: CONVERT TO STANDARD FORM (BIG M)" << endl;
       cout << string(70, '=') << endl;

       // Count different variable types
       numSlack = 0;
       numSurplus = 0;
       numArtificial = 0;

       for (int i = 0; i < numConstraints; i++) {
           if (constraintTypes[i] == 1) numSlack++;
           else if (constraintTypes[i] == 2) { numSurplus++; numArtificial++; }
           else numArtificial++;
       }

       cout << "\nAdding variables:" << endl;
       cout << "  - Slack variables (for <=): " << numSlack << endl;
       cout << "  - Surplus variables (for >=): " << numSurplus << endl;
       cout << "  - Artificial variables (for >= and =): " << numArtificial << endl;

       // Total columns
       int totalVars = numVariables + numSlack + numSurplus + numArtificial;
       int numRows = numConstraints + 1;
       int numCols = totalVars + 1;

       // Initialize tableau
       tableau.assign(numRows, vector<double>(numCols, 0.0));

       // Variable names
       varNames.clear();
       for (int i = 0; i < numVariables; i++) {
           varNames.push_back("x" + to_string(i + 1));
       }

       int slackIdx = numVariables;
       int surplusIdx = numVariables + numSlack;
       int artificialIdx = numVariables + numSlack + numSurplus;

       basicVars.clear();
       artificialIndices.clear();

       cout << "\nStandard form conversion:" << endl;

       // Fill constraint rows
       for (int i = 0; i < numConstraints; i++) {
           // Original variable coefficients
           for (int j = 0; j < numVariables; j++) {
               tableau[i][j] = constraints[i][j];
           }

           // Add appropriate variables
           if (constraintTypes[i] == 1) {  // <=
               tableau[i][slackIdx] = 1;
               varNames.push_back("s" + to_string(i + 1));
               basicVars.push_back(slackIdx);
               cout << "  Constraint " << (i + 1) << " (<=): Added slack variable s" << (i + 1) << endl;
               slackIdx++;
           }
           else if (constraintTypes[i] == 2) {  // >=
               tableau[i][surplusIdx] = -1;
               varNames.push_back("e" + to_string(i + 1));
               cout << "  Constraint " << (i + 1) << " (>=): Added surplus variable e" << (i + 1);
               cout << " and artificial variable a" << (i + 1) << endl;
               surplusIdx++;

               tableau[i][artificialIdx] = 1;
               varNames.push_back("a" + to_string(i + 1));
               basicVars.push_back(artificialIdx);
               artificialIndices.push_back(artificialIdx);
               artificialIdx++;
           }
           else {  // =
               tableau[i][artificialIdx] = 1;
               varNames.push_back("a" + to_string(i + 1));
               basicVars.push_back(artificialIdx);
               artificialIndices.push_back(artificialIdx);
               cout << "  Constraint " << (i + 1) << " (=): Added artificial variable a" << (i + 1) << endl;
               artificialIdx++;
           }

           // RHS
           tableau[i][numCols - 1] = rhs[i];
       }

       // Fill objective row
       cout << "\nObjective function with Big M penalty:" << endl;

       for (int j = 0; j < numVariables; j++) {
           if (isMaximization) {
               tableau[numRows - 1][j] = -objective[j];
           }
           else {
               tableau[numRows - 1][j] = objective[j];
           }
       }

       // Artificial variables get +M (for max) or -M (for min)
       for (int artIdx : artificialIndices) {
           if (isMaximization) {
               tableau[numRows - 1][artIdx] = M;
           }
           else {
               tableau[numRows - 1][artIdx] = -M;
           }
       }

       // Display objective with M
       string objType = isMaximization ? "Maximize" : "Minimize";
       cout << "  " << objType << " Z = ";
       for (int i = 0; i < numVariables; i++) {
           if (i > 0 && objective[i] >= 0) cout << "+ ";
           cout << objective[i] << "x" << (i + 1) << " ";
       }
       for (int idx : artificialIndices) {
           if (isMaximization) cout << "- M*" << varNames[idx] << " ";
           else cout << "+ M*" << varNames[idx] << " ";
       }
       cout << endl;

       // Eliminate artificial variables from objective row
       cout << "\nEliminating artificial variables from objective row:" << endl;
       for (size_t i = 0; i < basicVars.size(); i++) {
           int bv = basicVars[i];
           if (find(artificialIndices.begin(), artificialIndices.end(), bv) != artificialIndices.end()) {
               double coef = tableau[numRows - 1][bv];
               if (abs(coef) > EPSILON) {
                   cout << "  Subtracting " << coef << " * Row " << (i + 1) << " from objective row" << endl;
                   for (size_t j = 0; j < tableau[numRows - 1].size(); j++) {
                       tableau[numRows - 1][j] -= coef * tableau[i][j];
                   }
               }
           }
       }

       cout << "\n" << string(70, '-') << endl;
       cout << "INITIAL BIG M TABLEAU:" << endl;
       cout << string(70, '-') << endl;
       displayTableau();
   }

   void displayTableau() {
       int numCols = tableau[0].size();
       int colWidth = 10;

       // Header
       cout << "\n" << setw(12) << "";
       for (int j = 0; j < numCols - 1; j++) {
           if (j < (int)varNames.size()) {
               cout << setw(colWidth) << varNames[j];
           }
       }
       cout << setw(colWidth) << "RHS" << endl;

       // Separator
       cout << string(12 + colWidth * numCols, '-') << endl;

       // Constraint rows
       for (size_t i = 0; i < tableau.size() - 1; i++) {
           string basicVarName = (i < basicVars.size()) ? varNames[basicVars[i]] : "?";
           cout << setw(10) << basicVarName << " |";

           for (int j = 0; j < numCols; j++) {
               double val = tableau[i][j];
               if (abs(val) < EPSILON) val = 0;

               if (abs(val - round(val)) < EPSILON) {
                   cout << setw(colWidth) << (int)round(val);
               }
               else {
                   cout << setw(colWidth) << fixed << setprecision(3) << val;
               }
           }
           cout << endl;
       }

       // Separator
       cout << string(12 + colWidth * numCols, '-') << endl;

       // Objective row
       cout << setw(10) << "Zj-Cj" << " |";
       for (int j = 0; j < numCols; j++) {
           double val = tableau.back()[j];
           if (abs(val) < EPSILON) val = 0;

           // Check if value involves M
           if (abs(val) >= M * 0.5) {
               double mCoef = val / M;
               if (abs(mCoef - round(mCoef)) < 1e-6) {
                   cout << setw(colWidth - 1) << (int)round(mCoef) << "M";
               }
               else {
                   cout << setw(colWidth - 2) << fixed << setprecision(1) << mCoef << "M";
               }
           }
           else {
               if (abs(val - round(val)) < EPSILON) {
                   cout << setw(colWidth) << (int)round(val);
               }
               else {
                   cout << setw(colWidth) << fixed << setprecision(3) << val;
               }
           }
       }
       cout << endl;

       // Current basic solution
       cout << "\nCurrent Basic Solution:" << endl;
       double currentZ = 0;
       for (size_t i = 0; i < basicVars.size(); i++) {
           int bv = basicVars[i];
           double val = tableau[i].back();
           cout << "  " << varNames[bv] << " = " << fixed << setprecision(4) << val << endl;
           if (bv < numVariables) {
               currentZ += objective[bv] * val;
           }
           else if (find(artificialIndices.begin(), artificialIndices.end(), bv) != artificialIndices.end()) {
               if (isMaximization) currentZ -= M * val;
               else currentZ += M * val;
           }
       }

       double zVal = isMaximization ? -tableau.back().back() : tableau.back().back();
       cout << "\nCurrent Z value = " << fixed << setprecision(4) << zVal << endl;
   }

   int findPivotColumn() {
       int numCols = tableau[0].size();

       if (isMaximization) {
           double minVal = 0;
           int minIdx = -1;
           for (int j = 0; j < numCols - 1; j++) {
               if (tableau.back()[j] < minVal - EPSILON) {
                   minVal = tableau.back()[j];
                   minIdx = j;
               }
           }
           return minIdx;
       }
       else {
           double maxVal = 0;
           int maxIdx = -1;
           for (int j = 0; j < numCols - 1; j++) {
               if (tableau.back()[j] > maxVal + EPSILON) {
                   maxVal = tableau.back()[j];
                   maxIdx = j;
               }
           }
           return maxIdx;
       }
   }

   int findPivotRow(int pivotCol) {
       cout << "\n  Minimum Ratio Test:" << endl;

       double minRatio = numeric_limits<double>::max();
       int minRow = -1;

       for (size_t i = 0; i < tableau.size() - 1; i++) {
           if (tableau[i][pivotCol] > EPSILON) {
               double ratio = tableau[i].back() / tableau[i][pivotCol];
               cout << "    Row " << (i + 1) << " (" << varNames[basicVars[i]] << "): "
                   << fixed << setprecision(4) << tableau[i].back() << " / "
                   << tableau[i][pivotCol] << " = " << ratio << endl;

               if (ratio < minRatio) {
                   minRatio = ratio;
                   minRow = i;
               }
           }
           else {
               cout << "    Row " << (i + 1) << " (" << varNames[basicVars[i]] << "): "
                   << fixed << setprecision(4) << tableau[i].back() << " / "
                   << tableau[i][pivotCol] << " = Not applicable (non-positive)" << endl;
           }
       }

       if (minRow != -1) {
           cout << "\n  Minimum ratio = " << fixed << setprecision(4) << minRatio
               << " (Row " << (minRow + 1) << ")" << endl;
       }

       return minRow;
   }

   void performPivot(int pivotRow, int pivotCol) {
       double pivotElement = tableau[pivotRow][pivotCol];

       cout << "\n  Pivot Element: " << fixed << setprecision(4) << pivotElement << endl;
       cout << "\n  Pivot Operations:" << endl;

       // Make pivot element 1
       cout << "  1. R" << (pivotRow + 1) << " = R" << (pivotRow + 1) << " / "
           << fixed << setprecision(4) << pivotElement << endl;
       for (size_t j = 0; j < tableau[pivotRow].size(); j++) {
           tableau[pivotRow][j] /= pivotElement;
       }

       // Make other elements in pivot column 0
       for (size_t i = 0; i < tableau.size(); i++) {
           if ((int)i != pivotRow) {
               double factor = tableau[i][pivotCol];
               if (abs(factor) > EPSILON) {
                   if (i == tableau.size() - 1) {
                       cout << "  2. Zj-Cj = Zj-Cj - (" << fixed << setprecision(4)
                           << factor << ") * R" << (pivotRow + 1) << endl;
                   }
                   else {
                       cout << "  2. R" << (i + 1) << " = R" << (i + 1) << " - ("
                           << fixed << setprecision(4) << factor << ") * R" << (pivotRow + 1) << endl;
                   }
                   for (size_t j = 0; j < tableau[i].size(); j++) {
                       tableau[i][j] -= factor * tableau[pivotRow][j];
                   }
               }
           }
       }

       // Update basic variable
       string oldBasic = varNames[basicVars[pivotRow]];
       basicVars[pivotRow] = pivotCol;
       string newBasic = varNames[pivotCol];
       cout << "\n  " << oldBasic << " leaves the basis, " << newBasic << " enters the basis" << endl;
   }

   bool checkArtificialInBasis() {
       for (size_t i = 0; i < basicVars.size(); i++) {
           int bv = basicVars[i];
           if (find(artificialIndices.begin(), artificialIndices.end(), bv) != artificialIndices.end()) {
               if (tableau[i].back() > 1e-6) {
                   return true;
               }
           }
       }
       return false;
   }

   void solve() {
       cout << "\n" << string(70, '=') << endl;
       cout << "              STEP 2: APPLY BIG M SIMPLEX ITERATIONS" << endl;
       cout << string(70, '=') << endl;

       createInitialTableau();

       int maxIterations = 50;
       iteration = 0;

       while (iteration < maxIterations) {
           iteration++;

           cout << "\n" << string(70, '*') << endl;
           cout << "                        ITERATION " << iteration << endl;
           cout << string(70, '*') << endl;

           // Find pivot column
           int pivotCol = findPivotColumn();

           if (pivotCol == -1) {
               cout << "\n  All coefficients in objective row are optimal." << endl;
               cout << "  OPTIMAL SOLUTION REACHED!" << endl;
               break;
           }

           cout << "\n  Entering Variable: " << varNames[pivotCol] << " (Column " << (pivotCol + 1) << ")" << endl;
           if (isMaximization) {
               cout << "  Reason: Most negative coefficient = " << fixed << setprecision(4)
                   << tableau.back()[pivotCol] << endl;
           }
           else {
               cout << "  Reason: Most positive coefficient = " << fixed << setprecision(4)
                   << tableau.back()[pivotCol] << endl;
           }

           // Find pivot row
           int pivotRow = findPivotRow(pivotCol);

           if (pivotRow == -1) {
               cout << "\n  No valid pivot row found!" << endl;
               cout << "  PROBLEM IS UNBOUNDED!" << endl;
               return;
           }

           cout << "\n  Leaving Variable: " << varNames[basicVars[pivotRow]]
               << " (Row " << (pivotRow + 1) << ")" << endl;

               // Perform pivot
               performPivot(pivotRow, pivotCol);

               // Display updated tableau
               cout << "\n" << string(70, '-') << endl;
               cout << "TABLEAU AFTER ITERATION " << iteration << ":" << endl;
               cout << string(70, '-') << endl;
               displayTableau();
       }

       if (iteration >= maxIterations) {
           cout << "\n  Maximum iterations reached!" << endl;
           return;
       }

       // Check for infeasibility
       if (checkArtificialInBasis()) {
           cout << "\n" << string(70, '=') << endl;
           cout << "              PROBLEM IS INFEASIBLE" << endl;
           cout << string(70, '=') << endl;
           cout << "\nAn artificial variable remains in the basis with a positive value." << endl;
           cout << "This indicates that no feasible solution exists." << endl;
           return;
       }

       // Display final solution
       displaySolution();
   }

   void displaySolution() {
       cout << "\n" << string(70, '=') << endl;
       cout << "                    OPTIMAL SOLUTION" << endl;
       cout << string(70, '=') << endl;

       cout << "\nIterations: " << iteration << endl;
       cout << "Big M used: " << M << endl;

       // Get solution values
       vector<double> solution(numVariables, 0.0);

       for (size_t i = 0; i < basicVars.size(); i++) {
           int bv = basicVars[i];
           if (bv < numVariables) {
               solution[bv] = tableau[i].back();
           }
       }

       cout << "\nOptimal Decision Variables:" << endl;
       cout << string(40, '-') << endl;
       for (int i = 0; i < numVariables; i++) {
           double val = solution[i];
           if (abs(val - round(val)) < 1e-6) {
               cout << "  x" << (i + 1) << " = " << (int)round(val) << endl;
           }
           else {
               cout << "  x" << (i + 1) << " = " << fixed << setprecision(4) << val << endl;
           }
       }

       // Calculate optimal Z
       double optimalZ = 0;
       for (int i = 0; i < numVariables; i++) {
           optimalZ += objective[i] * solution[i];
       }

       cout << string(40, '-') << endl;
       string optType = isMaximization ? "Maximum" : "Minimum";
       cout << "\n" << optType << " Z = " << fixed << setprecision(4) << optimalZ << endl;

       // Verification
       cout << "\n" << string(40, '-') << endl;
       cout << "VERIFICATION:" << endl;
       cout << string(40, '-') << endl;

       // Objective function verification
       cout << "\nZ = ";
       for (int i = 0; i < numVariables; i++) {
           if (i > 0) cout << " + ";
           cout << objective[i] << " x " << fixed << setprecision(4) << solution[i];
       }
       cout << "\nZ = " << fixed << setprecision(4) << optimalZ << endl;

       // Constraint verification
       cout << "\nConstraint Check:" << endl;
       string typeSymbols[] = { "", "<=", ">=", "=" };
       bool allSatisfied = true;

       for (int i = 0; i < numConstraints; i++) {
           double lhs = 0;
           for (int j = 0; j < numVariables; j++) {
               lhs += constraints[i][j] * solution[j];
           }

           bool satisfied = false;
           if (constraintTypes[i] == 1) {  // <=
               satisfied = lhs <= rhs[i] + 1e-6;
           }
           else if (constraintTypes[i] == 2) {  // >=
               satisfied = lhs >= rhs[i] - 1e-6;
           }
           else {  // =
               satisfied = abs(lhs - rhs[i]) < 1e-6;
           }

           string status = satisfied ? "[OK]" : "[X]";
           cout << "  Constraint " << (i + 1) << ": " << fixed << setprecision(4) << lhs
               << " " << typeSymbols[constraintTypes[i]] << " " << rhs[i] << " " << status << endl;

           if (!satisfied) allSatisfied = false;
       }

       if (allSatisfied) {
           cout << "\n  All constraints are satisfied!" << endl;
       }
       else {
           cout << "\n  Warning: Some constraints are not satisfied!" << endl;
       }

       // Summary
       cout << "\n" << string(70, '=') << endl;
       cout << "                         SUMMARY" << endl;
       cout << string(70, '=') << endl;

       cout << "\n  Optimal Solution: (";
       for (int i = 0; i < numVariables; i++) {
           if (i > 0) cout << ", ";
           cout << "x" << (i + 1) << "=" << fixed << setprecision(2) << solution[i];
       }
       cout << ")" << endl;
       cout << "  " << optType << " Value: Z = " << fixed << setprecision(4) << optimalZ << endl;
       cout << "\n" << string(70, '=') << endl;
   }
};

int main() {
   cout << "\n" << string(70, '=') << endl;
   cout << "|                  BIG M METHOD SOLVER                               |" << endl;
   cout << "|              Linear Programming with Step-by-Step                  |" << endl;
   cout << "|            Handles <=, >=, and = Constraints                       |" << endl;
   cout << string(70, '=') << endl;

   char choice;
   do {
       BigMMethod solver;
       solver.getUserInput();

       cout << "\nPress Enter to start solving...";
       cin.ignore();
       cin.get();

       solver.solve();

       cout << "\n" << string(70, '-') << endl;
       cout << "\nSolve another problem? (y/n): ";
       cin >> choice;

   } while (choice == 'y' || choice == 'Y');

   cout << "\nThank you for using Big M Method Solver!" << endl;

   return 0;
}
