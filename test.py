import collections

class Solution:
    def isBipartite(self, graph) -> bool:
        colors = {}

        for i in range(len(graph)):
            if i not in colors:
                colors[i] = 0
                queue = collections.deque([])
                queue.append(i)
                while len(queue) > 0:
                    ele = queue.popleft()
                    for j in graph[ele]:
                        if j in colors:
                            if colors[j] ^ colors[ele] == 0:
                                return False
                        else:
                            colors[j] = 1 - colors[ele]
                            queue.append(j)
                        print(colors)
        return True
s = Solution()
print(s.isBipartite([[1, 2, 3], [0, 2], [1, 3], [0, 1, 2]]))