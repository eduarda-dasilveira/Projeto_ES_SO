import matplotlib.pyplot as plt

def rr(listas, quantum):
    # Número de processos
    n = len(listas)
    # Tempos de chegada, inicializados como 0
    tmpEnt = [0] * n
    # Tempos de execução (tamanhos das listas)
    tmpExe = [len(lista) for lista in listas]

    # Tempo atual
    relogio = 0
    # Tempo processado de cada lista
    processados = [0] * n
    # Fila de processos (inicialmente todos)
    fila = list(range(n))
    # Tempos de finalização de cada lista
    tempos_finalizacao = [0] * n
    # Lista para armazenar os intervalos de execução no gráfico de Gantt
    gantt_chart = []

    # Lista para armazenar os tempos de turnaround ao longo do tempo
    turnaround_times = []

    while fila:
        # Pega o próximo processo da fila
        processo = fila.pop(0)
        # Tempo restante para o processo
        falta = tmpExe[processo] - processados[processo]
        start_time = relogio

        if falta > quantum:
            # Atualiza o relógio e o tempo processado para o quantum
            relogio += quantum
            processados[processo] += quantum
            # Adiciona o intervalo de execução ao gráfico de Gantt
            gantt_chart.append((processo + 1, start_time, relogio))
            # Reinsere o processo na fila
            fila.append(processo)
        elif falta > 0:
            # Atualiza o relógio e o tempo processado para o tempo restante
            relogio += falta
            processados[processo] += falta
            # Marca o tempo de finalização do processo
            tempos_finalizacao[processo] = relogio
            # Adiciona o intervalo de execução ao gráfico de Gantt
            gantt_chart.append((processo + 1, start_time, relogio))

        # Calcula os tempos de turnaround atuais
        turnarounds_atuais = [tempos_finalizacao[i] - tmpEnt[i] for i in range(n) if tempos_finalizacao[i] > 0]
        if turnarounds_atuais:
            # Adiciona a média dos tempos de turnaround ao longo do tempo
            turnaround_times.append((relogio, sum(turnarounds_atuais) / len(turnarounds_atuais)))

    # Calcula o turnaround médio final
    turnaround_medio_final = sum([tempos_finalizacao[i] - tmpEnt[i] for i in range(n)]) / n
    turnaround_medio_final = round(turnaround_medio_final, 2)

    return turnaround_times, turnaround_medio_final, gantt_chart

def plot_gantt_chart(gantt_chart, n):
    # Cria uma figura e um gráfico de Gantt
    fig, gnt = plt.subplots()
    gnt.set_xlabel('Tempo')
    gnt.set_ylabel('Processos')

    # Define os rótulos dos processos
    yticks = [f'Lista {i+1}' for i in range(n)]
    gnt.set_yticks(range(1, n + 1))
    gnt.set_yticklabels(yticks)
    gnt.grid(True)

    # Cores para os processos no gráfico
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta', 'yellow', 'brown', 'grey']
    color_map = {i + 1: colors[i % len(colors)] for i in range(n)}

    # Adiciona os intervalos de execução ao gráfico de Gantt
    for processo, start, end in gantt_chart:
        gnt.barh(processo, end - start, left=start, height=0.4, align='center', color=color_map[processo])

    # Define os ticks do eixo X
    max_time = max(end for _, _, end in gantt_chart)
    gnt.set_xticks(range(0, int(max_time) + 1, 5))

    plt.show()

def plot_turnaround_times(turnaround_times, quantum_range):
    # Cria uma lista de tempos de quantum
    quanta = list(range(1, quantum_range + 1))
    turnarounds = [turnaround_times[q - 1] for q in quanta]

    # Plota o gráfico dos tempos de turnaround
    plt.figure()
    plt.plot(quanta, turnarounds, marker='o', color='skyblue')
    plt.xlabel('Tempo de quantum')
    plt.ylabel('Tempo médio de turnaround')
    plt.title('Tempo de turnaround varia com o quantum de tempo')

    plt.grid(True)
    plt.show()

def bubble_sort(items):
    had_swap = True
    # Loop até que não haja mais trocas
    while had_swap:
        had_swap = False
        # Varre a lista realizando trocas quando necessário
        for i in range(len(items) - 1):
            if items[i] > items[i + 1]:
                swap(items, i)
                had_swap = True
    return items

def swap(items, index):
    # Realiza a troca de dois elementos na lista
    items[index], items[index + 1] = items[index + 1], items[index]

if __name__ == '__main__':
    # Solicita ao usuário o número de listas
    num_listas = int(input("Quantas listas deseja ordenar? "))

    listas = []
    processos = []
    # Coleta as listas de números do usuário
    for i in range(num_listas):
        user_input = input(f"Digite a lista {i+1} de números separados por espaço: ")
        lista = list(map(int, user_input.split()))
        listas.append(lista)
        # Guarda o tamanho da lista como tempo de execução
        processos.append(len(lista))

    # Solicita ao usuário o valor do quantum
    quantum = int(input("Digite o valor do quantum: "))

    # Calcula os tempos de turnaround para diferentes valores de quantum
    turnaround_times = []
    for q in range(1, quantum + 1):
        _, turnaround_medio, _ = rr(listas, q)
        turnaround_times.append(turnaround_medio)

    # Executa o algoritmo RR com o quantum fornecido pelo usuário
    turnaround_times_usuario, turnaround_medio_final_usuario, gantt_chart_usuario = rr(listas, quantum)
    print(f"Turnaround médio final para o quantum {quantum}: {turnaround_medio_final_usuario:.2f}")

    # Ordena cada lista usando Bubble Sort
    for i, lista in enumerate(listas):
        sorted_lista = bubble_sort(lista)
        print(f"Lista {i+1} ordenada:", sorted_lista)

    # Plota o gráfico de Gantt
    plot_gantt_chart(gantt_chart_usuario, num_listas)
    # Plota os tempos de turnaround
    plot_turnaround_times(turnaround_times, quantum)
