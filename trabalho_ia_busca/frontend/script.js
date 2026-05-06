const API = 'http://localhost:5000/api';

async function getJson(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error('Erro na API');
  return r.json();
}

function money(v) {
  return Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function linePath(path) {
  if (!path) return '';
  if (Array.isArray(path) && Array.isArray(path[0])) {
    return path.map(([cidade, modo]) => `${cidade} [${modo}]`).join(' → ');
  }
  return path.join(' → ');
}

async function carregarCapitais() {
  const capitais = await getJson(`${API}/capitais`);
  for (const id of ['origem', 'destino']) {
    const sel = document.getElementById(id);
    capitais.forEach(c => {
      const op = document.createElement('option');
      op.value = c; op.textContent = c;
      sel.appendChild(op);
    });
  }
  document.getElementById('origem').value = 'São Paulo (SP)';
  document.getElementById('destino').value = 'Rio de Janeiro (RJ)';
}

async function buscarRota() {
  const origem = encodeURIComponent(document.getElementById('origem').value);
  const destino = encodeURIComponent(document.getElementById('destino').value);
  const tipo = document.getElementById('tipo').value;
  const endpoint = tipo === 'rodovia' ? 'astar/rodovia' : tipo === 'kruskal' ? 'astar/kruskal' : 'astar/genetico';
  const data = await getJson(`${API}/${endpoint}?origem=${origem}&destino=${destino}`);
  let texto = `Caminho: ${linePath(data.path)}\n`;
  if (data.distance_km) texto += `Distância: ${data.distance_km} km\n`;
  texto += `Custo de transporte: ${money(data.cost)}\n`;
  document.getElementById('resultadoRota').textContent = texto;
}

async function carregarKruskal() {
  const data = await getJson(`${API}/kruskal`);
  const linhas = data.edges.map(e => `${e.from} ↔ ${e.to}: ${e.km} km`).join('\n');
  document.getElementById('resultadoKruskal').textContent =
    `Total: ${data.total_km} km\nCusto da obra: ${money(data.implementation_cost)}\n\nTrechos:\n${linhas}`;
}

async function carregarGenetico() {
  const data = await getJson(`${API}/genetico`);
  const linhas = data.edges.map(e => `${e.from} ↔ ${e.to}: ${e.km} km`).join('\n');
  document.getElementById('resultadoGenetico').textContent =
    `Orçamento: ${money(data.budget)}\nCusto de implantação usado: ${money(data.implementation_cost)}\nTotal ferroviário: ${data.total_km} km\nFunção objetivo: ${money(data.objective_cost)}\n\nTrechos escolhidos:\n${linhas}`;
}

carregarCapitais();
