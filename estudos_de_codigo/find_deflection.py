# Objetivo: transformar dados brutos do sensor em uma resposta clara:
# "A força aplicada causou um deslocamento de X µm, com margem de erro Y µm".

import matplotlib.pyplot as plt   # plotagem
import pandas as pd               # leitura/manipulação de dados tabulares
import numpy as np                # operações numéricas (vetores/matrizes)
import math                       # utilidades matemáticas
from scipy import signal          # processamento de sinais (filtros)

# ---------------- Parâmetros iniciais ----------------
Filename = '5.caldata_m4_l5_F9,725.txt'  # arquivo TAB-separado com (tempo, deslocamento)

time = []    # vetor de tempo (s)
d = []       # vetor de deslocamento (µm) — será convertido no loop abaixo
#av = []     # (COMENTADO) média móvel ponto a ponto (não usado nesta versão)
std = []     # (não usado; mantido de versões anteriores)
#av0 = []    # (COMENTADO) outra média (não usada)
#w = 8000    # (COMENTADO) largura de janela para médias móveis

find_diff = True         # se True, calcula diferença de médias entre duas janelas de tempo
time1 = [150, 280]       # janela 1 em segundos (início, fim)
time2 = [400, 600]       # janela 2 em segundos (início, fim)

cutoff_freq = 0.05       # frequência de corte do filtro passa-baixas (Hz)
order = 5                # ordem do filtro Butterworth

# ---------------- Leitura do arquivo ----------------
data = pd.read_csv(Filename, sep="\t", header=None)  # lê como dataframe sem cabeçalho

# Converte strings com vírgula decimal para float e deslocamento para µm
for i in range(len(data[0])):
    time.append(float(data[0][i].replace(',', '.')))           # tempo (s)
    d.append(float(data[1][i].replace(',', '.')) * 1000)       # deslocamento (µm)

# fullav = np.average(d)  # (COMENTADO) média global do deslocamento

'''
# (COMENTADO) exemplo de cálculo de média móvel e desvio por janela deslizante de largura w
for i in range(len(d)-w):
    ptval = []
    for j in range(-int(w/2), int(w/2)):
        ptval.append(d[i+int(w/2)+j])
    av.append(np.average(ptval))
    std.append(np.std(ptval))
    # av0.append(np.average(d[i-int(w/2):i+int(w/2)]))
'''

# ---------------- Parâmetros de amostragem e filtro ----------------
N = len(d)  # número de amostras
# fs = N / (t_final - t_inicial)  → frequência de amostragem (Hz)
fs = N / (float(data[0][N-1].replace(',', '.')) - float(data[0][0].replace(',', '.')))

# Projeto do Butterworth passa-baixas (ordem 'order', corte 'cutoff_freq', com fs explícita)
b, a = signal.butter(order, cutoff_freq, analog=False, btype='lowpass', fs=fs)
# Filtro zero-fase (aplica ida e volta para não deslocar a fase)
av = signal.filtfilt(b, a, d)

# ---------------- Função utilitária: índice do ponto mais próximo ----------------
def find_nearest_index(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()  # índice do valor mais próximo
    return array[idx], idx                  # retorna (valor_mais_próximo, índice)

# ---------------- Cálculo de diferença entre janelas ----------------
if find_diff == True:
    # Janela 1
    startime1, startindex1 = find_nearest_index(time, time1[0])
    endtime1,   endindex1   = find_nearest_index(time, time1[1])
    d1  = d[startindex1:endindex1]                 # fatia do deslocamento bruto
    av1 = np.average(d1)                           # média do deslocamento na janela 1 (µm)
    endindex1 = endindex1                          # (resto de lógica antiga; sem efeito)
    std1 = np.std(av[startindex1:endindex1])       # desvio padrão do SINAL FILTRADO nessa janela

    # Janela 2
    startime2, startindex2 = find_nearest_index(time, time2[0])
    endtime2,   endindex2   = find_nearest_index(time, time2[1])
    d2  = d[startindex2:endindex2]
    av2 = np.average(d2)                           # média na janela 2 (µm)
    endindex2 = endindex2
    std2 = np.std(av[startindex2:endindex2])       # desvio padrão do filtrado na janela 2

    # Diferença absoluta de médias (µm)
    diff = abs(av1 - av2)
    print(f'Displacement={diff:.5f}µm')

    # Combinação quadrática dos desvios padrão (não é SEM; é RSS dos stds)
    disp_std = math.sqrt((std1**2) + (std2**2))

# ---------------- (COMENTADO) envelopes de média ± desvio, se houvesse 'w' e 'av' por janela ----------------
'''
Dplus = []
for i in range(len(d)-w):
    Dplus.append(av[i] + std[i])

Dminus = []
for i in range(len(d)-w):
    Dminus.append(av[i] - std[i])
'''

# ---------------- Plot ----------------
fig, ax = plt.subplots()
ax.plot(time, d, linewidth=0.5)  # série bruta
# ax.plot(time[int(w/2):-int(w/2)], av, label=f'Average over {w} points')   # (COMENTADO)
# ax.plot(time, av, label=f'Average over {w} points')                        # (COMENTADO)
ax.plot(time, av, label=f'Average Butterwothfliter : order={order} , cutoff frequency={cutoff_freq}Hz')
# ax.plot(time[int(w/2):-int(w/2)], Dplus, 'y--', ...)                       # (COMENTADO)
# ax.plot(time[int(w/2):-int(w/2)], Dminus, 'y--', ...)                      # (COMENTADO)

# Linhas horizontais de média e ±desvio nas janelas selecionadas
if find_diff == True:
    ax.plot([startime1, endtime1], [av1, av1], 'k--', label=f'Average between {time1[0]} and {time1[1]}s = {av1:.5f}µm')
    ax.plot([startime1, endtime1], [av1+std1, av1+std1], 'r--', label=f'Standard Deviation of average between {time1[0]} and {time1[1]}s = {std1}µm')
    ax.plot([startime1, endtime1], [av1-std1, av1-std1], 'r--')

    ax.plot([startime2, endtime2], [av2, av2], 'k--', label=f'Average between {time2[0]} and {time2[1]}s = {av2:.5f}µm')
    ax.plot([startime2, endtime2], [av2+std2, av2+std2], 'r--', label=f'Standard Deviation of average between {time2[0]} and {time2[1]}s = {std2}µm')
    ax.plot([startime2, endtime2], [av2-std2, av2-std2], 'r--')

    # “barrinha” vertical no fim do eixo x mostrando a diferença e o desvio combinado
    ax.plot([time[-1], time[-1]], [av1, av2], linewidth=5.0, label=f'Displacement = {diff}µm ; Standard deviation={disp_std}µm')

ax.set(xlabel='Time (s)', ylabel='d (µm)')
ax.set_title('Displacement for Masse=736,7mg ; l=5,52mm ; L=367,5mm ; Feq=108,55µN')
ax.grid()
plt.legend()
plt.show()