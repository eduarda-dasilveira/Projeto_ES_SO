import matplotlib.pyplot as plt
from math import ceil


def rr(listas):
    """
    Função principal que executa o algoritmo Round Robin (RR) para várias listas.

    Args:
        listas (list): Lista de listas a serem ordenadas.

    Returns:
        tuple: Contém os tempos de turnaround, o quantum calculado, o turnaround médio final e o gráfico de Gantt.
    """
    n = len(listas)  # Número de listas
    tmpEnt = [0] * n  # Tempo de entrada (inicializado como 0)
    tmpExe = [len(lista) for lista in listas]  # Tempo de execução baseado no comprimento da lista
    quantum_calculado = ceil(sum(tmpExe) / n)  # Quantum calculado como a média do tempo de execução

    turnaround_times = []  # Lista para armazenar os tempos de turnaround
    gantt_chart = []  # Lista para armazenar os dados do gráfico de Gantt

    # Calcula o tempo de turnaround para cada quantum de 1 até o quantum calculado
    for quantum in range(1, quantum_calculado + 1):
        turnaround_time, gantt = run_rr_with_quantum(listas, quantum, tmpEnt, tmpExe, n)
        turnaround_times.append((quantum, turnaround_time))  # Armazena o tempo de turnaround
        gantt_chart.append((quantum, gantt))  # Armazena os dados do gráfico de Gantt

    # Plota o gráfico de Gantt para o último quantum
    plot_gantt_chart(gantt_chart[-1][1], n)  # Plota o gráfico de Gantt correspondente ao último quantum

    plot_turnaround_times(turnaround_times)  # Plota o gráfico de turnaround

    return turnaround_times, quantum_calculado, turnaround_times[-1][1]  # Retorna os resultados


def run_rr_with_quantum(listas, quantum, tmpEnt, tmpExe, n):
    """
    Executa o algoritmo Round Robin para um quantum específico.

    Args:
        listas (list): Lista de listas a serem ordenadas.
        quantum (int): Quantum a ser utilizado.
        tmpEnt (list): Lista de tempos de entrada.
        tmpExe (list): Lista de tempos de execução.
        n (int): Número de listas.

    Returns:
        tuple: O tempo de turnaround médio e os dados do gráfico de Gantt.
    """
    relogio = 0  # Inicializa o relógio
    processados = [0] * n  # Processados mantém o controle do tempo processado de cada lista
    entraram = [0] * n  # Controla se a lista já entrou na fila
    fila = []  # Fila de processos prontos para execução
    tempos_finalizacao = [0] * n  # Armazena os tempos de finalização de cada lista
    soma_tempos = sum(tmpExe)  # Soma total dos tempos de execução
    fatias_tempo = [(tempo / soma_tempos) * quantum for tempo in tmpExe]  # Cálculo das fatias de tempo
    gantt_chart = []  # Lista para armazenar os dados do gráfico de Gantt

    def entra():
        """
        Função interna para adicionar processos prontos à fila.
        """
        processos_prontos = [(i, tmpEnt[i]) for i in range(n) if
                             tmpEnt[i] <= relogio and entraram[i] == 0 and tmpExe[i] > 0]
        processos_prontos.sort(key=lambda x: x[1])  # Ordena os processos prontos pelo tempo de entrada

        for x, _ in processos_prontos:
            entraram[x] = 1  # Marca como já entrou
            fila.append(x)  # Adiciona à fila

    while True:
        entra()  # Atualiza a fila de processos prontos
        if not fila:  # Se não há processos na fila
            if all([p == t for p, t in zip(processados, tmpExe)]):  # Verifica se todos os processos foram completados
                break
            relogio += 1  # Avança o relógio se a fila estiver vazia
            continue

        processo = fila.pop(0)  # Remove o primeiro processo da fila
        falta = tmpExe[processo] - processados[processo]  # Tempo restante para o processo
        start_time = relogio  # Tempo de início da execução do processo
        quantum_processo = ceil(fatias_tempo[processo])  # Calcula o quantum para o processo

        if falta > quantum_processo:  # Se o tempo restante é maior que o quantum
            relogio += quantum_processo  # Avança o relógio
            processados[processo] += quantum_processo  # Atualiza o tempo processado
            gantt_chart.append((processo + 1, start_time, relogio))  # Adiciona ao gráfico de Gantt
            entra()  # Atualiza a fila
            fila.append(processo)  # Re-adiciona o processo à fila
        elif falta <= quantum_processo and falta > 0:  # Se o processo pode ser completado
            relogio += falta  # Avança o relógio pelo tempo restante
            processados[processo] += falta  # Atualiza o tempo processado
            tempos_finalizacao[processo] = relogio  # Marca o tempo de finalização
            gantt_chart.append((processo + 1, start_time, relogio))  # Adiciona ao gráfico de Gantt
            entra()  # Atualiza a fila

    # Calcula o tempo médio de turnaround
    turnaround_medio_final = sum([tempos_finalizacao[i] - tmpEnt[i] for i in range(n) if tempos_finalizacao[i] > 0]) / n
    return round(turnaround_medio_final, 2), gantt_chart  # Retorna o turnaround médio e o gráfico de Gantt


def plot_gantt_chart(gantt_chart, n):
    """
    Plota o gráfico de Gantt com os dados fornecidos.

    Args:
        gantt_chart (list): Dados do gráfico de Gantt.
        n (int): Número de listas.
    """
    fig, gnt = plt.subplots()
    gnt.set_xlabel('Tempo')
    gnt.set_ylabel('Processos')

    yticks = [f'Lista {i + 1}' for i in range(n)]  # Rótulos do eixo y
    gnt.set_yticks(range(1, n + 1))  # Define os ticks do eixo y
    gnt.set_yticklabels(yticks)  # Define os rótulos dos ticks
    gnt.grid(True)  # Adiciona grid

    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta', 'yellow', 'brown', 'grey']
    color_map = {i + 1: colors[i % len(colors)] for i in range(n)}  # Mapeia cores para processos

    # Plota as barras do gráfico de Gantt
    for processo, start, end in gantt_chart:
        gnt.barh(processo, end - start, left=start, height=0.4, align='center', color=color_map[processo])

    max_time = max(end for _, _, end in gantt_chart)  # Tempo máximo do gráfico
    gnt.set_xticks(range(0, int(max_time) + 1, 5))  # Define os ticks do eixo x

    plt.show()  # Exibe o gráfico


def plot_turnaround_times(turnaround_times):
    """
    Plota o gráfico da variação do tempo de turnaround em relação ao quantum.

    Args:
        turnaround_times (list): Lista com os tempos de turnaround.
    """
    quantums = [t[0] for t in turnaround_times]  # Extraí os quantums
    turnarounds = [t[1] for t in turnaround_times]  # Extraí os turnarounds

    plt.figure()
    plt.plot(quantums, turnarounds, marker='o')  # Plota o gráfico
    plt.xlabel('Quantum')  # Rótulo do eixo x
    plt.ylabel('Turnaround Médio')  # Rótulo do eixo y
    plt.title('Variação do Turnaround Médio com o Quantum')  # Título do gráfico
    plt.grid(True)  # Adiciona grid
    plt.show()  # Exibe o gráfico


def bubble_sort(items):
    """
    Função que ordena uma lista usando o algoritmo Bubble Sort.

    Args:
        items (list): Lista a ser ordenada.

    Returns:
        list: Lista ordenada.
    """
    had_swap = True  # Indica se houve troca
    while had_swap:
        had_swap = False  # Reinicializa a variável
        for i in range(len(items) - 1):  # Itera sobre os itens
            if items[i] > items[i + 1]:  # Se o item atual é maior que o próximo
                swap(items, i)  # Realiza a troca
                had_swap = True  # Indica que houve troca
    return items  # Retorna a lista ordenada


def swap(items, index):
    """
    Realiza a troca de dois elementos em uma lista.

    Args:
        items (list): Lista onde a troca será realizada.
        index (int): Índice do primeiro elemento a ser trocado.
    """
    items[index], items[index + 1] = items[index + 1], items[index]  # Troca os itens


if __name__ == '__main__':
    # Código que executa a parte principal do programa
    num_listas = int(input("Quantas listas deseja ordenar? "))  # Solicita o número de listas

    listas = []  # Inicializa a lista de listas
    for i in range(num_listas):
        user_input = input(f"Digite a lista {i + 1} de números separados por espaço: ")  # Solicita a lista ao usuário
        lista = list(map(int, user_input.split()))  # Converte a entrada em uma lista de inteiros
        listas.append(lista)  # Adiciona a lista à lista de listas

    # Executa o algoritmo Round Robin e obtém os resultados
    turnaround_times, quantum_calculado, turnaround_medio_final = rr(listas)

    print(f"Quantum gerado: {quantum_calculado}")  # Exibe o quantum gerado
    print(f"Turnaround médio final: {turnaround_medio_final:.2f}")  # Exibe o turnaround médio final

    # Ordena e exibe cada lista
    for i, lista in enumerate(listas):
        sorted_lista = bubble_sort(lista)  # Ordena a lista
        print(f"Lista {i + 1} ordenada:", sorted_lista)  # Exibe a lista ordenada
