# Trabalho de IA - Resolução de Problemas por Busca

Implementação dos itens solicitados no Trabalho de Implementação 1 da disciplina de Inteligência Artificial.

## O que foi implementado

- Grafo das 27 capitais brasileiras, considerando ligações diretas entre capitais de estados vizinhos e a exceção Brasília ↔ Belo Horizonte.
- A* para encontrar a rota rodoviária mais barata entre duas capitais.
- Kruskal para gerar a malha ferroviária mínima conectando todas as capitais.
- A* multimodal considerando rodovia, ferrovia e custo de transbordo.
- Algoritmo Genético para escolher trechos ferroviários respeitando orçamento de 60% do custo da malha de Kruskal.
- A* usando a malha ferroviária gerada pelo Algoritmo Genético.
- Interface web simples para entrada de origem/destino e exibição dos resultados.

## Observação importante sobre as distâncias

As distâncias do arquivo `backend/data.py` foram estimadas a partir das coordenadas das capitais com um fator rodoviário médio. Caso você queira testar algo mais "realista" sugiro que substitua os valores pelo levantamento manual do Google Maps.

## Como rodar

### 1. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requisitos.txt
python app.py
```

A API ficará disponível em:

```text
http://localhost:5000/api
```

### 2. Frontend

Abra o arquivo:

```text
frontend/index.html
```

no navegador.

## Endpoints principais

- `GET /api/capitais`
- `GET /api/grafo`
- `GET /api/astar/rodovia?origem=São Paulo (SP)&destino=Rio de Janeiro (RJ)`
- `GET /api/kruskal`
- `GET /api/astar/kruskal?origem=São Paulo (SP)&destino=Rio de Janeiro (RJ)`
- `GET /api/genetico`
- `GET /api/astar/genetico?origem=São Paulo (SP)&destino=Rio de Janeiro (RJ)`

