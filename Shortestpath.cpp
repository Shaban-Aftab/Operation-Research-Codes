///*
//Shortest/Longest Path Algorithm - Backward Dynamic Programming
//Solves Multi-Stage Graph Path Problem (Minimization OR Maximization)
//With Cycle Detection and Handling
//C++ Version - Pure C++ with no external libraries
//
//Features:
//1. Backward Dynamic Programming for DAGs
//2. Bellman-Ford algorithm for graphs with cycles
//3. Cycle detection using DFS
//4. Step-by-step visualization
//5. Both Shortest and Longest path
//*/



#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <map>
#include <set>
#include <limits>

using namespace std;

const double INF_VAL = 1e30;
const double NEG_INF = -1e30;

class PathSolver {
private:
   int numNodes;
   int numEdges;
   map<int, vector<pair<int, double>>> edges;
   map<int, vector<pair<int, double>>> reverseEdges;
   map<int, string> nodeNames;
   map<int, double> cost;
   map<int, int> nextNode;
   int source;
   int destination;
   set<int> processedNodes;
   bool isMinimization;
   bool hasCycle;
   vector<int> cyclePath;

public:
   PathSolver() : numNodes(0), numEdges(0), source(1), destination(0),
       isMinimization(true), hasCycle(false) {
   }

   void getUserInput() {
       cout << "\n" << string(60, '=') << endl;
       cout << "       SHORTEST/LONGEST PATH SOLVER" << endl;
       cout << "         (Stage Graph / Network)" << endl;
       cout << string(60, '=') << endl;

       // Problem type
       cout << "\nProblem Type:" << endl;
       cout << "  1. Shortest Path (Minimization)" << endl;
       cout << "  2. Longest Path (Maximization)" << endl;

       int choice;
       while (true) {
           cout << "\nEnter choice (1 or 2): ";
           cin >> choice;
           if (choice == 1 || choice == 2) {
               isMinimization = (choice == 1);
               break;
           }
           cout << "Please enter 1 or 2" << endl;
       }

       string problemType = isMinimization ? "SHORTEST PATH" : "LONGEST PATH";
       cout << "\n>>> Selected: " << problemType << endl;

       // Number of nodes
       while (true) {
           cout << "\nHow many nodes/stages? ";
           cin >> numNodes;
           if (numNodes > 1) break;
           cout << "Must have at least 2 nodes" << endl;
       }

       destination = numNodes;

       // Node names
       cout << "\n>>> Nodes: 1 (Source) to " << numNodes << " (Destination)" << endl;
       cout << "\nCustom node names? (y/n, default=n): ";
       char ch;
       cin >> ch;

       if (tolower(ch) == 'y') {
           cin.ignore();
           cout << "\nEnter name for each node:" << endl;
           for (int i = 1; i <= numNodes; i++) {
               cout << "  Node " << i << ": ";
               string name;
               getline(cin, name);
               nodeNames[i] = name.empty() ? to_string(i) : name;
           }
       }
       else {
           for (int i = 1; i <= numNodes; i++) {
               nodeNames[i] = to_string(i);
           }
       }

       // Initialize edges
       for (int i = 1; i <= numNodes; i++) {
           edges[i] = vector<pair<int, double>>();
           reverseEdges[i] = vector<pair<int, double>>();
       }

       // Matrix input
       cout << "\n" << string(60, '-') << endl;
       cout << "ENTER COST MATRIX" << endl;
       cout << string(60, '-') << endl;
       cout << "Enter the cost from each node to connected nodes." << endl;
       cout << "Use 'x', '-', or just enter 0 for NO connection." << endl;
       cout << "(For stage graphs, edges go from lower to higher nodes)" << endl;

       // Show matrix format
       cout << "\nMatrix Format:" << endl;
       cout << "From\\To  ";
       for (int j = 1; j <= numNodes; j++) {
           cout << setw(8) << j;
       }
       cout << endl;
       cout << string(8 + 8 * numNodes, '-') << endl;

       // Get matrix input
       for (int i = 1; i <= numNodes; i++) {
           cout << "\nNode " << i << " connections (to which nodes?):" << endl;

           for (int j = 1; j <= numNodes; j++) {
               if (i == j) continue;  // Skip self-loops
               if (j < i) continue;   // Skip backward edges for stage graphs

               while (true) {
                   cout << "  " << i << " -> " << j << ": ";
                   string input;
                   cin >> input;

                   // Convert to lowercase
                   string lower = input;
                   transform(lower.begin(), lower.end(), lower.begin(), ::tolower);

                   if (lower == "x" || lower == "-" || lower == "0" || lower == "n" || lower == "no") {
                       break;  // No connection
                   }

                   try {
                       double edgeCost = stod(input);
                       if (edgeCost < 0) {
                           cout << "    Cost cannot be negative" << endl;
                           continue;
                       }

                       edges[i].push_back({ j, edgeCost });
                       reverseEdges[j].push_back({ i, edgeCost });
                       numEdges++;
                       break;
                   }
                   catch (...) {
                       cout << "    Enter a number or 'x' for no connection" << endl;
                   }
               }
           }
       }

       displayCostMatrix();
       displayGraph();
   }

   void displayCostMatrix() {
       cout << "\n" << string(60, '=') << endl;
       cout << "              COST MATRIX" << endl;
       cout << string(60, '=') << endl;

       // Build cost matrix
       vector<vector<string>> matrix(numNodes, vector<string>(numNodes, "-"));

       for (int i = 1; i <= numNodes; i++) {
           for (const auto& edge : edges[i]) {
               int j = edge.first;
               double c = edge.second;

               if (c == floor(c)) {
                   matrix[i - 1][j - 1] = to_string((int)c);
               }
               else {
                   ostringstream oss;
                   oss << fixed << setprecision(1) << c;
                   matrix[i - 1][j - 1] = oss.str();
               }
           }
       }

       // Calculate column width
       int maxNameLen = 1;
       for (int i = 1; i <= numNodes; i++) {
           maxNameLen = max(maxNameLen, (int)nodeNames[i].size());
       }
       int colWidth = max(8, maxNameLen + 2);

       // Header
       cout << "\n" << setw(maxNameLen + 3) << "" << "|";
       for (int j = 1; j <= numNodes; j++) {
           cout << setw(colWidth) << nodeNames[j];
       }
       cout << endl;
       cout << string(maxNameLen + 3 + colWidth * numNodes + 1, '-') << endl;

       // Rows
       int edgeCount = 0;
       for (int i = 1; i <= numNodes; i++) {
           cout << setw(maxNameLen) << nodeNames[i] << " |";
           for (int j = 1; j <= numNodes; j++) {
               cout << setw(colWidth) << matrix[i - 1][j - 1];
               if (matrix[i - 1][j - 1] != "-") edgeCount++;
           }
           cout << endl;
       }

       cout << string(maxNameLen + 3 + colWidth * numNodes + 1, '-') << endl;
       cout << "\nTotal edges: " << edgeCount << endl;
       cout << "('-' = no connection)" << endl;
       cout << string(60, '=') << endl;
   }

   bool detectCycleDFS(int node, vector<int>& path, vector<int>& color) {
       const int WHITE = 0, GRAY = 1, BLACK = 2;
       color[node] = GRAY;
       path.push_back(node);

       for (const auto& edge : edges[node]) {
           int neighbor = edge.first;
           if (color[neighbor] == GRAY) {
               // Found cycle
               auto it = find(path.begin(), path.end(), neighbor);
               cyclePath = vector<int>(it, path.end());
               cyclePath.push_back(neighbor);
               return true;
           }
           else if (color[neighbor] == WHITE) {
               if (detectCycleDFS(neighbor, path, color)) {
                   return true;
               }
           }
       }

       path.pop_back();
       color[node] = BLACK;
       return false;
   }

   bool detectCycle() {
       vector<int> color(numNodes + 1, 0);  // WHITE
       vector<int> path;

       for (int node = 1; node <= numNodes; node++) {
           if (color[node] == 0) {
               if (detectCycleDFS(node, path, color)) {
                   hasCycle = true;
                   return true;
               }
           }
       }

       hasCycle = false;
       return false;
   }

   void displayGraph() {
       string problemType = isMinimization ? "SHORTEST PATH" : "LONGEST PATH";

       cout << "\n" << string(60, '=') << endl;
       cout << "            GRAPH STRUCTURE (" << problemType << ")" << endl;
       cout << string(60, '=') << endl;

       cout << "\nSource: Node " << nodeNames[1] << endl;
       cout << "Destination: Node " << nodeNames[destination] << endl;

       // Cycle detection
       cout << "\n" << string(50, '-') << endl;
       cout << "CYCLE DETECTION:" << endl;
       cout << string(50, '-') << endl;

       if (detectCycle()) {
           cout << "\n  [!] CYCLE DETECTED IN GRAPH!" << endl;
           cout << "  Cycle: ";
           for (size_t i = 0; i < cyclePath.size(); i++) {
               cout << nodeNames[cyclePath[i]];
               if (i < cyclePath.size() - 1) cout << " -> ";
           }
           cout << endl;
           cout << "\n  Note: Standard backward DP requires a DAG (no cycles)." << endl;
           cout << "  The solver will use Bellman-Ford algorithm instead." << endl;
       }
       else {
           cout << "\n  [OK] No cycle detected. Graph is a DAG." << endl;
           cout << "  Using Backward Dynamic Programming." << endl;
       }

       drawGraphState("Initial Graph", -1);
   }

   void drawGraphState(const string& title, int currentNode) {
       string problemType = isMinimization ? "MIN" : "MAX";

       cout << "\n" << string(60, '=') << endl;
       cout << "  GRAPH STATE: " << title << " [" << problemType << "]" << endl;
       if (hasCycle) {
           cout << "  [CYCLIC GRAPH - Using Bellman-Ford]" << endl;
       }
       cout << string(60, '=') << endl;

       // Node status
       cout << "\n  NODES:" << endl;
       cout << "  " << string(56, '-') << endl;

       for (int node = 1; node <= numNodes; node++) {
           double costVal = cost.count(node) ? cost[node] : (isMinimization ? INF_VAL : NEG_INF);
           int nextVal = nextNode.count(node) ? nextNode[node] : 0;

           string costStr;
           if (costVal >= INF_VAL - 1) {
               costStr = "+INF";
           }
           else if (costVal <= NEG_INF + 1) {
               costStr = "-INF";
           }
           else {
               ostringstream oss;
               oss << fixed << setprecision(1) << costVal;
               costStr = oss.str();
           }

           string nextStr = nextVal > 0 ? ("-> " + nodeNames[nextVal]) : "-> -";

           string marker;
           if (node == currentNode) {
               marker = ">>>";
           }
           else if (processedNodes.find(node) != processedNodes.end()) {
               marker = "[x]";
           }
           else if (node == destination) {
               marker = "[D]";
           }
           else if (node == 1) {
               marker = "[S]";
           }
           else {
               marker = "[ ]";
           }

           bool inCycle = find(cyclePath.begin(), cyclePath.end(), node) != cyclePath.end();
           string cycleMark = (hasCycle && inCycle) ? " (in cycle)" : "";

           cout << "  " << marker << " Node " << node << " (" << setw(5) << left << nodeNames[node]
               << ") | Cost: " << setw(8) << left << costStr << " | Next: " << nextStr << cycleMark << endl;
       }

       cout << "  " << string(56, '-') << endl;
       cout << "\n  Legend: [S]=Source [D]=Destination [x]=Processed >>>=Current" << endl;
   }

   void solveWithBellmanFord() {
       string problemType = isMinimization ? "SHORTEST" : "LONGEST";

       cout << "\n" << string(60, '=') << endl;
       cout << "      SOLVING: " << problemType << " PATH (Bellman-Ford)" << endl;
       cout << "       (Handles graphs with cycles)" << endl;
       cout << string(60, '=') << endl;

       // Initialize
       for (int i = 1; i <= numNodes; i++) {
           cost[i] = isMinimization ? INF_VAL : NEG_INF;
           nextNode[i] = 0;
       }

       cost[destination] = 0;

       cout << "\n>>> INITIALIZATION:" << endl;
       cout << "    f(" << nodeNames[destination] << ") = 0 (destination)" << endl;
       cout << "    All other f(i) = " << (isMinimization ? "+INF" : "-INF") << endl;

       // Bellman-Ford iterations
       cout << "\n>>> ITERATIONS:" << endl;

       bool hasNegativeCycle = false;

       for (int iter = 1; iter <= numNodes; iter++) {
           cout << "\n--- Iteration " << iter << " ---" << endl;

           bool updated = false;

           // Relax all edges in reverse (from j to i for edge i->j)
           for (int i = 1; i <= numNodes; i++) {
               for (const auto& edge : edges[i]) {
                   int j = edge.first;
                   double edgeCost = edge.second;

                   if (cost[j] >= INF_VAL - 1 || cost[j] <= NEG_INF + 1) continue;

                   double newCost = cost[j] + edgeCost;

                   bool shouldUpdate = false;
                   if (isMinimization && newCost < cost[i] - 1e-9) {
                       shouldUpdate = true;
                   }
                   else if (!isMinimization && newCost > cost[i] + 1e-9) {
                       shouldUpdate = true;
                   }

                   if (shouldUpdate) {
                       cout << "    f(" << nodeNames[i] << "): " << cost[i];
                       cost[i] = newCost;
                       nextNode[i] = j;
                       cout << " -> " << newCost << " via " << nodeNames[j] << endl;
                       updated = true;

                       if (iter == numNodes) {
                           hasNegativeCycle = true;
                       }
                   }
               }
           }

           if (!updated) {
               cout << "    No updates - converged!" << endl;
               break;
           }
       }

       if (hasNegativeCycle) {
           cout << "\n>>> WARNING: Negative cycle detected!" << endl;
       }

       drawGraphState("Final State", -1);
   }

   void solveBackwardDP() {
       string problemType = isMinimization ? "SHORTEST" : "LONGEST";

       cout << "\n" << string(60, '=') << endl;
       cout << "      SOLVING: " << problemType << " PATH (Backward DP)" << endl;
       cout << "           Processing nodes from destination to source" << endl;
       cout << string(60, '=') << endl;

       // Initialize
       for (int i = 1; i <= numNodes; i++) {
           cost[i] = isMinimization ? INF_VAL : NEG_INF;
           nextNode[i] = 0;
       }

       cost[destination] = 0;
       processedNodes.insert(destination);

       cout << "\n>>> INITIALIZATION:" << endl;
       cout << "    f(" << nodeNames[destination] << ") = 0 (destination node)" << endl;

       // Process nodes from destination-1 to 1
       cout << "\n>>> BACKWARD PASS:" << endl;

       for (int node = numNodes - 1; node >= 1; node--) {
           cout << "\n" << string(50, '-') << endl;
           cout << "Processing Node " << node << " (" << nodeNames[node] << ")" << endl;
           cout << string(50, '-') << endl;

           if (edges[node].empty()) {
               cout << "    No outgoing edges from this node" << endl;
               continue;
           }

           cout << "    Recurrence: f(" << nodeNames[node] << ") = "
               << (isMinimization ? "min" : "max") << "{ c(i,j) + f(j) }" << endl;
           cout << "\n    Evaluating options:" << endl;

           double bestCost = isMinimization ? INF_VAL : NEG_INF;
           int bestNext = 0;

           for (const auto& edge : edges[node]) {
               int j = edge.first;
               double edgeCost = edge.second;

               if (cost[j] >= INF_VAL - 1 || cost[j] <= NEG_INF + 1) {
                   cout << "      -> " << nodeNames[j] << ": " << edgeCost << " + INF = INF (skip)" << endl;
                   continue;
               }

               double totalCost = edgeCost + cost[j];
               cout << "      -> " << nodeNames[j] << ": " << edgeCost << " + " << cost[j] << " = " << totalCost;

               bool isBetter = false;
               if (isMinimization && totalCost < bestCost) isBetter = true;
               else if (!isMinimization && totalCost > bestCost) isBetter = true;

               if (isBetter) {
                   bestCost = totalCost;
                   bestNext = j;
                   cout << " <-- " << (isMinimization ? "MIN" : "MAX") << endl;
               }
               else {
                   cout << endl;
               }
           }

           if (bestNext > 0) {
               cost[node] = bestCost;
               nextNode[node] = bestNext;
               cout << "\n    RESULT: f(" << nodeNames[node] << ") = " << bestCost
                   << ", next = " << nodeNames[bestNext] << endl;
           }

           processedNodes.insert(node);
       }

       drawGraphState("Final State", -1);
   }

   void solve() {
       if (hasCycle) {
           solveWithBellmanFord();
       }
       else {
           solveBackwardDP();
       }
   }

   void displaySolution() {
       string problemType = isMinimization ? "SHORTEST" : "LONGEST";
       string costType = isMinimization ? "Minimum" : "Maximum";

       cout << "\n" << string(60, '=') << endl;
       cout << "                FINAL " << problemType << " PATH SOLUTION" << endl;
       cout << string(60, '=') << endl;

       // Check if path exists
       if (cost[source] >= INF_VAL - 1 || cost[source] <= NEG_INF + 1) {
           cout << "\n>>> No path exists from source to destination!" << endl;
           return;
       }

       // Reconstruct path
       cout << "\n>>> OPTIMAL PATH:" << endl;
       cout << string(50, '-') << endl;

       vector<int> path;
       int current = source;
       double totalCost = 0;

       while (current != 0 && current != destination) {
           path.push_back(current);
           int next = nextNode[current];

           if (next == 0) break;

           // Find edge cost
           double edgeCost = 0;
           for (const auto& edge : edges[current]) {
               if (edge.first == next) {
                   edgeCost = edge.second;
                   break;
               }
           }
           totalCost += edgeCost;
           current = next;
       }
       path.push_back(destination);

       // Display path
       cout << "\n    PATH: ";
       for (size_t i = 0; i < path.size(); i++) {
           cout << nodeNames[path[i]];
           if (i < path.size() - 1) cout << " -> ";
       }
       cout << endl;

       // Display path with costs
       cout << "\n    DETAILED PATH:" << endl;
       for (size_t i = 0; i < path.size() - 1; i++) {
           int from = path[i];
           int to = path[i + 1];

           double edgeCost = 0;
           for (const auto& edge : edges[from]) {
               if (edge.first == to) {
                   edgeCost = edge.second;
                   break;
               }
           }

           cout << "      " << nodeNames[from] << " --(" << edgeCost << ")--> " << nodeNames[to] << endl;
       }

       cout << "\n" << string(50, '=') << endl;
       cout << costType << " Path Cost = " << fixed << setprecision(1) << cost[source] << endl;
       cout << string(50, '=') << endl;

       // Display all paths
       displayAllPaths();
   }

   void findAllPaths(int current, int dest, vector<int>& path, double pathCost,
       vector<pair<vector<int>, double>>& allPaths) {
       path.push_back(current);

       if (current == dest) {
           allPaths.push_back({ path, pathCost });
           path.pop_back();
           return;
       }

       for (const auto& edge : edges[current]) {
           int next = edge.first;
           double edgeCost = edge.second;

           // Avoid cycles
           if (find(path.begin(), path.end(), next) == path.end()) {
               findAllPaths(next, dest, path, pathCost + edgeCost, allPaths);
           }
       }

       path.pop_back();
   }

   void displayAllPaths() {
       cout << "\n" << string(60, '=') << endl;
       cout << "              ALL POSSIBLE PATHS" << endl;
       cout << string(60, '=') << endl;

       vector<pair<vector<int>, double>> allPaths;
       vector<int> currentPath;
       findAllPaths(source, destination, currentPath, 0, allPaths);

       if (allPaths.empty()) {
           cout << "\n>>> No paths found from source to destination!" << endl;
           return;
       }

       // Sort by cost
       if (isMinimization) {
           sort(allPaths.begin(), allPaths.end(),
               [](const auto& a, const auto& b) { return a.second < b.second; });
       }
       else {
           sort(allPaths.begin(), allPaths.end(),
               [](const auto& a, const auto& b) { return a.second > b.second; });
       }

       double optimalCost = allPaths[0].second;

       cout << "\nTotal paths found: " << allPaths.size() << endl;
       cout << string(60, '-') << endl;

       for (size_t i = 0; i < allPaths.size(); i++) {
           const auto& p = allPaths[i];
           bool isOptimal = fabs(p.second - optimalCost) < 1e-9;

           cout << "\n" << (isOptimal ? "*** " : "    ") << "Path " << (i + 1) << ": ";
           for (size_t j = 0; j < p.first.size(); j++) {
               cout << nodeNames[p.first[j]];
               if (j < p.first.size() - 1) cout << " -> ";
           }
           cout << endl;
           cout << "    Cost: " << fixed << setprecision(1) << p.second;
           if (isOptimal) cout << " <-- OPTIMAL";
           cout << endl;
       }

       cout << "\n" << string(60, '-') << endl;
       cout << "*** = Optimal path(s)" << endl;
   }
};

int main() {
   cout << "\n" << string(60, '=') << endl;
   cout << "|         SHORTEST/LONGEST PATH SOLVER                    |" << endl;
   cout << "|      Dynamic Programming & Bellman-Ford                 |" << endl;
   cout << "|         With Cycle Detection                            |" << endl;
   cout << string(60, '=') << endl;

   char choice;
   do {
       PathSolver solver;
       solver.getUserInput();

       cout << "\nPress Enter to start solving...";
       cin.ignore();
       cin.get();

       solver.solve();
       solver.displaySolution();

       cout << "\n" << string(60, '-') << endl;
       cout << "\nSolve another problem? (y/n): ";
       cin >> choice;

   } while (tolower(choice) == 'y');
}