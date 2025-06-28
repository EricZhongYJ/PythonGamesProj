n = [8]  # Number of column
data = []  # Data of chessboard: data[j][i] = [Id, obj]
step = []  # Data of each step


def setN(num):  # Set n
    global data
    n[0] = num  # Number of column
    data.clear()
    for i in range(n[0]):
        data += [[0] * n[0]]


class __obj:  # Private super class
    def __init__(self, x, y, player, Id):
        self.x = x
        self.y = y
        self.player = player  # -1 Computer and 1 Player
        self.Id = Id

    def _touch(self, dx, dy, K):  # K: # of steps
        ret = []
        for i in range(len(dx)):
            x, y = self.x, self.y
            for k in range(K):
                x += dx[i] * self.player
                y += dy[i]
                if 0 <= x < n[0] and 0 <= y < n[0] and \
                        not (data[x][y] and (data[x][y][1].player > 0) == (self.player > 0)):
                    ret += [[x, y]]
                    if data[x][y] and (data[x][y][1].player > 0) != (self.player > 0):
                        break
                else:
                    break
        return ret

    def touch(self):
        return []

    def __repr__(self):  # todo
        return '<%d,%s>' % (self.player, str(self.__class__)[18:-1])


class king(__obj):  # King
    def touch(self):
        return self._touch([-1, -1, -1, 0, 0, 1, 1, 1], [-1, 0, 1, -1, 1, -1, 0, 1], 1)


class queen(__obj):  # Queen
    def touch(self):
        return self._touch([-1, -1, -1, 0, 0, 1, 1, 1], [-1, 0, 1, -1, 1, -1, 0, 1], n[0])


class che(__obj):  # Rook
    def touch(self):
        return self._touch([-1, 0, 0, 1], [0, -1, 1, 0], n[0])


class xiang(__obj):  # Bishop
    def touch(self):
        return self._touch([-1, -1, 1, 1], [-1, 1, -1, 1], n[0])


class ma(__obj):  # Knight
    def touch(self):
        return self._touch([-2, -2, -1, -1, 1, 1, 2, 2], [-1, 1, -2, 2, -2, 2, -1, 1], 1)


class bing(__obj):  # Pawn
    # Which block can it reach
    def _touch(self, dx, dy, K):  # K: # of steps
        ret = []
        for i in range(len(dx)):
            x, y = self.x, self.y
            for k in range(K):
                x += dx[i] * self.player
                y += dy[i]
                if 0 <= x < n[0] and 0 <= y < n[0] and not data[x][y]:
                    ret += [[x, y]]
                else:
                    break
        return ret

    # Which one can it eat
    def _eat(self):
        ret = []
        dx, dy = [-1, -1], [-1, 1]
        for i in range(len(dx)):
            x, y = self.x, self.y
            x += dx[i] * self.player
            y += dy[i]
            if 0 <= x < n[0] and 0 <= y < n[0] and data[x][y] and \
                     (data[x][y][1].player > 0) != (self.player > 0):
                ret += [[x, y]]
        return ret

    # Color the block it can reach (different color for computer and player)
    def touch(self):
        if (self.player > 0 and self.x == 6) or (self.player < 0 and self.x == 1):
            return self._touch([-1], [0], 2) + self._eat()
        else:
            return self._touch([-1], [0], 1) + self._eat()
