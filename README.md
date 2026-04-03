# MSCS532_Assignment6
Implementation of algorithms for selecting the \(k^{th}\) smallest element (order statistics) in an array. This includes the deterministic algorithm for selection in worst-case linear time and a randomized algorithm for selection in expected linear 

Repository Structure
.
├── selection_algorithms.py   # Part 1 — Median of Medians + Randomized Quickselect
├── data_structures.py        # Part 2 — DynamicArray, Matrix, Stack, Queue, LinkedList, RootedTree
├── Assignment6_Report.docx   # Full written report with analysis and empirical results
└── README.md

Requirements

Python 3.8 or later (no external libraries required)


Running the Code
Part 1 — Selection Algorithms
bashpython selection_algorithms.py
This will:

Run correctness tests verifying both algorithms match sorted()[k-1] across 6 test cases.
Run empirical benchmarks across 4 distributions × 5 sizes (1,000 – 100,000 elements), printing a formatted timing table.

Part 2 — Elementary Data Structures
bashpython data_structures.py
This will run unit tests on all implemented data structures (DynamicArray, Matrix, Stack, Queue, SinglyLinkedList, RootedTree) and print a pass/fail summary.

Summary of Findings
Part 1: Selection Algorithms
AlgorithmWorst-CaseExpectedConstant FactorMedian of Medians (MoM)O(n)O(n)LargeRandomized Quickselect (RQS)O(n²)O(n)Small

MoM guarantees O(n) worst-case by choosing a pivot that lies between the 30th and 70th percentile, bounding the larger partition to ≤ 7n/10 elements.
RQS is 2–4× faster in practice due to a much smaller constant factor; the O(n²) worst case is theoretically possible but occurs with vanishingly small probability.
Empirical benchmarks confirm linear scaling for both algorithms across random, sorted, reverse-sorted, and duplicate-heavy inputs.

Part 2: Data Structures
StructureKey OperationsTime ComplexityDynamicArrayappend, insert, delete, accessO(1) amortized / O(n) / O(1)Matrixaccess, add, transpose, multiplyO(1) / O(n²) / O(n²) / O(n³)Stackpush, pop, peekO(1) amortizedQueueenqueue, dequeue, peekO(1) amortizedSinglyLinkedListprepend/append, search, deleteO(1) / O(n) / O(n)RootedTree (LCRS)find, add_child, BFS/DFSO(n)

Arrays are preferred when random access is frequent; linked lists when insertions/deletions at arbitrary positions dominate.
The circular-buffer Queue avoids element shifting on every dequeue, achieving true O(1) amortized performance.
The LCRS tree representation stores a k-ary tree with only two pointers per node, independent of branching factor.