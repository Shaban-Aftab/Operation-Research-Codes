///*
//0/1 Knapsack Problem Solver
//Uses Dynamic Programming with Step-by-Step Visualization
//C++ Version - Pure C++ with no external libraries
//
//Features:
//- Exclude specific items (force NOT to pick)
//- Require specific items (force to pick if feasible)
//- Step-by-step DP table visualization
//- Backtracking to find selected items
//*/


#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <cmath>
#include <algorithm>
#include <sstream>

using namespace std;

class KnapsackSolver {
private:
   int numItems;
   int capacity;
   vector<int> weights;
   vector<double> values;
   vector<string> itemNames;
   vector<vector<double>> dpTable;
   vector<int> selectedItems;
   vector<int> excludedItems;  // Items user doesn't want to pick
   vector<int> requiredItems;  // Items user must pick

public:
   KnapsackSolver() : numItems(0), capacity(0) {}

   void getUserInput() {
       cout << "\n" << string(60, '=') << endl;
       cout << "         0/1 KNAPSACK PROBLEM SOLVER" << endl;
       cout << "           (Dynamic Programming)" << endl;
       cout << string(60, '=') << endl;

       // Number of items
       while (true) {
           cout << "\nEnter the number of items: ";
           cin >> numItems;
           if (numItems > 0) break;
           cout << "Number of items must be positive" << endl;
       }

       // Knapsack capacity
       while (true) {
           cout << "Enter the knapsack capacity (integer): ";
           cin >> capacity;
           if (capacity > 0) break;
           cout << "Capacity must be positive" << endl;
       }

       // Get item details
       cout << "\n--- ITEM DETAILS ---" << endl;
       cout << "Enter weight and value for each item" << endl;

       cin.ignore();  // Clear newline

       for (int i = 0; i < numItems; i++) {
           cout << "\nItem " << (i + 1) << ":" << endl;

           // Item name
           cout << "  Item name (or press Enter for 'Item " << (i + 1) << "'): ";
           string name;
           getline(cin, name);
           if (name.empty()) {
               name = "Item " + to_string(i + 1);
           }
           itemNames.push_back(name);

           // Weight
           int weight;
           while (true) {
               cout << "  Weight of " << name << ": ";
               cin >> weight;
               if (weight > 0) {
                   weights.push_back(weight);
                   break;
               }
               cout << "  Weight must be positive" << endl;
           }

           // Value
           double value;
           while (true) {
               cout << "  Value of " << name << ": ";
               cin >> value;
               if (value >= 0) {
                   values.push_back(value);
                   break;
               }
               cout << "  Value must be non-negative" << endl;
           }
           cin.ignore();  // Clear newline
       }

       // Item constraints
       cout << "\n" << string(60, '-') << endl;
       cout << "         ITEM SELECTION CONSTRAINTS" << endl;
       cout << string(60, '-') << endl;

       cout << "\nDo you want to add any constraints on item selection?" << endl;
       cout << "  1. EXCLUDE items (items you DON'T want to pick)" << endl;
       cout << "  2. REQUIRE items (items you MUST pick if feasible)" << endl;
       cout << "  3. No constraints (optimal selection)" << endl;

       // Excluded items
       char excludeChoice;
       cout << "\nExclude any items? (y/n): ";
       cin >> excludeChoice;

       if (tolower(excludeChoice) == 'y') {
           cout << "\nAvailable items:" << endl;
           for (int i = 0; i < numItems; i++) {
               cout << "  " << (i + 1) << ". " << itemNames[i]
                   << " (w=" << weights[i] << ", v=" << values[i] << ")" << endl;
           }

           cout << "Enter item numbers to EXCLUDE (comma-separated, e.g., 1,3): ";
           cin.ignore();
           string excludeInput;
           getline(cin, excludeInput);

           if (!excludeInput.empty()) {
               stringstream ss(excludeInput);
               string token;
               while (getline(ss, token, ',')) {
                   try {
                       int num = stoi(token);
                       if (num >= 1 && num <= numItems) {
                           excludedItems.push_back(num - 1);
                           cout << "  X " << itemNames[num - 1] << " will be EXCLUDED" << endl;
                       }
                   }
                   catch (...) {}
               }
           }
       }

       // Required items
       char requireChoice;
       cout << "\nRequire any items to be picked? (y/n): ";
       cin >> requireChoice;

       if (tolower(requireChoice) == 'y') {
           cout << "\nAvailable items (not excluded):" << endl;
           for (int i = 0; i < numItems; i++) {
               if (find(excludedItems.begin(), excludedItems.end(), i) == excludedItems.end()) {
                   cout << "  " << (i + 1) << ". " << itemNames[i]
                       << " (w=" << weights[i] << ", v=" << values[i] << ")" << endl;
               }
           }

           cout << "Enter item numbers to REQUIRE (comma-separated, e.g., 2,4): ";
           cin.ignore();
           string requireInput;
           getline(cin, requireInput);

           if (!requireInput.empty()) {
               stringstream ss(requireInput);
               string token;
               while (getline(ss, token, ',')) {
                   try {
                       int num = stoi(token);
                       if (num >= 1 && num <= numItems &&
                           find(excludedItems.begin(), excludedItems.end(), num - 1) == excludedItems.end()) {
                           requiredItems.push_back(num - 1);
                           cout << "  + " << itemNames[num - 1] << " will be REQUIRED" << endl;
                       }
                   }
                   catch (...) {}
               }
           }
       }

       displayProblem();
   }

   void displayProblem() {
       cout << "\n" << string(70, '=') << endl;
       cout << "                 KNAPSACK PROBLEM" << endl;
       cout << string(70, '=') << endl;

       cout << "\nKnapsack Capacity: " << capacity << endl;
       cout << "Number of Items: " << numItems << endl;

       // Show constraints if any
       if (!excludedItems.empty() || !requiredItems.empty()) {
           cout << "\n" << string(50, '-') << endl;
           cout << "USER-DEFINED CONSTRAINTS:" << endl;
           if (!excludedItems.empty()) {
               cout << "  X EXCLUDED: ";
               for (size_t i = 0; i < excludedItems.size(); i++) {
                   if (i > 0) cout << ", ";
                   cout << itemNames[excludedItems[i]];
               }
               cout << endl;
           }
           if (!requiredItems.empty()) {
               cout << "  + REQUIRED: ";
               for (size_t i = 0; i < requiredItems.size(); i++) {
                   if (i > 0) cout << ", ";
                   cout << itemNames[requiredItems[i]];
               }
               cout << endl;
           }
       }

       cout << "\n" << string(60, '-') << endl;
       cout << left << setw(15) << "Item" << setw(10) << "Weight"
           << setw(10) << "Value" << setw(10) << "Ratio" << setw(12) << "Constraint" << endl;
       cout << string(60, '-') << endl;

       int totalWeight = 0;
       double totalValue = 0;

       for (int i = 0; i < numItems; i++) {
           double ratio = values[i] / weights[i];

           string constraint;
           if (find(excludedItems.begin(), excludedItems.end(), i) != excludedItems.end()) {
               constraint = "EXCLUDED X";
           }
           else if (find(requiredItems.begin(), requiredItems.end(), i) != requiredItems.end()) {
               constraint = "REQUIRED +";
           }
           else {
               constraint = "Optional";
           }

           cout << left << setw(15) << itemNames[i].substr(0, 14)
               << setw(10) << weights[i]
               << setw(10) << fixed << setprecision(2) << values[i]
                   << setw(10) << ratio
                       << setw(12) << constraint << endl;

                   totalWeight += weights[i];
                   totalValue += values[i];
       }

       cout << string(60, '-') << endl;
       cout << left << setw(15) << "TOTAL" << setw(10) << totalWeight
           << setw(10) << fixed << setprecision(2) << totalValue << endl;
   }

   void displayDPTable(int highlightRow = -1, int highlightCol = -1) {
       int n = numItems;
       int W = capacity;

       int colWidth = 6;

       // Limit display for large tables
       vector<int> displayCols;
       if (W > 15) {
           for (int w = 0; w <= min(7, W); w++) displayCols.push_back(w);
           displayCols.push_back(-1);  // marker for "..."
           for (int w = max(8, W - 3); w <= W; w++) displayCols.push_back(w);
       }
       else {
           for (int w = 0; w <= W; w++) displayCols.push_back(w);
       }

       // Header
       cout << setw(12) << "" << "| ";
       for (int w : displayCols) {
           if (w == -1) {
               cout << setw(colWidth) << "...";
           }
           else {
               string header = "w=" + to_string(w);
               cout << setw(colWidth) << header;
           }
       }
       cout << endl;
       cout << string(12 + displayCols.size() * colWidth + 2, '-') << endl;

       // Rows
       for (int i = 0; i <= n; i++) {
           string rowLabel = (i == 0) ? "No items" : itemNames[i - 1].substr(0, 10);
           cout << left << setw(11) << rowLabel << " | ";

           for (int w : displayCols) {
               if (w == -1) {
                   cout << setw(colWidth) << "...";
               }
               else {
                   double val = dpTable[i][w];
                   if (i == highlightRow && w == highlightCol) {
                       cout << "[" << setw(colWidth - 2) << (int)val << "]";
                   }
                   else {
                       cout << setw(colWidth) << (int)val;
                   }
               }
           }

           if (i == highlightRow) {
               cout << " <-- Current";
           }
           cout << endl;
       }
       cout << string(12 + displayCols.size() * colWidth + 2, '-') << endl;
   }

   void solve() {
       cout << "\n" << string(70, '=') << endl;
       cout << "      SOLVING 0/1 KNAPSACK USING DYNAMIC PROGRAMMING" << endl;
       cout << string(70, '=') << endl;

       int n = numItems;
       int W = capacity;

       // Handle required items
       int requiredWeight = 0;
       double requiredValue = 0;
       for (int idx : requiredItems) {
           requiredWeight += weights[idx];
           requiredValue += values[idx];
       }

       // Display constraints
       cout << "\n" << string(70, '-') << endl;
       cout << "CONSTRAINT SUMMARY" << endl;
       cout << string(70, '-') << endl;
       cout << "\n  Knapsack Capacity: W = " << W << endl;
       cout << "  Number of Items: n = " << n << endl;
       cout << "\n  Constraint: Each item can be taken at most ONCE (0/1 constraint)" << endl;
       cout << "  Objective: MAXIMIZE total value without exceeding capacity" << endl;

       if (!excludedItems.empty()) {
           cout << "\n  X USER EXCLUDED ITEMS: ";
           for (size_t i = 0; i < excludedItems.size(); i++) {
               if (i > 0) cout << ", ";
               cout << itemNames[excludedItems[i]];
           }
           cout << endl;
           cout << "    These items will NOT be considered, even if feasible." << endl;
       }

       if (!requiredItems.empty()) {
           cout << "\n  + USER REQUIRED ITEMS: ";
           for (size_t i = 0; i < requiredItems.size(); i++) {
               if (i > 0) cout << ", ";
               cout << itemNames[requiredItems[i]];
           }
           cout << endl;
           cout << "    These items MUST be included if they fit." << endl;
           cout << "    Combined weight: " << requiredWeight << endl;
           cout << "    Combined value: " << requiredValue << endl;

           if (requiredWeight > W) {
               cout << "    ERROR: Required items exceed capacity! Cannot satisfy constraint." << endl;
               return;
           }
       }

       // Initialize DP table
       dpTable.assign(n + 1, vector<double>(W + 1, 0));

       cout << "\n" << string(70, '=') << endl;
       cout << "STEP 1: INITIALIZE DP TABLE" << endl;
       cout << string(70, '=') << endl;
       cout << "\n  Table dimensions: (n+1) x (W+1) = " << (n + 1) << " rows x " << (W + 1) << " columns" << endl;
       cout << "  dp[i][w] = Maximum value using items 1 to i with capacity w" << endl;
       cout << "\n  Base Case: dp[0][w] = 0 for all w (no items = no value)" << endl;
       cout << "  Base Case: dp[i][0] = 0 for all i (zero capacity = no items)" << endl;

       cout << "\n  Initial Table (all zeros):" << endl;
       displayDPTable();

       cout << "\n" << string(70, '=') << endl;
       cout << "STEP 2: FILL DP TABLE - APPLYING CONSTRAINTS ITEM BY ITEM" << endl;
       cout << string(70, '=') << endl;

       cout << "\n  Recurrence Relation:" << endl;
       cout << "  If weight[i] > w: dp[i][w] = dp[i-1][w] (CANNOT include)" << endl;
       cout << "  Else: dp[i][w] = max(dp[i-1][w], value[i] + dp[i-1][w-weight[i]])" << endl;

       cout << "\nPress Enter to see step-by-step filling of DP table...";
       cin.ignore();
       cin.get();

       // Fill DP table
       for (int i = 1; i <= n; i++) {
           int itemIdx = i - 1;

           cout << "\n" << string(70, '=') << endl;
           cout << "  PROCESSING ITEM " << i << ": " << itemNames[itemIdx] << endl;
           cout << "  Weight = " << weights[itemIdx] << ", Value = " << values[itemIdx] << endl;

           bool isExcluded = find(excludedItems.begin(), excludedItems.end(), itemIdx) != excludedItems.end();
           bool isRequired = find(requiredItems.begin(), requiredItems.end(), itemIdx) != requiredItems.end();

           if (isExcluded) {
               cout << "  *** USER CONSTRAINT: EXCLUDED - This item will be SKIPPED ***" << endl;
           }
           else if (isRequired) {
               cout << "  *** USER CONSTRAINT: REQUIRED - This item MUST be included ***" << endl;
           }
           cout << string(70, '=') << endl;

           // Handle excluded items
           if (isExcluded) {
               cout << "\n  X " << itemNames[itemIdx] << " is EXCLUDED by user constraint!" << endl;
               cout << "    Copying previous row: dp[" << i << "][w] = dp[" << (i - 1) << "][w] for all w" << endl;
               for (int w = 0; w <= W; w++) {
                   dpTable[i][w] = dpTable[i - 1][w];
               }

               cout << "\n  " << string(60, '-') << endl;
               cout << "  TABLE AFTER SKIPPING " << itemNames[itemIdx] << " (EXCLUDED):" << endl;
               cout << "  " << string(60, '-') << endl;
               displayDPTable(i, W);

               if (i < n) {
                   cout << "\n  Press Enter to process next item (" << itemNames[i] << ")...";
                   cin.get();
               }
               continue;
           }

           // Fill for each capacity
           for (int w = 0; w <= W; w++) {
               if (weights[itemIdx] > w) {
                   dpTable[i][w] = dpTable[i - 1][w];
               }
               else {
                   double excludeValue = dpTable[i - 1][w];
                   int remainingCapacity = w - weights[itemIdx];
                   double includeValue = values[itemIdx] + dpTable[i - 1][remainingCapacity];

                   if (isRequired) {
                       dpTable[i][w] = includeValue;
                   }
                   else {
                       dpTable[i][w] = max(excludeValue, includeValue);
                   }
               }
           }

           // Show decision for capacity W
           if (weights[itemIdx] <= W) {
               cout << "\n  At capacity w = " << W << ":" << endl;
               double excludeValue = dpTable[i - 1][W];
               int remainingCapacity = W - weights[itemIdx];
               double includeValue = values[itemIdx] + dpTable[i - 1][remainingCapacity];

               if (isRequired) {
                   cout << "    MUST INCLUDE (Required): " << includeValue << endl;
               }
               else {
                   cout << "    Exclude: " << excludeValue << " vs Include: " << includeValue << endl;
                   cout << "    Decision: " << (dpTable[i][W] == includeValue ? "INCLUDE" : "EXCLUDE") << endl;
               }
           }

           cout << "\n  " << string(60, '-') << endl;
           cout << "  TABLE AFTER PROCESSING " << itemNames[itemIdx] << ":" << endl;
           cout << "  " << string(60, '-') << endl;
           displayDPTable(i, W);

           if (i < n) {
               cout << "\n  Press Enter to process next item (" << itemNames[i] << ")...";
               cin.get();
           }
       }

       // Show final table
       cout << "\n" << string(70, '=') << endl;
       cout << "COMPLETE DP TABLE (FINAL)" << endl;
       cout << string(70, '=') << endl;
       displayDPTable(n, W);

       cout << "\n  >>> MAXIMUM VALUE = dp[" << n << "][" << W << "] = " << dpTable[n][W] << endl;

       // Backtrack
       cout << "\n" << string(70, '=') << endl;
       cout << "STEP 3: BACKTRACKING TO FIND SELECTED ITEMS" << endl;
       cout << string(70, '=') << endl;

       backtrack();

       // Display solution
       displaySolution();
   }

   void backtrack() {
       int n = numItems;
       int W = capacity;

       int w = W;
       selectedItems.clear();

       cout << "\nStarting from dp[" << n << "][" << W << "] = " << dpTable[n][W] << endl;
       cout << "\nBacktracking path:" << endl;

       for (int i = n; i > 0; i--) {
           if (dpTable[i][w] != dpTable[i - 1][w]) {
               selectedItems.push_back(i - 1);
               cout << "\n  dp[" << i << "][" << w << "] = " << dpTable[i][w]
                   << " != dp[" << (i - 1) << "][" << w << "] = " << dpTable[i - 1][w] << endl;
                   cout << "  => " << itemNames[i - 1] << " was INCLUDED" << endl;
                   cout << "     Remaining capacity: " << w << " - " << weights[i - 1]
                       << " = " << (w - weights[i - 1]) << endl;
                   w -= weights[i - 1];
           }
           else {
               cout << "\n  dp[" << i << "][" << w << "] = " << dpTable[i][w]
                   << " == dp[" << (i - 1) << "][" << w << "] = " << dpTable[i - 1][w] << endl;
                   cout << "  => " << itemNames[i - 1] << " was NOT included" << endl;
           }
       }

       reverse(selectedItems.begin(), selectedItems.end());
   }

   void displaySolution() {
       cout << "\n" << string(60, '=') << endl;
       cout << "                OPTIMAL SOLUTION" << endl;
       cout << string(60, '=') << endl;

       int totalWeight = 0;
       double totalValue = 0;

       cout << "\nSelected Items:" << endl;
       cout << string(50, '-') << endl;
       cout << left << setw(20) << "Item" << setw(10) << "Weight" << setw(10) << "Value" << endl;
       cout << string(50, '-') << endl;

       for (int idx : selectedItems) {
           cout << left << setw(20) << itemNames[idx]
               << setw(10) << weights[idx]
                   << setw(10) << fixed << setprecision(2) << values[idx] << endl;
                   totalWeight += weights[idx];
                   totalValue += values[idx];
       }

       cout << string(50, '-') << endl;
       cout << left << setw(20) << "TOTAL" << setw(10) << totalWeight
           << setw(10) << fixed << setprecision(2) << totalValue << endl;
       cout << string(50, '-') << endl;

       cout << "\nKnapsack Capacity Used: " << totalWeight << " / " << capacity << endl;
       cout << "Remaining Capacity: " << (capacity - totalWeight) << endl;
       cout << "\nMaximum Value Achieved: " << fixed << setprecision(2) << totalValue << endl;

       // Visual representation
       cout << "\n" << string(50, '-') << endl;
       cout << "KNAPSACK VISUALIZATION" << endl;
       cout << string(50, '-') << endl;

       int filled = (int)((double)totalWeight / capacity * 30);
       int empty = 30 - filled;

       cout << "\n  [" << string(filled, '#') << string(empty, '.') << "]" << endl;
       cout << "\n  Capacity: " << totalWeight << "/" << capacity
           << " (" << fixed << setprecision(1) << ((double)totalWeight / capacity * 100) << "% full)" << endl;

       // Items in knapsack
       cout << "\n  Items in knapsack:" << endl;
       for (int idx : selectedItems) {
           int barLen = (int)((double)weights[idx] / capacity * 30);
           cout << "  |" << left << setw(30) << string(barLen, '=') << "| "
               << itemNames[idx] << " (w=" << weights[idx] << ", v=" << values[idx] << ")" << endl;
       }

       // Items not selected
       vector<int> notSelected;
       for (int i = 0; i < numItems; i++) {
           if (find(selectedItems.begin(), selectedItems.end(), i) == selectedItems.end()) {
               notSelected.push_back(i);
           }
       }

       if (!notSelected.empty()) {
           cout << "\n  Items NOT selected:" << endl;
           for (int idx : notSelected) {
               cout << "  x " << itemNames[idx] << " (w=" << weights[idx] << ", v=" << values[idx] << ")" << endl;
           }
       }
   }
};

int main() {
   cout << "\n" << string(60, '=') << endl;
   cout << "|            0/1 KNAPSACK PROBLEM SOLVER                 |" << endl;
   cout << "|              Dynamic Programming with                  |" << endl;
   cout << "|             Step-by-Step Visualization                 |" << endl;
   cout << string(60, '=') << endl;

   char choice;
   do {
       KnapsackSolver solver;
       solver.getUserInput();

       cout << "\nPress Enter to start solving...";
       cin.ignore();
       cin.get();

       solver.solve();

       cout << "\n" << string(60, '-') << endl;
       cout << "\nSolve another problem? (y/n): ";
       cin >> choice;

   } while (tolower(choice) == 'y');

   cout << "\nThank you for using Knapsack Solver!" << endl;

   return 0;
}
