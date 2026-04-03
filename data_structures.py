"""
Assignment 6 - Part 2: Elementary Data Structures
Author: Reza Shrestha

Implements from scratch:
  - DynamicArray   — resizable array with O(1) amortized append
  - Matrix         — 2-D array with basic operations
  - Stack          — LIFO structure backed by DynamicArray
  - Queue          — FIFO structure backed by a circular array
  - SinglyLinkedList
  - RootedTree     — general rooted tree via left-child / right-sibling representation
"""


# ─────────────────────────────────────────────────────────────────────────────
# Dynamic Array
# ─────────────────────────────────────────────────────────────────────────────

class DynamicArray:
    """
    A resizable array similar to Python's built-in list.

    Internal storage doubles when capacity is reached and halves when the
    load factor drops to 1/4 (to avoid thrashing).

    Time Complexities
    -----------------
    append      : O(1) amortized
    insert      : O(n)
    delete      : O(n)
    access      : O(1)
    length      : O(1)
    """

    def __init__(self):
        self._capacity = 4
        self._size = 0
        self._data = [None] * self._capacity

    # ── helpers ────────────────────────────────────────────────────────────

    def _resize(self, new_cap):
        """Copy data into a new backing store of size new_cap."""
        new_data = [None] * new_cap
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_cap

    def _check_index(self, i):
        if not (0 <= i < self._size):
            raise IndexError(f"Index {i} out of range for size {self._size}.")

    # ── public interface ────────────────────────────────────────────────────

    def __len__(self):
        return self._size

    def __getitem__(self, i):
        """O(1) random access."""
        self._check_index(i)
        return self._data[i]

    def __setitem__(self, i, value):
        """O(1) random update."""
        self._check_index(i)
        self._data[i] = value

    def __repr__(self):
        items = [repr(self._data[i]) for i in range(self._size)]
        return f"DynamicArray([{', '.join(items)}])"

    def append(self, value):
        """Append to end; doubles capacity when full. O(1) amortized."""
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._size] = value
        self._size += 1

    def insert(self, i, value):
        """Insert value before position i. O(n)."""
        if not (0 <= i <= self._size):
            raise IndexError(f"Insert index {i} out of range.")
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        # Shift right
        for j in range(self._size, i, -1):
            self._data[j] = self._data[j - 1]
        self._data[i] = value
        self._size += 1

    def delete(self, i):
        """Delete element at index i and return it. O(n)."""
        self._check_index(i)
        value = self._data[i]
        # Shift left
        for j in range(i, self._size - 1):
            self._data[j] = self._data[j + 1]
        self._data[self._size - 1] = None
        self._size -= 1
        # Shrink if load is low (halve but keep at least 4)
        if self._size > 0 and self._size == self._capacity // 4:
            self._resize(max(4, self._capacity // 2))
        return value

    def to_list(self):
        """Return a plain Python list copy."""
        return [self._data[i] for i in range(self._size)]


# ─────────────────────────────────────────────────────────────────────────────
# Matrix
# ─────────────────────────────────────────────────────────────────────────────

class Matrix:
    """
    2-D matrix backed by a flat list.

    Time Complexities
    -----------------
    access / set cell   : O(1)
    add / subtract      : O(rows * cols)
    transpose           : O(rows * cols)
    multiply            : O(rows * inner * cols)
    """

    def __init__(self, rows, cols, fill=0):
        if rows <= 0 or cols <= 0:
            raise ValueError("Dimensions must be positive.")
        self._rows = rows
        self._cols = cols
        self._data = [fill] * (rows * cols)

    # ── helpers ────────────────────────────────────────────────────────────

    @classmethod
    def from_list(cls, nested):
        """Create a Matrix from a list-of-lists."""
        rows = len(nested)
        cols = len(nested[0]) if rows else 0
        m = cls(rows, cols)
        for r in range(rows):
            for c in range(cols):
                m[r, c] = nested[r][c]
        return m

    def _idx(self, r, c):
        if not (0 <= r < self._rows and 0 <= c < self._cols):
            raise IndexError(f"({r},{c}) out of range for {self._rows}x{self._cols} matrix.")
        return r * self._cols + c

    # ── dunder ─────────────────────────────────────────────────────────────

    def __getitem__(self, key):
        r, c = key
        return self._data[self._idx(r, c)]

    def __setitem__(self, key, value):
        r, c = key
        self._data[self._idx(r, c)] = value

    def __repr__(self):
        rows = []
        for r in range(self._rows):
            row = [str(self._data[r * self._cols + c]) for c in range(self._cols)]
            rows.append("  [" + ", ".join(row) + "]")
        return "Matrix([\n" + "\n".join(rows) + "\n])"

    @property
    def shape(self):
        return (self._rows, self._cols)

    # ── operations ─────────────────────────────────────────────────────────

    def add(self, other):
        """Element-wise addition. O(rows*cols)."""
        if self.shape != other.shape:
            raise ValueError("Shape mismatch for addition.")
        result = Matrix(self._rows, self._cols)
        for i in range(len(self._data)):
            result._data[i] = self._data[i] + other._data[i]
        return result

    def subtract(self, other):
        """Element-wise subtraction. O(rows*cols)."""
        if self.shape != other.shape:
            raise ValueError("Shape mismatch for subtraction.")
        result = Matrix(self._rows, self._cols)
        for i in range(len(self._data)):
            result._data[i] = self._data[i] - other._data[i]
        return result

    def transpose(self):
        """Return transposed matrix. O(rows*cols)."""
        result = Matrix(self._cols, self._rows)
        for r in range(self._rows):
            for c in range(self._cols):
                result[c, r] = self[r, c]
        return result

    def multiply(self, other):
        """Standard matrix multiplication. O(n^3)."""
        if self._cols != other._rows:
            raise ValueError("Inner dimensions must agree for multiplication.")
        result = Matrix(self._rows, other._cols)
        for r in range(self._rows):
            for k in range(self._cols):
                for c in range(other._cols):
                    result[r, c] += self[r, k] * other[k, c]
        return result


# ─────────────────────────────────────────────────────────────────────────────
# Stack (array-backed, LIFO)
# ─────────────────────────────────────────────────────────────────────────────

class Stack:
    """
    LIFO stack backed by a DynamicArray.

    Time Complexities
    -----------------
    push  : O(1) amortized
    pop   : O(1) amortized
    peek  : O(1)
    """

    def __init__(self):
        self._arr = DynamicArray()

    def push(self, value):
        """Push value onto the top of the stack. O(1) amortized."""
        self._arr.append(value)

    def pop(self):
        """Remove and return the top element. O(1) amortized."""
        if self.is_empty():
            raise IndexError("Stack underflow: pop from empty stack.")
        return self._arr.delete(len(self._arr) - 1)

    def peek(self):
        """Return the top element without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("Stack is empty.")
        return self._arr[len(self._arr) - 1]

    def is_empty(self):
        return len(self._arr) == 0

    def __len__(self):
        return len(self._arr)

    def __repr__(self):
        return f"Stack(top→ {self._arr.to_list()[::-1]})"


# ─────────────────────────────────────────────────────────────────────────────
# Queue (circular-array, FIFO)
# ─────────────────────────────────────────────────────────────────────────────

class Queue:
    """
    FIFO queue using a circular array.

    Doubling/halving amortises the cost of resizing.

    Time Complexities
    -----------------
    enqueue : O(1) amortized
    dequeue : O(1) amortized
    peek    : O(1)
    """

    def __init__(self):
        self._capacity = 4
        self._data = [None] * self._capacity
        self._head = 0
        self._size = 0

    def _resize(self, new_cap):
        new_data = [None] * new_cap
        for i in range(self._size):
            new_data[i] = self._data[(self._head + i) % self._capacity]
        self._data = new_data
        self._head = 0
        self._capacity = new_cap

    def enqueue(self, value):
        """Add value to the back of the queue. O(1) amortized."""
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        tail = (self._head + self._size) % self._capacity
        self._data[tail] = value
        self._size += 1

    def dequeue(self):
        """Remove and return the front element. O(1) amortized."""
        if self.is_empty():
            raise IndexError("Queue underflow: dequeue from empty queue.")
        value = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        if self._size > 0 and self._size == self._capacity // 4:
            self._resize(max(4, self._capacity // 2))
        return value

    def peek(self):
        """Return the front element without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("Queue is empty.")
        return self._data[self._head]

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def __repr__(self):
        items = [self._data[(self._head + i) % self._capacity] for i in range(self._size)]
        return f"Queue(front→ {items})"


# ─────────────────────────────────────────────────────────────────────────────
# Singly Linked List
# ─────────────────────────────────────────────────────────────────────────────

class _SLLNode:
    """Node for a singly linked list."""
    __slots__ = ("value", "next")

    def __init__(self, value):
        self.value = value
        self.next  = None


class SinglyLinkedList:
    """
    Singly linked list supporting insertion, deletion, and traversal.

    Time Complexities
    -----------------
    prepend         : O(1)
    append          : O(n) without tail pointer; O(1) with (we maintain one)
    insert_after    : O(1) given node reference; O(n) by index
    delete_head     : O(1)
    delete          : O(n) search, O(1) removal
    search          : O(n)
    traverse        : O(n)
    """

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def prepend(self, value):
        """Insert at head. O(1)."""
        node = _SLLNode(value)
        node.next = self._head
        self._head = node
        if self._tail is None:
            self._tail = node
        self._size += 1

    def append(self, value):
        """Insert at tail. O(1) due to tail pointer."""
        node = _SLLNode(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def insert_after(self, target_value, new_value):
        """Insert new_value after the first node with target_value. O(n)."""
        cur = self._head
        while cur:
            if cur.value == target_value:
                node = _SLLNode(new_value)
                node.next = cur.next
                cur.next = node
                if cur is self._tail:
                    self._tail = node
                self._size += 1
                return
            cur = cur.next
        raise ValueError(f"Value {target_value} not found in list.")

    def delete(self, value):
        """Delete first occurrence of value. O(n)."""
        prev, cur = None, self._head
        while cur:
            if cur.value == value:
                if prev:
                    prev.next = cur.next
                else:
                    self._head = cur.next
                if cur is self._tail:
                    self._tail = prev
                self._size -= 1
                return
            prev, cur = cur, cur.next
        raise ValueError(f"Value {value} not found in list.")

    def search(self, value):
        """Return True if value exists. O(n)."""
        cur = self._head
        while cur:
            if cur.value == value:
                return True
            cur = cur.next
        return False

    def traverse(self):
        """Yield each value in order. O(n)."""
        cur = self._head
        while cur:
            yield cur.value
            cur = cur.next

    def to_list(self):
        return list(self.traverse())

    def __len__(self):
        return self._size

    def __repr__(self):
        return " -> ".join(str(v) for v in self.traverse()) + " -> None"


# ─────────────────────────────────────────────────────────────────────────────
# Rooted Tree (left-child / right-sibling representation)
# ─────────────────────────────────────────────────────────────────────────────

class _TreeNode:
    """
    Node for a general rooted tree.

    Uses the left-child / right-sibling (LCRS) representation so that
    each tree node requires only two pointers regardless of the number
    of children.
    """
    __slots__ = ("value", "left_child", "right_sibling", "parent")

    def __init__(self, value):
        self.value         = value
        self.left_child    = None    # first child
        self.right_sibling = None    # next sibling
        self.parent        = None


class RootedTree:
    """
    General rooted tree using the left-child / right-sibling representation.

    Supported operations:
        add_child(parent_val, child_val)
        remove_leaf(value)
        find(value)
        bfs_traversal()
        dfs_traversal()

    Time Complexities (n = number of nodes)
    ----------------------------------------
    find            : O(n)
    add_child       : O(n) (need to find parent)
    remove_leaf     : O(n)
    bfs / dfs       : O(n)
    """

    def __init__(self, root_value):
        self._root = _TreeNode(root_value)
        self._size = 1

    def find(self, value):
        """Return the node with the given value via BFS, or None. O(n)."""
        from collections import deque
        q = deque([self._root])
        while q:
            node = q.popleft()
            if node.value == value:
                return node
            child = node.left_child
            while child:
                q.append(child)
                child = child.right_sibling
        return None

    def add_child(self, parent_value, child_value):
        """Add a child node under the node with parent_value. O(n)."""
        parent = self.find(parent_value)
        if parent is None:
            raise ValueError(f"Parent value {parent_value} not found in tree.")
        child = _TreeNode(child_value)
        child.parent = parent
        # Attach as the rightmost sibling of parent's children
        if parent.left_child is None:
            parent.left_child = child
        else:
            sib = parent.left_child
            while sib.right_sibling:
                sib = sib.right_sibling
            sib.right_sibling = child
        self._size += 1

    def remove_leaf(self, value):
        """Remove a leaf node with the given value. O(n)."""
        if self._root.value == value:
            if self._root.left_child is None:
                self._root = None
                self._size -= 1
                return
            raise ValueError("Cannot remove root node that has children.")
        node = self.find(value)
        if node is None:
            raise ValueError(f"Value {value} not found in tree.")
        if node.left_child is not None:
            raise ValueError(f"Node {value} is not a leaf (has children).")
        parent = node.parent
        if parent.left_child is node:
            parent.left_child = node.right_sibling
        else:
            sib = parent.left_child
            while sib.right_sibling is not node:
                sib = sib.right_sibling
            sib.right_sibling = node.right_sibling
        self._size -= 1

    def bfs_traversal(self):
        """Breadth-first traversal, returning values level by level. O(n)."""
        from collections import deque
        result, q = [], deque([self._root])
        while q:
            node = q.popleft()
            result.append(node.value)
            child = node.left_child
            while child:
                q.append(child)
                child = child.right_sibling
        return result

    def dfs_traversal(self):
        """Pre-order depth-first traversal. O(n)."""
        result = []
        def _dfs(node):
            if node is None:
                return
            result.append(node.value)
            child = node.left_child
            while child:
                _dfs(child)
                child = child.right_sibling
        _dfs(self._root)
        return result

    def __len__(self):
        return self._size


# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────

def run_tests():
    print("=" * 60)
    print("Part 2: Elementary Data Structures — Tests")
    print("=" * 60)

    # ── DynamicArray ─────────────────────────────────────────────────────
    print("\n[DynamicArray]")
    da = DynamicArray()
    for v in range(10):
        da.append(v)
    assert len(da) == 10
    assert da[5] == 5
    da.insert(3, 99)
    assert da[3] == 99 and len(da) == 11
    da.delete(3)
    assert da[3] == 3 and len(da) == 10
    print(f"  Final array: {da.to_list()}  ✓")

    # ── Matrix ────────────────────────────────────────────────────────────
    print("\n[Matrix]")
    A = Matrix.from_list([[1, 2], [3, 4]])
    B = Matrix.from_list([[5, 6], [7, 8]])
    C = A.multiply(B)
    assert C[0, 0] == 19 and C[1, 1] == 50
    T = A.transpose()
    assert T[0, 1] == 3
    print(f"  A × B top-left = {C[0,0]} (expected 19)  ✓")
    print(f"  A^T[0,1] = {T[0,1]} (expected 3)  ✓")

    # ── Stack ─────────────────────────────────────────────────────────────
    print("\n[Stack]")
    s = Stack()
    for v in [10, 20, 30]:
        s.push(v)
    assert s.peek() == 30
    assert s.pop() == 30
    assert len(s) == 2
    print(f"  After 3 pushes then 1 pop: {repr(s)}  ✓")

    # ── Queue ─────────────────────────────────────────────────────────────
    print("\n[Queue]")
    q = Queue()
    for v in [10, 20, 30]:
        q.enqueue(v)
    assert q.peek() == 10
    assert q.dequeue() == 10
    assert len(q) == 2
    print(f"  After 3 enqueues then 1 dequeue: {repr(q)}  ✓")

    # ── SinglyLinkedList ──────────────────────────────────────────────────
    print("\n[SinglyLinkedList]")
    ll = SinglyLinkedList()
    for v in [1, 2, 3, 4, 5]:
        ll.append(v)
    ll.insert_after(3, 99)
    assert ll.to_list() == [1, 2, 3, 99, 4, 5]
    ll.delete(99)
    assert ll.to_list() == [1, 2, 3, 4, 5]
    assert ll.search(3) is True
    assert ll.search(99) is False
    print(f"  List after ops: {ll}  ✓")

    # ── RootedTree ────────────────────────────────────────────────────────
    print("\n[RootedTree]")
    tree = RootedTree("A")
    tree.add_child("A", "B")
    tree.add_child("A", "C")
    tree.add_child("B", "D")
    tree.add_child("B", "E")
    tree.add_child("C", "F")
    bfs = tree.bfs_traversal()
    dfs = tree.dfs_traversal()
    assert bfs == ["A", "B", "C", "D", "E", "F"]
    assert dfs == ["A", "B", "D", "E", "C", "F"]
    tree.remove_leaf("F")
    assert len(tree) == 5
    print(f"  BFS: {bfs}  ✓")
    print(f"  DFS: {dfs}  ✓")
    print(f"  Size after removing leaf 'F': {len(tree)}  ✓")

    print("\nAll tests passed ✓\n")


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_tests()