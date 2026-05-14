# -*- coding: utf-8 -*-
import heapq, random
from data import CAPITAIS, ROTAS_COMUNS, construir_grafo, haversine_km

CUSTO_RODOVIA_KM = 5.00
CUSTO_FERROVIA_KM = 1.20
CUSTO_TRANSBORDO = 1000.00
CUSTO_CONSTRUCAO_FERROVIA_KM = 2_000_000.00

def heuristic_dist(a, b):
    return haversine_km(a, b)

def edges_from_graph(grafo):
    edges = []
    seen = set()
    for a, viz in grafo.items():
        for b, d in viz.items():
            key = tuple(sorted((a,b)))
            if key not in seen:
                seen.add(key)
                edges.append((a,b,d))
    return edges

class DSU:
    def __init__(self, nodes):
        self.parent = {n:n for n in nodes}
        self.rank = {n:0 for n in nodes}
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        if self.rank[ra] < self.rank[rb]: ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]: self.rank[ra] += 1
        return True

def kruskal(grafo):
    dsu = DSU(grafo.keys())
    mst = []
    total_km = 0
    for a,b,d in sorted(edges_from_graph(grafo), key=lambda x: x[2]):
        if dsu.union(a,b):
            mst.append((a,b,d))
            total_km += d
    return mst, total_km, total_km * CUSTO_CONSTRUCAO_FERROVIA_KM

def a_star_rodoviario(grafo, origem, destino):
    pq = [(heuristic_dist(origem, destino), 0, origem, [origem])]
    best = {origem: 0}
    while pq:
        _, custo_km, atual, caminho = heapq.heappop(pq)
        if atual == destino:
            return {"path": caminho, "distance_km": round(custo_km,2), "cost": round(custo_km*CUSTO_RODOVIA_KM,2)}
        for viz, dist in grafo[atual].items():
            novo = custo_km + dist
            if novo < best.get(viz, float('inf')):
                best[viz] = novo
                f = novo + heuristic_dist(viz, destino)
                heapq.heappush(pq, (f, novo, viz, caminho+[viz]))
    return None

def ferro_set(malha):
    return {tuple(sorted((a,b))) for a,b,_ in malha}

def a_star_multimodal(grafo, origem, destino, malha):
    ferrovias = ferro_set(malha)
    modos = ["rodovia", "ferrovia"]
    start = (origem, "rodovia")
    pq = [(0, 0, origem, "rodovia", [(origem, "rodovia")])]
    best = {start: 0}
    while pq:
        _, custo, atual, modo_atual, caminho = heapq.heappop(pq)
        if atual == destino:
            return {"path": caminho, "cost": round(custo,2)}
        for viz, dist in grafo[atual].items():
            key = tuple(sorted((atual, viz)))
            opcoes = [("rodovia", dist*CUSTO_RODOVIA_KM)]
            if key in ferrovias:
                opcoes.append(("ferrovia", dist*CUSTO_FERROVIA_KM))
            for modo_novo, custo_trecho in opcoes:
                transbordo = CUSTO_TRANSBORDO if modo_novo != modo_atual else 0
                novo = custo + custo_trecho + transbordo
                estado = (viz, modo_novo)
                if novo < best.get(estado, float('inf')):
                    best[estado] = novo
                    # heurística admissível baseada no menor custo possível por km
                    h = heuristic_dist(viz, destino) * CUSTO_FERROVIA_KM
                    heapq.heappush(pq, (novo+h, novo, viz, modo_novo, caminho+[(viz, modo_novo)]))
    return None

def avaliar_malha(grafo, selected_edges, budget):
    custo_impl = sum(d for _,_,d in selected_edges) * CUSTO_CONSTRUCAO_FERROVIA_KM
    if custo_impl > budget:
        return 10**18 + custo_impl
    total_operacional = 0
    for o,d,cargas in ROTAS_COMUNS:
        r = a_star_multimodal(grafo, o, d, selected_edges)
        total_operacional += (r["cost"] if r else 10**12) * cargas
    return total_operacional

def genetic_algorithm(grafo, budget, pop_size=80, generations=120, mutation_rate=0.03, seed=42):
    random.seed(seed)
    edges = edges_from_graph(grafo)
    n = len(edges)
    def random_individual():
        ind = [0]*n
        order = list(range(n)); random.shuffle(order)
        cost = 0
        for i in order:
            add = edges[i][2] * CUSTO_CONSTRUCAO_FERROVIA_KM
            if cost + add <= budget and random.random() < 0.45:
                ind[i] = 1; cost += add
        return ind
    def decode(ind):
        return [edges[i] for i,b in enumerate(ind) if b]
    def fitness(ind):
        return avaliar_malha(grafo, decode(ind), budget)
    def repair(ind):
        while sum(edges[i][2] * CUSTO_CONSTRUCAO_FERROVIA_KM for i,b in enumerate(ind) if b) > budget:
            ones = [i for i,b in enumerate(ind) if b]
            ind[random.choice(ones)] = 0
        return ind
    population = [random_individual() for _ in range(pop_size)]
    best_ind, best_fit = None, float('inf')
    for _ in range(generations):
        scored = sorted((fitness(ind), ind) for ind in population)
        if scored[0][0] < best_fit:
            best_fit, best_ind = scored[0][0], scored[0][1][:]
        elite = [ind[:] for _, ind in scored[:8]]
        newpop = elite[:]
        while len(newpop) < pop_size:
            p1 = random.choice(scored[:30])[1]
            p2 = random.choice(scored[:30])[1]
            cut = random.randint(1, n-2)
            child = p1[:cut] + p2[cut:]
            for i in range(n):
                if random.random() < mutation_rate:
                    child[i] = 1-child[i]
            newpop.append(repair(child))
        population = newpop
    malha = decode(best_ind)
    total_km = sum(d for _,_,d in malha)
    return {"edges": malha, "total_km": total_km, "implementation_cost": total_km*CUSTO_CONSTRUCAO_FERROVIA_KM, "objective_cost": best_fit}
