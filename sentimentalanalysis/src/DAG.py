class DAG:
    def __init__(self):
        self.adj_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, start, end, weight=0):
        if start not in self.adj_list:
            self.add_vertex(start)
        if end not in self.adj_list:
            self.add_vertex(end)
        self.adj_list[start].append((end, weight))

    def topological_sort(self):
        in_degree = {v: 0 for v in self.adj_list}
        for v in self.adj_list:
            for neighbor, weight in self.adj_list[v]:
                in_degree[neighbor] += 1

        queue = [v for v in self.adj_list if in_degree[v] == 0]
        topo_order = []
        while queue:
            v = queue.pop(0)
            topo_order.append(v)
            for neighbor, weight in self.adj_list[v]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(topo_order) != len(self.adj_list):
            return None
        else:
            return topo_order

    def shortest_path(self, start):
        topo_order = self.topological_sort()
        dist = {v: float('inf') for v in self.adj_list}
        dist[start] = 0
        for v in topo_order:
            for neighbor, weight in self.adj_list[v]:
                if dist[v] + weight < dist[neighbor]:
                    dist[neighbor] = dist[v] + weight
        return dist






