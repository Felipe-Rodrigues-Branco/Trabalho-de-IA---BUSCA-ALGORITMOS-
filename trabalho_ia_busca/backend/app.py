# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
from data import CAPITAIS, construir_grafo
from algorithms import a_star_rodoviario, kruskal, a_star_multimodal, genetic_algorithm

app = Flask(__name__)
CORS(app)
GRAFO = construir_grafo()
MST, MST_KM, MST_COST = kruskal(GRAFO)
GA_CACHE = None

@app.get('/api/capitais')
def capitais():
    return jsonify(sorted(CAPITAIS.keys()))

@app.get('/api/grafo')
def grafo():
    edges = []
    seen = set()
    for a, viz in GRAFO.items():
        for b, d in viz.items():
            key = tuple(sorted((a,b)))
            if key not in seen:
                seen.add(key)
                edges.append({"from": a, "to": b, "km": d})
    return jsonify({"nodes": sorted(CAPITAIS.keys()), "edges": edges})

@app.get('/api/astar/rodovia')
def astar_rodovia():
    origem = request.args.get('origem')
    destino = request.args.get('destino')
    return jsonify(a_star_rodoviario(GRAFO, origem, destino))

@app.get('/api/kruskal')
def api_kruskal():
    return jsonify({"edges": [{"from":a,"to":b,"km":d} for a,b,d in MST], "total_km": MST_KM, "implementation_cost": MST_COST})

@app.get('/api/astar/kruskal')
def astar_kruskal():
    origem = request.args.get('origem')
    destino = request.args.get('destino')
    return jsonify(a_star_multimodal(GRAFO, origem, destino, MST))

@app.get('/api/genetico')
def api_genetico():
    global GA_CACHE
    if GA_CACHE is None:
        budget = MST_COST * 0.60
        GA_CACHE = genetic_algorithm(GRAFO, budget)
        GA_CACHE["budget"] = budget
    return jsonify({**GA_CACHE, "edges": [{"from":a,"to":b,"km":d} for a,b,d in GA_CACHE["edges"]]})

@app.get('/api/astar/genetico')
def astar_genetico():
    global GA_CACHE
    if GA_CACHE is None:
        budget = MST_COST * 0.60
        GA_CACHE = genetic_algorithm(GRAFO, budget)
        GA_CACHE["budget"] = budget
    origem = request.args.get('origem')
    destino = request.args.get('destino')
    return jsonify(a_star_multimodal(GRAFO, origem, destino, GA_CACHE["edges"]))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
