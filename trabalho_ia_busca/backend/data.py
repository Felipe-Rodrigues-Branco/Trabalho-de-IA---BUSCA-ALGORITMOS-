# -*- coding: utf-8 -*-
"Dados do grafo das capitais brasileiras.
Observação: as distâncias foram estimadas a partir de coordenadas geográficas com fator rodoviário.
Caso ache necessário poderá utilizar os valores reais do google maps"

from math import radians, sin, cos, asin, sqrt

CAPITAIS = {
    "Rio Branco (AC)": (-9.97499, -67.8243),
    "Maceió (AL)": (-9.66599, -35.735),
    "Macapá (AP)": (0.034934, -51.0694),
    "Manaus (AM)": (-3.11903, -60.0217),
    "Salvador (BA)": (-12.9714, -38.5014),
    "Fortaleza (CE)": (-3.7319, -38.5267),
    "Brasília (DF)": (-15.7939, -47.8828),
    "Vitória (ES)": (-20.3155, -40.3128),
    "Goiânia (GO)": (-16.6869, -49.2648),
    "São Luís (MA)": (-2.53073, -44.3068),
    "Cuiabá (MT)": (-15.601, -56.0974),
    "Campo Grande (MS)": (-20.4697, -54.6201),
    "Belo Horizonte (MG)": (-19.9167, -43.9345),
    "Belém (PA)": (-1.45583, -48.5044),
    "João Pessoa (PB)": (-7.11532, -34.861),
    "Curitiba (PR)": (-25.4284, -49.2733),
    "Recife (PE)": (-8.04756, -34.877),
    "Teresina (PI)": (-5.08921, -42.8016),
    "Rio de Janeiro (RJ)": (-22.9068, -43.1729),
    "Natal (RN)": (-5.79448, -35.211),
    "Porto Alegre (RS)": (-30.0346, -51.2177),
    "Porto Velho (RO)": (-8.76077, -63.8999),
    "Boa Vista (RR)": (2.82384, -60.6753),
    "Florianópolis (SC)": (-27.5954, -48.548),
    "São Paulo (SP)": (-23.5505, -46.6333),
    "Aracaju (SE)": (-10.9472, -37.0731),
    "Palmas (TO)": (-10.184, -48.3336),
}

# Estados vizinhos + exceções do enunciado: DF-GO e DF-MG.
ARESTAS_ESTADOS = [
    ("Rio Branco (AC)", "Manaus (AM)"),
    ("Rio Branco (AC)", "Porto Velho (RO)"),
    ("Maceió (AL)", "Recife (PE)"),
    ("Maceió (AL)", "Aracaju (SE)"),
    ("Maceió (AL)", "Salvador (BA)"),
    ("Macapá (AP)", "Belém (PA)"),
    ("Macapá (AP)", "Boa Vista (RR)"),
    ("Manaus (AM)", "Boa Vista (RR)"),
    ("Manaus (AM)", "Porto Velho (RO)"),
    ("Manaus (AM)", "Cuiabá (MT)"),
    ("Manaus (AM)", "Belém (PA)"),
    ("Salvador (BA)", "Aracaju (SE)"),
    ("Salvador (BA)", "Recife (PE)"),
    ("Salvador (BA)", "Teresina (PI)"),
    ("Salvador (BA)", "Palmas (TO)"),
    ("Salvador (BA)", "Goiânia (GO)"),
    ("Salvador (BA)", "Belo Horizonte (MG)"),
    ("Salvador (BA)", "Vitória (ES)"),
    ("Fortaleza (CE)", "Natal (RN)"),
    ("Fortaleza (CE)", "João Pessoa (PB)"),
    ("Fortaleza (CE)", "Recife (PE)"),
    ("Fortaleza (CE)", "Teresina (PI)"),
    ("Goiânia (GO)", "Palmas (TO)"),
    ("Goiânia (GO)", "Cuiabá (MT)"),
    ("Goiânia (GO)", "Campo Grande (MS)"),
    ("Goiânia (GO)", "Belo Horizonte (MG)"),
    ("Brasília (DF)", "Goiânia (GO)"),
    ("Brasília (DF)", "Belo Horizonte (MG)"),
    ("Vitória (ES)", "Belo Horizonte (MG)"),
    ("Vitória (ES)", "Rio de Janeiro (RJ)"),
    ("São Luís (MA)", "Belém (PA)"),
    ("São Luís (MA)", "Palmas (TO)"),
    ("São Luís (MA)", "Teresina (PI)"),
    ("Cuiabá (MT)", "Porto Velho (RO)"),
    ("Cuiabá (MT)", "Belém (PA)"),
    ("Cuiabá (MT)", "Palmas (TO)"),
    ("Cuiabá (MT)", "Campo Grande (MS)"),
    ("Campo Grande (MS)", "Belo Horizonte (MG)"),
    ("Campo Grande (MS)", "São Paulo (SP)"),
    ("Campo Grande (MS)", "Curitiba (PR)"),
    ("Belo Horizonte (MG)", "Rio de Janeiro (RJ)"),
    ("Belo Horizonte (MG)", "São Paulo (SP)"),
    ("Belém (PA)", "Boa Vista (RR)"),
    ("Belém (PA)", "Palmas (TO)"),
    ("João Pessoa (PB)", "Natal (RN)"),
    ("João Pessoa (PB)", "Recife (PE)"),
    ("Curitiba (PR)", "São Paulo (SP)"),
    ("Curitiba (PR)", "Florianópolis (SC)"),
    ("Recife (PE)", "Teresina (PI)"),
    ("Teresina (PI)", "Palmas (TO)"),
    ("Rio de Janeiro (RJ)", "São Paulo (SP)"),
    ("Porto Alegre (RS)", "Florianópolis (SC)"),
]

ROTAS_COMUNS = [
    ("São Paulo (SP)", "Rio de Janeiro (RJ)", 150), ("Brasília (DF)", "Goiânia (GO)", 140),
    ("Rio de Janeiro (RJ)", "Belo Horizonte (MG)", 130), ("São Paulo (SP)", "Recife (PE)", 120),
    ("Manaus (AM)", "São Paulo (SP)", 110), ("Fortaleza (CE)", "São Paulo (SP)", 100),
    ("Porto Alegre (RS)", "Brasília (DF)", 90), ("São Paulo (SP)", "Salvador (BA)", 90),
    ("Rio de Janeiro (RJ)", "Salvador (BA)", 85), ("Belém (PA)", "Manaus (AM)", 80),
    ("Belo Horizonte (MG)", "Brasília (DF)", 80), ("Belém (PA)", "Rio de Janeiro (RJ)", 75),
    ("Florianópolis (SC)", "Porto Alegre (RS)", 75), ("Recife (PE)", "Salvador (BA)", 75),
    ("Curitiba (PR)", "Natal (RN)", 70), ("Curitiba (PR)", "Florianópolis (SC)", 70),
    ("Porto Alegre (RS)", "Rio de Janeiro (RJ)", 70), ("São Luís (MA)", "Belém (PA)", 65),
    ("São Paulo (SP)", "Florianópolis (SC)", 65), ("Salvador (BA)", "Brasília (DF)", 65),
    ("Belo Horizonte (MG)", "São Luís (MA)", 60), ("Natal (RN)", "Fortaleza (CE)", 60),
    ("Cuiabá (MT)", "Goiânia (GO)", 60), ("Cuiabá (MT)", "Vitória (ES)", 55),
    ("Fortaleza (CE)", "Teresina (PI)", 55), ("Vitória (ES)", "Rio de Janeiro (RJ)", 55),
    ("Campo Grande (MS)", "Curitiba (PR)", 55), ("Brasília (DF)", "Cuiabá (MT)", 55),
    ("Campo Grande (MS)", "Recife (PE)", 50), ("Recife (PE)", "João Pessoa (PB)", 50),
    ("Teresina (PI)", "São Luís (MA)", 50), ("Manaus (AM)", "Porto Velho (RO)", 50),
    ("Rio de Janeiro (RJ)", "Vitória (ES)", 50), ("Maceió (AL)", "Recife (PE)", 45),
    ("João Pessoa (PB)", "Natal (RN)", 45), ("Porto Velho (RO)", "Cuiabá (MT)", 45),
    ("Teresina (PI)", "Brasília (DF)", 45), ("Salvador (BA)", "Aracaju (SE)", 40),
    ("Manaus (AM)", "Boa Vista (RR)", 40), ("Palmas (TO)", "Brasília (DF)", 40),
    ("João Pessoa (PB)", "Salvador (BA)", 40), ("Aracaju (SE)", "Maceió (AL)", 35),
    ("Porto Velho (RO)", "Rio Branco (AC)", 35), ("Palmas (TO)", "Belém (PA)", 35),
    ("Maceió (AL)", "Belo Horizonte (MG)", 35), ("Belém (PA)", "Macapá (AP)", 30),
    ("Macapá (AP)", "Fortaleza (CE)", 30), ("Aracaju (SE)", "Rio de Janeiro (RJ)", 30),
    ("Rio Branco (AC)", "São Paulo (SP)", 25), ("Boa Vista (RR)", "Brasília (DF)", 20),
]

def haversine_km(a, b):
    lat1, lon1 = CAPITAIS[a]
    lat2, lon2 = CAPITAIS[b]
    R = 6371
    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    h = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return 2 * R * asin(sqrt(h))

def distancia_rodoviaria(a, b):
    # Fator médio para aproximar estrada real a partir da distância em linha reta.
    return round(haversine_km(a, b) * 1.28)

def construir_grafo():
    grafo = {c: {} for c in CAPITAIS}
    for a, b in ARESTAS_ESTADOS:
        d = distancia_rodoviaria(a, b)
        grafo[a][b] = d
        grafo[b][a] = d
    return grafo
