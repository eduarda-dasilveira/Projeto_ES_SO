def rr():
    entradas = list(tmpEnt)  # A LISTA DE ENTRADAS PARA UMA NOVA LISTA, QUE SERÁ ORDENADA
    tempos = list(tmpExe)  # MESMA IDEIA DE CIMA
    relogio = 0
    processados = [0] * n  # LISTA ONDE A CADA EXECUÇÃO IRA SE INCREMENTAR O TEMPO QUE FOI EXECUTADO
    entraram = [0] * n  # LISTA DE 0/1 PARA SABER QUAIS PROCESSOS JA ENTRAM
    fila = []  # UMA FILA, QUE IRÁ DETERMINAR QUAIS OS PROXIMOS PROCESSOS IRÃO EXECUTAR
    tempos_finalizacao = [0] * n  # Armazena o tempo de finalização de cada processo
    quantum = float(input("Insira o valor do quantum: "))

    def entra():
        for x in range(n):  # ADICIONA OS TEMPOS QUE NÃO ENTRARAM E MENORES OU IGUAL AO RELOGIO NA FILA
            if entradas[x] <= relogio and entraram[x] == 0:
                entraram[x] = 1  # OS PROCESSOS QUE JÁ ENTRARAM, RECEBEM 1, ASSIM SÓ ENTRAM NOVAMENTE NA FILA EM CASO DE PREEPÇÃO
                fila.append(x)  # O PROCESSO É ADICIONADO AO FIM DA FILA

    while True:
        entra()
        if not fila:  # Se a fila estiver vazia, verificar se todos os processos foram concluídos
            if all([p == t for p, t in zip(processados, tempos)]):
                break
            relogio += 1  # Incrementar o relógio até que um novo processo entre na fila
            continue

        processo = fila.pop(0)
        falta = tempos[processo] - processados[processo]  # VARIÁVEL FALTA RECEBE O TEMPO DO PROCESSO - O QUE JÁ FOI PROCESSADO
        if falta > quantum:  # SE FALTA MAIS QUE O QUANTUM ENTRA NO BLOCO
            relogio += quantum  # RELOGIO INCREMENTA O QUANTUM, POIS IRÁ EXECUTAR TODO O TEMPO DO QUANTUM
            processados[processo] += quantum  # INCREMENTA EM UM QUANTUM O QUE JÁ FOI PROCESSADO DO PROCESSO ATUAL
            fila.append(processo)  # COMO O PROCESSO NÃO FOI EXECUTADO TOTALMENTE, ELE VOLTA PARA O FIM DA FILA DE EXECUÇÃO
            print(f"Processo {processo + 1} executou por {quantum} unidades; tempo restante: {tempos[processo] - processados[processo]}")
        elif falta <= quantum and falta > 0:  # NESSE CASO VERIFICAMOS SE FALTA ALGUM TEMPO ENTRE 0 E O QUANTUM A SER EXECUTADO
            relogio += falta  # INCREMENTA O RELÓGIO O TEMPO QUE FALTA
            processados[processo] += falta  # INCREMENTA O QUE FALTA AO QUE JÁ FOI PROCESSADO DO PROCESSO ATUAL
            tempos_finalizacao[processo] = relogio  # ARMAZENA O TEMPO DE FINALIZAÇÃO DO PROCESSO
            print(f"Processo {processo + 1} executou por {falta} unidades; completou no tempo {relogio}")
        relogio += 1  # Incrementa o relógio para a sobrecarga de troca de contexto

    soma_turnaround = sum([tempos_finalizacao[i] - entradas[i] for i in range(n)])
    return float(soma_turnaround / n)  # RETORNA A MEDIA DOS TURNAROUND


# LÊ A QUANTIDADE DE PROCESSOS E CRIA AS LISTAS DE TEMPO DE EXECUÇÃO E TEMPO DE ENTRADA PARA CADA PROCESSO
n = int(input("Informe o numero de processos: "))
tmpExe = []
tmpEnt = []

# LÊ OS TEMPOS DE EXECUÇÃO E DE ENTRADA PARA CADA PROCESSO
for x in range(1, n + 1):
    print("Tempo de entrada do processo ", x, ": ")
    tmpEnt.append(float(input()))
    print("Tempo de execução do processo ", x, ": ")
    tmpExe.append(float(input()))

turnaround_medio = rr()
print("TURNAROUND MÉDIO:", turnaround_medio)
