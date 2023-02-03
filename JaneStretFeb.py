array = [[0, 6, 36, 30, 34, 27, 3, 40, 27, 0, 0, 7, 0, 0],
         [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
         [7, 0, 0, 0, 1, 0, 0, 0, 0, 0, 6, 5, 0, 0],
         [7, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 6, 0, 0],
         [33, 0, 4, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 1],
         [29, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 7, 0],
         [2, 0, 0, 6, 0, 0, 0, 0, 0, 3, 7, 0, 0, 0],
         [40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 7, 0, 5, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 5, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0],
         [36, 0, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 7],
         [0, 6, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 5, 0]]

# rb = []
# for i in range(8, 13):
#     rb.append(array[i][8:13])
#
# rt = []
# for i in range(1, 6):
#     rt.append(array[i][8:13])
#
# lb = []
# for i in range(8, 13):
#     lb.append(array[i][1:6])
#
# lt = []
# for i in range(1, 6):
#     lt.append(array[i][1:6])

#21 blanks
#28 numbers
from itertools import permutations
possibilities = [[1, 5, 7, 7], [1, 6, 6, 7], [2, 4, 7, 7], [2, 5, 6, 7], [2, 6, 6, 6], [3, 3, 7, 7], [3, 4, 6, 7], [3, 5, 5, 7], [3, 5, 6, 6], [4, 4, 5, 7], [4, 4, 6, 6], [4, 5, 5, 6], [5, 5, 5, 5]]
# generate all possibilities
from collections import Counter
pp = []
for i in possibilities:
    for j in range(0,8):
        for k in range(0,8):
            for l in range(0,8):
                toperm = i+[j]+[k]+[l]
                count = Counter(toperm)
                if count[1] <=1 and count[2] <=2 and count[3]<=3 and count[4]<=4 and count[5]<=5 and count[6]<=6:
                    pp.append(list(permutations(toperm)))
print(len(pp))
with open('myfile.txt', 'w') as f:
    f.writelines([f"{x}\n" for x in pp])
#remove all permutations by addind seen and sorted to set, if in set, don't add
# tt = [x[:y] + [0] + x[y:] for y in range(5) for x in possibilities]
# print(tt)
# toTestTest = []
# for i in toTest:
#     for j in toTest:
#         for k in toTest:
#             for l in toTest:
#                 for m in toTest:
#                     if all([i[n]+j[n]+k[n]+l[n]+m[n] == 20 for n in range(5)]):
#                         toTestTest.append([i,j,k,l,m])
# print(toTestTest)
                            
# Each 7 by 7:
# r= 4 numbers, sum to 20
# c = 4 numbers, sum to 20
# max N of N in range (1,8)
# all numbers must be connected orthogonally
# Also test connections in any direction? Diagonally? As well as orthogonally
# Every 2by2 subsquare must have AT LEAST one empty cell

# def isValidSudoku(self, board: List[List[str]]) -> bool:
#     cols = collections.defaultdict(set)
#     rows = collections.defaultdict(set)
#     squares = collections.defaultdict(set) #key == (r//3,c//3)
#
#     for r in range(9):
#         for c in range(9):
#             if board[r][c] == '.':
#                 continue
#             if (board[r][c] in rows[r] or
#             board[r][c] in cols[c] or
#             board[r][c] in squares[(r//3,c//3)]):
#                 return False
#             squares[(r//3,c//3)].add(board[r][c])
#             cols[c].add(board[r][c])
#             rows[r].add(board[r][c])
#     return True
