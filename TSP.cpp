///*
//Travelling Salesman Problem (TSP) Solver
//Branch and Bound with Tree Visualization
//C++ Version - Pure C++ with no external libraries
//
//Features:
//1. Branch and Bound algorithm
//2. Lower bound calculation
//3. Tree visualization
//4. Matrix or edge-by-edge input
//5. User-specified starting city
//*/
//

#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <map>
#include <set>
#include <queue>
#include <limits>

using namespace std;

const double INF_VAL = 1e30;

// TSP Node for Branch and Bound Tree
struct TSPNode {
   int nodeId;
   vector<int> path;
   double cost;
   double bound;
   int level;
   int parentId;
   vector<int> children;
   string status;
   bool isOptimal;

   TSPNode() : nodeId(-1), cost(0), bound(0), level(0), parentId(-1), isOptimal(false) {}

   TSPNode(int id, const vector<int>& p, double c, double b, int lvl, int parent = -1)
       : nodeId(id), path(p), cost(c), bound(b), level(lvl), parentId(parent), isOptimal(false) {
   }
};

class TSPSolver {
private:
   int numCities;
   map<int, string> cityNames;
   map<string, int> cityIndices;
   vector<vector<double>> distanceMatrix;
   map<int, vector<pair<int, double>>> edges;
   int startCity;
   vector<int> bestTour;
   double bestCost;
   map<int, TSPNode> nodes;
   int nodeCounter;
   int rootId;
   vector<int> optimalPathIds;

public:
   TSPSolver() : numCities(0), startCity(0), bestCost(INF_VAL), nodeCounter(0), rootId(0) {}

   void getUserInput() {
       cout << "\n" << string(60, '=') << endl;
       cout << "       TRAVELLING SALESMAN PROBLEM (TSP)" << endl;
       cout << "           Branch and Bound Solver" << endl;
       cout << string(60, '=') << endl;

       // Number of cities
       while (true) {
           cout << "\nEnter the number of cities: ";
           cin >> numCities;
           if (numCities >= 2) break;
           cout << "Number of cities must be at least 2" << endl;
       }

       // City names
       cout << "\n--- CITY NAMES ---" << endl;
       cout << "Use default city names? (y/n): ";
       char choice;
       cin >> choice;

       if (tolower(choice) == 'y') {
           for (int i = 0; i < numCities; i++) {
               string name = "City" + to_string(i + 1);
               cityNames[i] = name;
               cityIndices[name] = i;
           }
       }
       else {
           cin.ignore();
           for (int i = 0; i < numCities; i++) {
               cout << "  Enter name for City " << (i + 1) << ": ";
               string name;
               getline(cin, name);
               if (name.empty()) name = "City" + to_string(i + 1);
               cityNames[i] = name;
               cityIndices[name] = i;
           }
       }

       // Display cities
       cout << "\nCities registered:" << endl;
       for (int i = 0; i < numCities; i++) {
           cout << "  " << (i + 1) << ": " << cityNames[i] << endl;
       }

       // Starting city
       cout << "\n--- STARTING CITY ---" << endl;
       while (true) {
           cout << "Enter starting city (number 1-" << numCities << "): ";
           int startNum;
           cin >> startNum;
           if (startNum >= 1 && startNum <= numCities) {
               startCity = startNum - 1;
               cout << "  Starting from: " << cityNames[startCity] << endl;
               break;
           }
           cout << "  Please enter a number between 1 and " << numCities << endl;
       }

       // Initialize distance matrix
       distanceMatrix.assign(numCities, vector<double>(numCities, INF_VAL));
       for (int i = 0; i < numCities; i++) {
           edges[i] = vector<pair<int, double>>();
       }

       // Choose input method
       cout << "\n--- INPUT METHOD ---" << endl;
       cout << "1. Enter distance matrix directly" << endl;
       cout << "2. Enter edges one by one" << endl;

       int method;
       while (true) {
           cout << "\nChoose input method (1 or 2): ";
           cin >> method;
           if (method == 1 || method == 2) break;
           cout << "Please enter 1 or 2" << endl;
       }

       if (method == 1) {
           inputMatrix();
       }
       else {
           inputEdges();
       }

       displayProblem();
   }

   void inputMatrix() {
       cout << "\n--- DISTANCE MATRIX INPUT ---" << endl;
       cout << "Enter the distance from each city to every other city." << endl;
       cout << "Use 'x', '-', or 0 for no connection/infinity." << endl;
       cout << "Diagonal entries will be set to infinity automatically.\n" << endl;

       for (int i = 0; i < numCities; i++) {
           cout << "\nRow " << (i + 1) << " (" << cityNames[i] << "):" << endl;
           for (int j = 0; j < numCities; j++) {
               if (i == j) {
                   distanceMatrix[i][j] = INF_VAL;
                   cout << "  " << cityNames[i] << " -> " << cityNames[j] << ": inf (same city)" << endl;
               }
               else {
                   while (true) {
                       cout << "  " << cityNames[i] << " -> " << cityNames[j] << ": ";
                       string input;
                       cin >> input;

                       string lower = input;
                       transform(lower.begin(), lower.end(), lower.begin(), ::tolower);

                       if (lower == "x" || lower == "-" || lower == "inf" || lower == "m") {
                           distanceMatrix[i][j] = INF_VAL;
                           break;
                       }

                       try {
                           double dist = stod(input);
                           if (dist < 0) {
                               cout << "    Distance cannot be negative." << endl;
                               continue;
                           }
                           if (dist == 0) {
                               distanceMatrix[i][j] = INF_VAL;
                           }
                           else {
                               distanceMatrix[i][j] = dist;
                               edges[i].push_back({ j, dist });
                           }
                           break;
                       }
                       catch (...) {
                           cout << "    Invalid input." << endl;
                       }
                   }
               }
           }
       }

       cout << "\nDistance matrix entered successfully!" << endl;
   }

   void inputEdges() {
       cout << "\n--- CONNECTIONS (EDGES) ---" << endl;
       cout << "Enter which cities are connected and their distances." << endl;
       cout << "Type 0 for 'from city' when finished.\n" << endl;

       int edgeCount = 0;
       while (true) {
           cout << "Edge " << (edgeCount + 1) << ":" << endl;

           cout << "  From city (1-" << numCities << ", or 0 to finish): ";
           int fromNum;
           cin >> fromNum;

           if (fromNum == 0) break;
           if (fromNum < 1 || fromNum > numCities) {
               cout << "    Invalid city number." << endl;
               continue;
           }
           int fromIdx = fromNum - 1;

           cout << "  To city (1-" << numCities << "): ";
           int toNum;
           cin >> toNum;

           if (toNum < 1 || toNum > numCities) {
               cout << "    Invalid city number." << endl;
               continue;
           }
           int toIdx = toNum - 1;

           if (fromIdx == toIdx) {
               cout << "    Cannot connect a city to itself." << endl;
               continue;
           }

           cout << "  Distance: ";
           double dist;
           cin >> dist;

           if (dist <= 0) {
               cout << "    Distance must be positive." << endl;
               continue;
           }

           // Add edge (both directions)
           distanceMatrix[fromIdx][toIdx] = dist;
           distanceMatrix[toIdx][fromIdx] = dist;
           edges[fromIdx].push_back({ toIdx, dist });
           edges[toIdx].push_back({ fromIdx, dist });

           cout << "    Added: " << cityNames[fromIdx] << " <--" << dist << "--> " << cityNames[toIdx] << "\n" << endl;
           edgeCount++;
       }

       if (edgeCount == 0) {
           cout << "\nWarning: No edges entered!" << endl;
       }
   }

   void displayProblem() {
       cout << "\n" << string(60, '=') << endl;
       cout << "              TSP PROBLEM" << endl;
       cout << string(60, '=') << endl;

       cout << "\nNumber of Cities: " << numCities << endl;
       cout << "Starting City: " << cityNames[startCity] << endl;

       // City connections
       cout << "\n" << string(50, '-') << endl;
       cout << "CITY CONNECTIONS:" << endl;
       cout << string(50, '-') << endl;

       for (int i = 0; i < numCities; i++) {
           cout << "  " << cityNames[i] << " --> ";
           if (edges[i].empty()) {
               cout << "(no connections)";
           }
           else {
               for (size_t k = 0; k < edges[i].size(); k++) {
                   if (k > 0) cout << ", ";
                   cout << cityNames[edges[i][k].first] << "(" << edges[i][k].second << ")";
               }
           }
           cout << endl;
       }

       // Distance matrix
       cout << "\n" << string(50, '-') << endl;
       cout << "DISTANCE MATRIX:" << endl;
       cout << string(50, '-') << endl;

       cout << setw(8) << "";
       for (int j = 0; j < numCities; j++) {
           cout << setw(8) << cityNames[j].substr(0, 5);
       }
       cout << endl;
       cout << setw(8) << "" << string(8 * numCities, '-') << endl;

       for (int i = 0; i < numCities; i++) {
           cout << setw(6) << cityNames[i].substr(0, 5) << " |";
           for (int j = 0; j < numCities; j++) {
               if (distanceMatrix[i][j] >= INF_VAL - 1) {
                   cout << setw(8) << "--";
               }
               else {
                   cout << setw(8) << fixed << setprecision(0) << distanceMatrix[i][j];
               }
           }
           if (i == startCity) {
               cout << "  <-- START";
           }
           cout << endl;
       }
       cout << string(50, '-') << endl;
   }

   double calculateLowerBound(const vector<int>& path, double currentCost) {
       int n = numCities;
       set<int> visited(path.begin(), path.end());
       double bound = currentCost;

       // Minimum outgoing edge from last city
       if (!path.empty()) {
           int lastCity = path.back();
           if ((int)visited.size() < n) {
               double minEdge = INF_VAL;
               for (int j = 0; j < n; j++) {
                   bool canVisit = (visited.find(j) == visited.end()) ||
                       ((int)visited.size() == n - 1 && j == startCity);
                   if (canVisit && distanceMatrix[lastCity][j] < minEdge) {
                       minEdge = distanceMatrix[lastCity][j];
                   }
               }
               if (minEdge < INF_VAL - 1) {
                   bound += minEdge;
               }
           }
       }

       // Minimum edges for unvisited cities
       for (int i = 0; i < n; i++) {
           if (visited.find(i) == visited.end()) {
               double minOut = INF_VAL;
               for (int j = 0; j < n; j++) {
                   bool canGo = (i != j) && (visited.find(j) == visited.end() || j == startCity);
                   if (canGo && distanceMatrix[i][j] < minOut) {
                       minOut = distanceMatrix[i][j];
                   }
               }
               if (minOut < INF_VAL - 1) {
                   bound += minOut;
               }
           }
       }

       return bound;
   }

   void solve() {
       cout << "\n" << string(60, '=') << endl;
       cout << "      SOLVING TSP - BRANCH AND BOUND" << endl;
       cout << string(60, '=') << endl;

       int n = numCities;

       if (n <= 1) {
           cout << "\nNeed at least 2 cities!" << endl;
           return;
       }

       // Check connectivity
       for (int i = 0; i < n; i++) {
           bool hasEdge = false;
           for (int j = 0; j < n; j++) {
               if (i != j && distanceMatrix[i][j] < INF_VAL - 1) {
                   hasEdge = true;
                   break;
               }
           }
           if (!hasEdge) {
               cout << "\nWarning: " << cityNames[i] << " has no connections!" << endl;
           }
       }

       // Initialize root node
       vector<int> rootPath = { startCity };
       double rootCost = 0;
       double rootBound = calculateLowerBound(rootPath, rootCost);

       rootId = nodeCounter;
       TSPNode root(nodeCounter++, rootPath, rootCost, rootBound, 0, -1);
       root.status = "ROOT";
       nodes[root.nodeId] = root;

       cout << "\n>>> ROOT NODE:" << endl;
       cout << "    Path: [" << cityNames[startCity] << "]" << endl;
       cout << "    Cost: " << rootCost << endl;
       cout << "    Lower Bound: " << rootBound << endl;

       // Priority queue (min-heap by bound)
       auto cmp = [](const pair<double, int>& a, const pair<double, int>& b) {
           return a.first > b.first;
           };
       priority_queue<pair<double, int>, vector<pair<double, int>>, decltype(cmp)> pq(cmp);
       pq.push({ rootBound, rootId });

       int iteration = 0;

       cout << "\n>>> BRANCHING:" << endl;

       while (!pq.empty()) {
           iteration++;

           pair<double, int> top = pq.top();
           pq.pop();
           double currentBound = top.first;
           int currentId = top.second;

           TSPNode& current = nodes[currentId];

           // Skip if bound is worse than best
           if (currentBound >= bestCost) {
               current.status = "PRUNED";
               continue;
           }

           cout << "\n" << string(50, '-') << endl;
           cout << "Iteration " << iteration << ": Expanding Node " << currentId << endl;
           cout << "  Path: [";
           for (size_t i = 0; i < current.path.size(); i++) {
               if (i > 0) cout << " -> ";
               cout << cityNames[current.path[i]];
           }
           cout << "]" << endl;
           cout << "  Cost: " << current.cost << ", Bound: " << current.bound << endl;

           // Check if complete tour
           if ((int)current.path.size() == n) {
               // Add return to start
               double returnCost = distanceMatrix[current.path.back()][startCity];
               if (returnCost < INF_VAL - 1) {
                   double totalCost = current.cost + returnCost;

                   cout << "  Complete tour found!" << endl;
                   cout << "  Return to start: " << returnCost << endl;
                   cout << "  Total cost: " << totalCost << endl;

                   if (totalCost < bestCost) {
                       bestCost = totalCost;
                       bestTour = current.path;
                       bestTour.push_back(startCity);
                       current.status = "SOLUTION";
                       cout << "  >>> NEW BEST SOLUTION!" << endl;

                       // Update optimal path
                       optimalPathIds.clear();
                       int traceId = currentId;
                       while (traceId != -1) {
                           optimalPathIds.insert(optimalPathIds.begin(), traceId);
                           traceId = nodes[traceId].parentId;
                       }
                   }
                   else {
                       current.status = "PRUNED";
                   }
               }
               else {
                   current.status = "NO_RETURN";
                   cout << "  No return path to start!" << endl;
               }
               continue;
           }

           // Branch to unvisited cities
           set<int> visited(current.path.begin(), current.path.end());
           int lastCity = current.path.back();

           current.status = "BRANCHED";

           for (int nextCity = 0; nextCity < n; nextCity++) {
               if (visited.find(nextCity) != visited.end()) continue;
               if (distanceMatrix[lastCity][nextCity] >= INF_VAL - 1) continue;

               vector<int> newPath = current.path;
               newPath.push_back(nextCity);
               double newCost = current.cost + distanceMatrix[lastCity][nextCity];
               double newBound = calculateLowerBound(newPath, newCost);

               cout << "  -> Branch to " << cityNames[nextCity]
                   << ": cost=" << newCost << ", bound=" << newBound;

                   if (newBound >= bestCost) {
                       cout << " [PRUNED]" << endl;

                       int childId = nodeCounter++;
                       TSPNode child(childId, newPath, newCost, newBound, current.level + 1, currentId);
                       child.status = "PRUNED";
                       nodes[childId] = child;
                       current.children.push_back(childId);
                   }
                   else {
                       cout << " [EXPLORE]" << endl;

                       int childId = nodeCounter++;
                       TSPNode child(childId, newPath, newCost, newBound, current.level + 1, currentId);
                       child.status = "ACTIVE";
                       nodes[childId] = child;
                       current.children.push_back(childId);

                       pq.push({ newBound, childId });
                   }
           }
       }

       // Mark optimal path nodes
       for (int id : optimalPathIds) {
           nodes[id].isOptimal = true;
       }

       drawTree();
       displaySolution();
   }

   void drawTree() {
       cout << "\n" << string(70, '=') << endl;
       cout << "                    BRANCH AND BOUND TREE" << endl;
       cout << string(70, '=') << endl;

       cout << "\nLEGEND:" << endl;
       cout << "  [*] = Optimal Path" << endl;
       cout << "  [S] = Solution Found" << endl;
       cout << "  [P] = Pruned" << endl;
       cout << "  [B] = Branched" << endl;
       cout << endl;

       drawNode(rootId, "", true);
   }

   void drawNode(int nodeId, const string& prefix, bool isLast) {
       if (nodes.find(nodeId) == nodes.end()) return;

       TSPNode& node = nodes[nodeId];

       string marker;
       if (node.isOptimal) marker = "[*]";
       else if (node.status == "SOLUTION") marker = "[S]";
       else if (node.status == "PRUNED") marker = "[P]";
       else if (node.status == "BRANCHED") marker = "[B]";
       else marker = "[ ]";

       string connector, newPrefix;
       if (node.level == 0) {
           connector = "";
           newPrefix = "";
       }
       else {
           connector = isLast ? "`-- " : "|-- ";
           newPrefix = prefix + (isLast ? "    " : "|   ");
       }

       // Build path string
       ostringstream pathStr;
       for (size_t i = 0; i < node.path.size(); i++) {
           if (i > 0) pathStr << "->";
           pathStr << cityNames[node.path[i]].substr(0, 3);
       }

       cout << prefix << connector << marker << " Node " << nodeId
           << ": [" << pathStr.str() << "] cost=" << node.cost
           << " bound=" << fixed << setprecision(1) << node.bound << endl;

       for (size_t i = 0; i < node.children.size(); i++) {
           drawNode(node.children[i], newPrefix, i == node.children.size() - 1);
       }
   }

   void displaySolution() {
       cout << "\n" << string(60, '=') << endl;
       cout << "              OPTIMAL TSP SOLUTION" << endl;
       cout << string(60, '=') << endl;

       if (bestTour.empty()) {
           cout << "\nNo valid tour found!" << endl;
           cout << "Check if all cities are connected." << endl;
           return;
       }

       cout << "\nOPTIMAL TOUR:" << endl;
       cout << string(50, '-') << endl;

       cout << "\n  ";
       for (size_t i = 0; i < bestTour.size(); i++) {
           cout << cityNames[bestTour[i]];
           if (i < bestTour.size() - 1) cout << " -> ";
       }
       cout << endl;

       cout << "\nDETAILED PATH:" << endl;
       double totalCost = 0;
       for (size_t i = 0; i < bestTour.size() - 1; i++) {
           int from = bestTour[i];
           int to = bestTour[i + 1];
           double dist = distanceMatrix[from][to];
           totalCost += dist;
           cout << "  " << cityNames[from] << " --(" << dist << ")--> " << cityNames[to] << endl;
       }

       cout << "\n" << string(50, '=') << endl;
       cout << "MINIMUM TOUR COST = " << fixed << setprecision(0) << bestCost << endl;
       cout << string(50, '=') << endl;

       cout << "\nNodes explored: " << nodes.size() << endl;
   }
};

int main() {
   cout << "\n" << string(60, '=') << endl;
   cout << "|         TRAVELLING SALESMAN PROBLEM (TSP)              |" << endl;
   cout << "|            Branch and Bound Solver                     |" << endl;
   cout << "|           With Tree Visualization                      |" << endl;
   cout << string(60, '=') << endl;

   char choice;
   do {
       TSPSolver solver;
       solver.getUserInput();

       cout << "\nPress Enter to start solving...";
       cin.ignore();
       cin.get();

       solver.solve();

       cout << "\n" << string(60, '-') << endl;
       cout << "\nSolve another problem? (y/n): ";
       cin >> choice;

   } while (tolower(choice) == 'y');

   cout << "\nThank you for using TSP Solver!" << endl;

   return 0;
}
