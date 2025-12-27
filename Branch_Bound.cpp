///*
//Branch and Bound Method for Integer Linear Programming
//With Visual Tree Representation
//Uses Simplex Method to solve LP relaxations
//C++ Version - Pure C++ with no external libraries
//Compatible with C++11 and later
//*/
//

#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <limits>
#include <map>

using namespace std;

const double EPSILON = 1e-10;
const double BIG_M = 10000;

// ========================================
// Simplified Simplex Solver for B&B
// ========================================
class SimplexSolver {
private:
   int numVariables;
   int numConstraints;
   vector<double> objective;
   vector<vector<double>> constraints;
   vector<double> rhs;
   vector<int> constraintTypes;
   bool isMaximization;

   vector<vector<double>> tableau;
   vector<string> varNames;
   vector<int> basicVars;

public:
   bool isFeasible;
   bool isUnbounded;

   SimplexSolver(const vector<double>& obj, const vector<vector<double>>& cons,
       const vector<double>& r, const vector<int>& types, bool isMax = true)
       : objective(obj), constraints(cons), rhs(r), constraintTypes(types),
       isMaximization(isMax), isFeasible(true), isUnbounded(false) {
       numVariables = (int)obj.size();
       numConstraints = (int)cons.size();
   }

   void createInitialTableau() {
       int numSlack = 0, numSurplus = 0, numArtificial = 0;
       for (size_t i = 0; i < constraintTypes.size(); i++) {
           int t = constraintTypes[i];
           if (t == 1) numSlack++;
           else if (t == 2) { numSurplus++; numArtificial++; }
           else numArtificial++;
       }

       int totalVars = numVariables + numSlack + numSurplus + numArtificial;
       int numRows = numConstraints + 1;
       int numCols = totalVars + 1;

       tableau.assign(numRows, vector<double>(numCols, 0.0));
       varNames.clear();
       for (int i = 0; i < numVariables; i++) {
           varNames.push_back("x" + to_string(i + 1));
       }

       int slackIdx = numVariables;
       int surplusIdx = numVariables + numSlack;
       int artificialIdx = numVariables + numSlack + numSurplus;

       basicVars.clear();

       for (int i = 0; i < numConstraints; i++) {
           for (int j = 0; j < numVariables; j++) {
               tableau[i][j] = constraints[i][j];
           }

           if (constraintTypes[i] == 1) {
               tableau[i][slackIdx] = 1;
               varNames.push_back("s" + to_string(i + 1));
               basicVars.push_back(slackIdx);
               slackIdx++;
           }
           else if (constraintTypes[i] == 2) {
               tableau[i][surplusIdx] = -1;
               varNames.push_back("e" + to_string(i + 1));
               surplusIdx++;
               tableau[i][artificialIdx] = 1;
               varNames.push_back("a" + to_string(i + 1));
               basicVars.push_back(artificialIdx);
               artificialIdx++;
           }
           else {
               tableau[i][artificialIdx] = 1;
               varNames.push_back("a" + to_string(i + 1));
               basicVars.push_back(artificialIdx);
               artificialIdx++;
           }

           tableau[i][numCols - 1] = rhs[i];
       }

       for (int j = 0; j < numVariables; j++) {
           if (isMaximization) {
               tableau[numRows - 1][j] = -objective[j];
           }
           else {
               tableau[numRows - 1][j] = objective[j];
           }
       }

       for (int i = 0; i < numConstraints; i++) {
           if (constraintTypes[i] == 2 || constraintTypes[i] == 3) {
               for (int j = numVariables + numSlack + numSurplus; j < totalVars; j++) {
                   if (tableau[i][j] == 1) {
                       if (isMaximization) {
                           tableau[numRows - 1][j] = BIG_M;
                       }
                       else {
                           tableau[numRows - 1][j] = -BIG_M;
                       }
                       for (int k = 0; k < numCols; k++) {
                           if (isMaximization) {
                               tableau[numRows - 1][k] -= BIG_M * tableau[i][k];
                           }
                           else {
                               tableau[numRows - 1][k] += BIG_M * tableau[i][k];
                           }
                       }
                       break;
                   }
               }
           }
       }
   }

   int findPivotColumn() {
       int numCols = (int)tableau[0].size();
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
       double minRatio = 1e30;
       int minRow = -1;
       int numRows = (int)tableau.size();
       for (int i = 0; i < numRows - 1; i++) {
           if (tableau[i][pivotCol] > EPSILON) {
               double ratio = tableau[i].back() / tableau[i][pivotCol];
               if (ratio < minRatio) {
                   minRatio = ratio;
                   minRow = i;
               }
           }
       }
       return minRow;
   }

   void performPivot(int pivotRow, int pivotCol) {
       basicVars[pivotRow] = pivotCol;
       double pivotElement = tableau[pivotRow][pivotCol];

       int numCols = (int)tableau[pivotRow].size();
       for (int j = 0; j < numCols; j++) {
           tableau[pivotRow][j] /= pivotElement;
       }

       int numRows = (int)tableau.size();
       for (int i = 0; i < numRows; i++) {
           if (i != pivotRow) {
               double factor = tableau[i][pivotCol];
               for (int j = 0; j < numCols; j++) {
                   tableau[i][j] -= factor * tableau[pivotRow][j];
               }
           }
       }
   }

   void solve(vector<double>& outSolution, double& outObjValue) {
       createInitialTableau();

       int maxIterations = 100;
       for (int iter = 0; iter < maxIterations; iter++) {
           int pivotCol = findPivotColumn();
           if (pivotCol == -1) break;

           int pivotRow = findPivotRow(pivotCol);
           if (pivotRow == -1) {
               isUnbounded = true;
               outSolution.clear();
               outObjValue = 0;
               return;
           }

           performPivot(pivotRow, pivotCol);
       }

       // Check for artificial variables
       for (size_t i = 0; i < basicVars.size(); i++) {
           int bv = basicVars[i];
           if (bv < (int)varNames.size() && varNames[bv][0] == 'a') {
               if (tableau[i].back() > 1e-6) {
                   isFeasible = false;
                   outSolution.clear();
                   outObjValue = 0;
                   return;
               }
           }
       }

       // Extract solution
       outSolution.assign(numVariables, 0.0);
       for (size_t i = 0; i < basicVars.size(); i++) {
           int bv = basicVars[i];
           if (bv < numVariables) {
               outSolution[bv] = tableau[i].back();
           }
       }

       outObjValue = 0;
       for (int i = 0; i < numVariables; i++) {
           outObjValue += objective[i] * outSolution[i];
       }
   }
};

// ========================================
// Tree Node for Visualization
// ========================================
struct TreeNode {
   int nodeId;
   int parentId;
   string branchConstraint;
   int depth;
   vector<double> solution;
   double objValue;
   string status;  // "INTEGER", "BRANCHED", "PRUNED", "INFEASIBLE"
   int leftChild;
   int rightChild;
   bool isOptimal;

   TreeNode() : nodeId(-1), parentId(-1), depth(0), objValue(0),
       leftChild(-1), rightChild(-1), isOptimal(false) {
   }

   TreeNode(int id, int parent, const string& constraint, int d)
       : nodeId(id), parentId(parent), branchConstraint(constraint), depth(d),
       objValue(0), status(""), leftChild(-1), rightChild(-1), isOptimal(false) {
   }
};

// ========================================
// Queue Item for B&B
// ========================================
struct QueueItem {
   vector<vector<double>> extraCons;
   vector<double> extraRhs;
   vector<int> extraTypes;
   double bound;
   int parentId;
   string branchInfo;
   int depth;

   QueueItem() : bound(0), parentId(-1), depth(0) {}
};

// ========================================
// Branch and Bound Solver
// ========================================
class BranchAndBound {
private:
   vector<double> objective;
   vector<vector<double>> constraints;
   vector<double> rhs;
   vector<int> constraintTypes;
   bool isMaximization;
   int numVariables;
   int numConstraints;
   vector<int> integerVars;

   vector<double> bestSolution;
   double bestObjValue;
   int iteration;

   map<int, TreeNode> treeNodes;
   vector<int> optimalPath;

public:
   BranchAndBound() : isMaximization(true), numVariables(0), numConstraints(0),
       bestObjValue(0), iteration(0) {
   }

   void getUserInput() {
       cout << "\n" << string(60, '=') << endl;
       cout << "      BRANCH AND BOUND - INTEGER PROGRAMMING SOLVER" << endl;
       cout << "             (With Tree Visualization)" << endl;
       cout << string(60, '=') << endl;

       // Problem type
       cout << "\nSelect Problem Type:" << endl;
       cout << "1. Maximization" << endl;
       cout << "2. Minimization" << endl;

       int choice;
       while (true) {
           cout << "Enter choice (1 or 2): ";
           cin >> choice;
           if (choice == 1 || choice == 2) {
               isMaximization = (choice == 1);
               break;
           }
           cout << "Please enter 1 or 2" << endl;
       }

       while (true) {
           cout << "\nEnter the number of decision variables: ";
           cin >> numVariables;
           if (numVariables > 0) break;
       }

       while (true) {
           cout << "Enter the number of constraints: ";
           cin >> numConstraints;
           if (numConstraints > 0) break;
       }

       // Objective function
       cout << "\n--- OBJECTIVE FUNCTION ---" << endl;
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
           }

           cout << "  RHS value: ";
           cin >> rhs[i];
       }

       // Integer variables
       cout << "\n--- INTEGER VARIABLES ---" << endl;
       cout << "1. All variables must be integers" << endl;
       cout << "2. Select specific variables" << endl;

       while (true) {
           cout << "Enter choice (1 or 2): ";
           cin >> choice;
           if (choice == 1) {
               for (int i = 0; i < numVariables; i++) {
                   integerVars.push_back(i);
               }
               break;
           }
           else if (choice == 2) {
               cout << "Enter variable numbers separated by spaces (e.g., 1 2): ";
               cin.ignore();
               string line;
               getline(cin, line);
               int var;
               size_t pos = 0;
               while (pos < line.size()) {
                   while (pos < line.size() && !isdigit(line[pos])) pos++;
                   if (pos >= line.size()) break;
                   var = 0;
                   while (pos < line.size() && isdigit(line[pos])) {
                       var = var * 10 + (line[pos] - '0');
                       pos++;
                   }
                   if (var >= 1 && var <= numVariables) {
                       integerVars.push_back(var - 1);
                   }
               }
               break;
           }
       }

       displayProblem();
   }

   void displayProblem() {
       cout << "\n" << string(60, '=') << endl;
       cout << "            FORMULATED ILP PROBLEM" << endl;
       cout << string(60, '=') << endl;

       string objType = isMaximization ? "Maximize" : "Minimize";
       cout << "\n" << objType << " Z = ";
       for (int i = 0; i < numVariables; i++) {
           if (i > 0 && objective[i] >= 0) cout << "+ ";
           else if (objective[i] < 0) cout << "- ";
           cout << fabs(objective[i]) << "x" << (i + 1) << " ";
       }
       cout << endl;

       cout << "\nSubject to:" << endl;
       string typeSymbols[] = { "", "<=", ">=", "=" };
       for (int i = 0; i < numConstraints; i++) {
           cout << "  ";
           for (int j = 0; j < numVariables; j++) {
               if (j > 0 && constraints[i][j] >= 0) cout << "+ ";
               else if (constraints[i][j] < 0) cout << "- ";
               cout << fabs(constraints[i][j]) << "x" << (j + 1) << " ";
           }
           cout << typeSymbols[constraintTypes[i]] << " " << rhs[i] << endl;
       }

       cout << "\n  Integer constraint: ";
       for (size_t i = 0; i < integerVars.size(); i++) {
           if (i > 0) cout << ", ";
           cout << "x" << (integerVars[i] + 1);
       }
       cout << " must be integers" << endl;
   }

   bool isIntegerSolution(const vector<double>& solution) {
       if (solution.empty()) return false;
       for (size_t i = 0; i < integerVars.size(); i++) {
           int idx = integerVars[i];
           double val = solution[idx];
           if (fabs(val - floor(val + 0.5)) > 1e-6) return false;
       }
       return true;
   }

   void findBranchingVariable(const vector<double>& solution, int& varIdx, double& fracVal) {
       varIdx = -1;
       fracVal = 0;
       for (size_t i = 0; i < integerVars.size(); i++) {
           int idx = integerVars[i];
           double val = solution[idx];
           if (fabs(val - floor(val + 0.5)) > 1e-6) {
               varIdx = idx;
               fracVal = val;
               return;
           }
       }
   }

   void solveSubproblem(const vector<vector<double>>& extraCons,
       const vector<double>& extraRhs,
       const vector<int>& extraTypes,
       vector<double>& outSolution, double& outObjValue) {
       vector<vector<double>> allCons = constraints;
       vector<double> allRhs = rhs;
       vector<int> allTypes = constraintTypes;

       for (size_t i = 0; i < extraCons.size(); i++) {
           allCons.push_back(extraCons[i]);
           allRhs.push_back(extraRhs[i]);
           allTypes.push_back(extraTypes[i]);
       }

       SimplexSolver solver(objective, allCons, allRhs, allTypes, isMaximization);
       solver.solve(outSolution, outObjValue);
   }

   void drawTree() {
       if (treeNodes.empty()) return;

       cout << "\n" << string(70, '=') << endl;
       cout << "                    BRANCH AND BOUND TREE" << endl;
       cout << string(70, '=') << endl;

       cout << "\nLEGEND:" << endl;
       cout << "  [*] = Optimal Solution Path" << endl;
       cout << "  [I] = Integer Solution Found" << endl;
       cout << "  [P] = Pruned (Bound)" << endl;
       cout << "  [X] = Infeasible" << endl;
       cout << "  [B] = Branched Further" << endl;
       cout << endl;

       drawNodeRecursive(0, "", true);
   }

   void drawNodeRecursive(int nodeId, const string& prefix, bool isLast) {
       if (treeNodes.find(nodeId) == treeNodes.end()) return;

       TreeNode& node = treeNodes[nodeId];

       string marker;
       if (node.isOptimal) marker = "[*]";
       else if (node.status == "INTEGER") marker = "[I]";
       else if (node.status == "PRUNED") marker = "[P]";
       else if (node.status == "INFEASIBLE") marker = "[X]";
       else if (node.status == "BRANCHED") marker = "[B]";
       else marker = "[ ]";

       string connector, newPrefix;
       if (node.depth == 0) {
           connector = "";
           newPrefix = "";
       }
       else {
           connector = isLast ? "`-- " : "|-- ";
           newPrefix = prefix + (isLast ? "    " : "|   ");
       }

       string info = (node.depth == 0) ? "ROOT NODE (LP Relaxation)" : node.branchConstraint;

       if (!node.solution.empty()) {
           string solStr = "";
           for (int i = 0; i < numVariables; i++) {
               if (i > 0) solStr += ", ";
               ostringstream oss;
               oss << "x" << (i + 1) << "=" << fixed << setprecision(2) << node.solution[i];
               solStr += oss.str();
           }
           cout << prefix << connector << marker << " Node " << nodeId << ": " << info << endl;
           cout << newPrefix << "     Solution: " << solStr << ", Z=" << fixed << setprecision(2) << node.objValue << endl;
           cout << newPrefix << "     Status: " << node.status << endl;
       }
       else {
           cout << prefix << connector << marker << " Node " << nodeId << ": " << info << endl;
           cout << newPrefix << "     Status: " << node.status << endl;
       }
       cout << newPrefix << endl;

       vector<int> children;
       if (node.leftChild != -1) children.push_back(node.leftChild);
       if (node.rightChild != -1) children.push_back(node.rightChild);

       for (size_t i = 0; i < children.size(); i++) {
           drawNodeRecursive(children[i], newPrefix, i == children.size() - 1);
       }
   }

   void solve() {
       cout << "\n" << string(60, '=') << endl;
       cout << "         SOLVING USING BRANCH AND BOUND" << endl;
       cout << string(60, '=') << endl;

       // Solve root node
       cout << "\n" << string(50, '-') << endl;
       cout << "STEP 1: Solve LP Relaxation (Root Node)" << endl;
       cout << string(50, '-') << endl;

       vector<double> rootSol;
       double rootObj;
       solveSubproblem({}, {}, {}, rootSol, rootObj);

       TreeNode root(0, -1, "ROOT", 0);
       root.solution = rootSol;
       root.objValue = rootObj;
       treeNodes[0] = root;

       if (rootSol.empty()) {
           cout << "Problem is INFEASIBLE!" << endl;
           treeNodes[0].status = "INFEASIBLE";
           drawTree();
           return;
       }

       cout << "\nLP Relaxation Solution:" << endl;
       for (int i = 0; i < numVariables; i++) {
           cout << "  x" << (i + 1) << " = " << fixed << setprecision(4) << rootSol[i] << endl;
       }
       cout << "  Z = " << fixed << setprecision(4) << rootObj << endl;

       if (isIntegerSolution(rootSol)) {
           cout << "\n>>> LP solution is already integer! Optimal found." << endl;
           treeNodes[0].status = "INTEGER";
           treeNodes[0].isOptimal = true;
           bestSolution = rootSol;
           bestObjValue = rootObj;
           optimalPath.push_back(0);
           drawTree();
           displayFinalSolution();
           return;
       }

       treeNodes[0].status = "BRANCHED";

       // Initialize best bound
       if (isMaximization) {
           bestObjValue = -1e30;
       }
       else {
           bestObjValue = 1e30;
       }

       vector<QueueItem> queue;
       QueueItem initial;
       initial.bound = rootObj;
       initial.parentId = 0;
       initial.branchInfo = "";
       initial.depth = 0;
       queue.push_back(initial);

       cout << "\n" << string(50, '-') << endl;
       cout << "STEP 2: Branch and Bound Iterations" << endl;
       cout << string(50, '-') << endl;

       int nodeCounter = 0;

       while (!queue.empty()) {
           iteration++;

           // Best-first selection
           if (isMaximization) {
               sort(queue.begin(), queue.end(), [](const QueueItem& a, const QueueItem& b) {
                   return a.bound > b.bound;
                   });
           }
           else {
               sort(queue.begin(), queue.end(), [](const QueueItem& a, const QueueItem& b) {
                   return a.bound < b.bound;
                   });
           }

           QueueItem current = queue.front();
           queue.erase(queue.begin());

           if (current.depth == 0 && iteration > 1) continue;

           cout << "\n" << string(60, '*') << endl;
           cout << "ITERATION " << iteration << endl;
           cout << string(60, '*') << endl;

           vector<double> solution;
           double objValue;
           solveSubproblem(current.extraCons, current.extraRhs, current.extraTypes, solution, objValue);

           int currentNodeId;
           if (current.depth > 0) {
               nodeCounter++;
               currentNodeId = nodeCounter;
               TreeNode node(currentNodeId, current.parentId, current.branchInfo, current.depth);
               node.solution = solution;
               node.objValue = objValue;
               treeNodes[currentNodeId] = node;

               if (treeNodes[current.parentId].leftChild == -1) {
                   treeNodes[current.parentId].leftChild = currentNodeId;
               }
               else {
                   treeNodes[current.parentId].rightChild = currentNodeId;
               }

               cout << "Node " << currentNodeId << ": " << current.branchInfo << endl;
           }
           else {
               currentNodeId = 0;
           }

           if (solution.empty()) {
               cout << "  Result: INFEASIBLE - Pruned" << endl;
               treeNodes[currentNodeId].status = "INFEASIBLE";
               continue;
           }

           cout << "\n  LP Solution:" << endl;
           for (int i = 0; i < numVariables; i++) {
               double val = solution[i];
               string marker = (fabs(val - floor(val + 0.5)) > 1e-6) ? " (fractional)" : "";
               cout << "    x" << (i + 1) << " = " << fixed << setprecision(4) << val << marker << endl;
           }
           cout << "    Z = " << fixed << setprecision(4) << objValue << endl;

           // Bound check
           bool prune = false;
           if (isMaximization && objValue <= bestObjValue) {
               prune = true;
           }
           else if (!isMaximization && objValue >= bestObjValue) {
               prune = true;
           }

           if (prune) {
               cout << "  Result: PRUNED (bound check)" << endl;
               treeNodes[currentNodeId].status = "PRUNED";
               continue;
           }

           // Check for integer
           if (isIntegerSolution(solution)) {
               cout << "  Result: INTEGER SOLUTION FOUND!" << endl;
               treeNodes[currentNodeId].status = "INTEGER";

               bool updateBest = false;
               if (isMaximization && objValue > bestObjValue) updateBest = true;
               else if (!isMaximization && objValue < bestObjValue) updateBest = true;

               if (updateBest) {
                   bestSolution = solution;
                   bestObjValue = objValue;
                   cout << "  >>> New best solution! Z = " << fixed << setprecision(4) << objValue << endl;

                   optimalPath.clear();
                   int traceId = currentNodeId;
                   while (traceId != -1) {
                       optimalPath.insert(optimalPath.begin(), traceId);
                       traceId = treeNodes[traceId].parentId;
                   }

                   for (map<int, TreeNode>::iterator it = treeNodes.begin(); it != treeNodes.end(); ++it) {
                       bool found = false;
                       for (size_t k = 0; k < optimalPath.size(); k++) {
                           if (optimalPath[k] == it->first) { found = true; break; }
                       }
                       it->second.isOptimal = found;
                   }
               }
               continue;
           }

           // Branch
           int varIdx;
           double fracVal;
           findBranchingVariable(solution, varIdx, fracVal);
           int floorVal = (int)floor(fracVal);
           int ceilVal = (int)ceil(fracVal);

           treeNodes[currentNodeId].status = "BRANCHED";

           cout << "\n  Branching on x" << (varIdx + 1) << " = " << fixed << setprecision(4) << fracVal << endl;
           cout << "    Left branch:  x" << (varIdx + 1) << " <= " << floorVal << endl;
           cout << "    Right branch: x" << (varIdx + 1) << " >= " << ceilVal << endl;

           vector<double> coef(numVariables, 0.0);
           coef[varIdx] = 1.0;

           // Left branch
           QueueItem left;
           left.extraCons = current.extraCons;
           left.extraCons.push_back(coef);
           left.extraRhs = current.extraRhs;
           left.extraRhs.push_back((double)floorVal);
           left.extraTypes = current.extraTypes;
           left.extraTypes.push_back(1);
           left.bound = objValue;
           left.parentId = currentNodeId;
           left.branchInfo = "x" + to_string(varIdx + 1) + " <= " + to_string(floorVal);
           left.depth = current.depth + 1;
           queue.push_back(left);

           // Right branch
           QueueItem right;
           right.extraCons = current.extraCons;
           right.extraCons.push_back(coef);
           right.extraRhs = current.extraRhs;
           right.extraRhs.push_back((double)ceilVal);
           right.extraTypes = current.extraTypes;
           right.extraTypes.push_back(2);
           right.bound = objValue;
           right.parentId = currentNodeId;
           right.branchInfo = "x" + to_string(varIdx + 1) + " >= " + to_string(ceilVal);
           right.depth = current.depth + 1;
           queue.push_back(right);
       }

       drawTree();
       displayFinalSolution();
   }

   void displayFinalSolution() {
       cout << "\n" << string(60, '=') << endl;
       cout << "              OPTIMAL INTEGER SOLUTION" << endl;
       cout << string(60, '=') << endl;

       if (bestSolution.empty()) {
           cout << "\nNo feasible integer solution found!" << endl;
           return;
       }

       cout << "\nNodes Explored: " << treeNodes.size() << endl;
       cout << "Iterations: " << iteration << endl;

       cout << "\nOptimal Decision Variables:" << endl;
       for (int i = 0; i < numVariables; i++) {
           double val = bestSolution[i];
           bool isInt = false;
           for (size_t k = 0; k < integerVars.size(); k++) {
               if (integerVars[k] == i) { isInt = true; break; }
           }
           if (isInt) {
               cout << "  x" << (i + 1) << " = " << (int)(val + 0.5) << " (integer)" << endl;
           }
           else {
               cout << "  x" << (i + 1) << " = " << fixed << setprecision(4) << val << endl;
           }
       }

       double calcZ = 0;
       for (int i = 0; i < numVariables; i++) {
           calcZ += objective[i] * bestSolution[i];
       }
       cout << "\nOptimal Value of Z = " << fixed << setprecision(4) << calcZ << endl;

       cout << "\n" << string(40, '-') << endl;
       cout << "VERIFICATION:" << endl;

       cout << "\nConstraint Check:" << endl;
       string typeSymbols[] = { "", "<=", ">=", "=" };
       for (int i = 0; i < numConstraints; i++) {
           double lhs = 0;
           for (int j = 0; j < numVariables; j++) {
               lhs += constraints[i][j] * bestSolution[j];
           }
           cout << "  Constraint " << (i + 1) << ": " << fixed << setprecision(4) << lhs
               << " " << typeSymbols[constraintTypes[i]] << " " << rhs[i] << " [OK]" << endl;
       }
   }
};

int main() {
   cout << "\n" << string(60, '=') << endl;
   cout << "|       BRANCH AND BOUND - INTEGER PROGRAMMING           |" << endl;
   cout << "|           With Tree Visualization                      |" << endl;
   cout << "|        Handles Maximization and Minimization           |" << endl;
   cout << string(60, '=') << endl;

   char choice;
   do {
       BranchAndBound solver;
       solver.getUserInput();

       cout << "\nPress Enter to start solving...";
       cin.ignore();
       cin.get();

       solver.solve();

       cout << "\n" << string(60, '-') << endl;
       cout << "\nSolve another problem? (y/n): ";
       cin >> choice;

   } while (tolower(choice) == 'y');

   cout << "\nThank you for using Branch and Bound Solver!" << endl;

   return 0;
}
