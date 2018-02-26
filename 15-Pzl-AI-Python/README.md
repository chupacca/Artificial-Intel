

Index: 
	-> (DEPTH, NUMBER CREATED, EXPANISON NUMBER, FRINGE)
	-> b = branching factor
	-> d = depth

IDS

Command: python fifteen-pzl.py '12345678 abc9def' ids

(4, 32, 35, 3)

O(b^d*l): O(4^4*4)

DFS

Command: python fifteen-pzl.py '237416b859ecd af' dfs

(52, 108, 53, 56)

O(b^d): O(4^52)

BFS

Command: python fifteen-pzl.py '237416b859ecd af' bfs

(12, 33356, 16662, 16695)

O(b^d): O(4^12)

A*

python fifteen-pzl.py 'a876bc1532ef 49d' astar h2

(131, 2086, 1021, 1066)

O(d*logb)): O(log 4*(131))

A*

Command: python fifteen-pzl.py 'a876bc1532ef 49d' astar h1

(131, 2086, 1021, 1066)

O(d*logb)): O(log 4*(131))

GBFS h1

Command: python fifteen-pzl.py 'a876bc1532ef 49d' gbfs h1

(221, 65177, 33639, 31539)

O(d*logb): O(221*4*log(221))


GBFS h2

Command: python fifteen-pzl.py 'a876bc1532ef 49d' gbfs h2

(197, 8095, 4050, 4046)

O(db*logb): O(221*4*log(221))

