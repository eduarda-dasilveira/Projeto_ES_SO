import matplotlib.pyplot as plt

def rr(listas, quantum):
    n = len(listas)
    tmpEnt = [0] * n  # Tempos de chegada, inicializados como 0
    tmpExe = [len(lista) for lista in listas]  # Tempos de execução (tamanhos das listas)

    relogio = 0  # Tempo atual
    processados = [0] * n  # Tempo processado de cada lista
    fila = list(range(n))  # Fila de processos (inicialmente todos)
    tempos_finalizacao = [0] * n  # Tempos de finalização de cada lista
    gantt_chart = []

    turnaround_times = []

    while fila:
        processo = fila.pop(0)  # Pega o próximo processo da fila
        falta = tmpExe[processo] - processados[processo]  # Tempo restante para o processo
        start_time = relogio

        if falta > quantum:
            relogio += quantum
            processados[processo] += quantum
            gantt_chart.append((processo + 1, start_time, relogio))
            fila.append(processo)  # Reinsere o processo na fila
        elif falta > 0:
            relogio += falta
            processados[processo] += falta
            tempos_finalizacao[processo] = relogio
            gantt_chart.append((processo + 1, start_time, relogio))

        turnarounds_atuais = [tempos_finalizacao[i] - tmpEnt[i] for i in range(n) if tempos_finalizacao[i] > 0]
        if turnarounds_atuais:
            turnaround_times.append((relogio, sum(turnarounds_atuais) / len(turnarounds_atuais)))

    turnaround_medio_final = sum([tempos_finalizacao[i] - tmpEnt[i] for i in range(n)]) / n
    turnaround_medio_final = round(turnaround_medio_final, 2)

    return turnaround_times, turnaround_medio_final, gantt_chart

def plot_gantt_chart(gantt_chart, n):
    fig, gnt = plt.subplots()
    gnt.set_xlabel('Tempo')
    gnt.set_ylabel('Processos')

    yticks = [f'Lista {i+1}' for i in range(n)]
    gnt.set_yticks(range(1, n + 1))
    gnt.set_yticklabels(yticks)
    gnt.grid(True)

    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta', 'yellow', 'brown', 'grey']
    color_map = {i + 1: colors[i % len(colors)] for i in range(n)}

    for processo, start, end in gantt_chart:
        gnt.barh(processo, end - start, left=start, height=0.4, align='center', color=color_map[processo])

    max_time = max(end for _, _, end in gantt_chart)
    gnt.set_xticks(range(0, int(max_time) + 1, 5))

    plt.show()

def plot_turnaround_times(turnaround_times, quantum_range):
    quanta = list(range(1, quantum_range + 1))
    turnarounds = [turnaround_times[q - 1] for q in quanta]

    plt.figure()
    plt.plot(quanta, turnarounds, marker='o', color='skyblue')
    plt.xlabel('Tempo de quantum')
    plt.ylabel('Tempo médio de turnaround')
    plt.title('Tempo de turnaround varia com o quantum de tempo')


    plt.grid(True)
    plt.show()

def bubble_sort(items):
    had_swap = True
    while had_swap:
        had_swap = False
        for i in range(len(items) - 1):
            if items[i] > items[i + 1]:
                swap(items, i)
                had_swap = True
    return items

def swap(items, index):
    items[index], items[index + 1] = items[index + 1], items[index]

if __name__ == '__main__':
    num_listas = int(input("Quantas listas deseja ordenar? "))

    listas = []
    processos = []
    for i in range(num_listas):
        user_input = input(f"Digite a lista {i+1} de números separados por espaço: ")
        lista = list(map(int, user_input.split()))
        listas.append(lista)
        processos.append(len(lista))  # Guardando o tamanho da lista como tempo de execução

    quantum = int(input("Digite o valor do quantum: "))

    # Calcula os tempos de turnaround para diferentes valores de quantum
    turnaround_times = []
    for q in range(1, quantum + 1):
        _, turnaround_medio, _ = rr(listas, q)
        turnaround_times.append(turnaround_medio)

    turnaround_times_usuario, turnaround_medio_final_usuario, gantt_chart_usuario = rr(listas, quantum)
    print(f"Turnaround médio final para o quantum {quantum}: {turnaround_medio_final_usuario:.2f}")

    for i, lista in enumerate(listas):
        sorted_lista = bubble_sort(lista)
        print(f"Lista {i+1} ordenada:", sorted_lista)

    plot_gantt_chart(gantt_chart_usuario, num_listas)
    plot_turnaround_times(turnaround_times, quantum)
