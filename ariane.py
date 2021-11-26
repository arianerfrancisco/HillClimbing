import pandas as pd
import random

def resolve_instancia(arq_instancia, arq_solucao, arq_relatorio, qtd_iteracoes):
    relatorio = []
    matriz_de_tempo = []

    df = pd.read_csv(arq_instancia)  # FAZ A LEITURA DA INSTÂNCIA
    qtde_tarefas, qtde_maquinas = df["INSTANCE_SIZE"][0].split(";")  # ARMANEZA EM VARIÁVEIS= QTDE DE TAREFAS E MÁQUINAS

    copy_df = df["INSTANCE_SIZE"][2: int(qtde_tarefas) + 2]  # ARMAZENA OS PRÓXIMOS VALORES EM UM DATAFRAME copy_df,
    # NÃO INCLUINDO OS DADOS JÁ LIDOS
    matriz_auxiliar = [x.split(";") for x in
                       copy_df]  # PERCORRE copy_df PARA ARMAZENAR EM LISTAS OS TEMPOS DE OPERAÇÃO
    # POR CADA MÁQUINA DE CADA TAREFA
    for auxiliar in matriz_auxiliar:  # LAÇO QUE CONVERTE matriz_auxiliar PARA DADOS INTEIROS,
        # EXCLUINDO O INDICE DA TAREFA
        vetor_aux = []
        [vetor_aux.append(int(x)) for x in auxiliar]
        matriz_de_tempo.append(vetor_aux[1:])

    otimo_global_soma_tempo_medio_maquina = 9999999999
    otimo_global_matriz_sequencias_jobs = []

    relatorio.append([qtd_iteracoes])  # NA 1ª LINHA DO ARQ RELATÓRIO É GRAVADA A QUANTIDADE DE ITERAÇÕES REALIZADAS

    for iteracao in range(0, qtd_iteracoes):
        # CRIA-SE UMA LISTA COM TODAS AS TAREFAS DAS INSTÂNCIAS (1, 2, 3, ....) - ESTÁ SERÁ A SOLUÇÃO INICIAL
        solucao_I = [tarefa for tarefa in range(0, int(qtde_tarefas))]
        # EMBARALHA-SE OS ELEMENTOS (TAREFAS DESTA LISTA)
        random.shuffle(solucao_I)

        # CHAMA-SE O MÉTODO CALCULA:
        # UMA VEZ GERADA A SOLUÇÃO INICIAL COM OS ELEMENTOS EMBARALHADOS, ESTES PASSARÃO
        # A PARTIR DO PRIMEIRO ELEMENTO ATÉ O ÚLTIMO POR UM LAÇO FOR QUE ATRIBUIRÁ ESTAS TAREFAS
        # A MÁQUINAS FACTÍVEIS PARA ATENDIMENTO

        (otimo_local_matriz_sequencias_jobs, otimo_local_soma_tempo_medio_maquina,) = calcula(solucao_I,
                                                                                              matriz_de_tempo,
                                                                                              qtde_maquinas,
                                                                                              qtde_tarefas)
        # ENTÃO APLICANDO O MÉTODO CALCULA PARA A SOLUÇÃO INICIAL - SOLUÇÃO CANDIDATA- ATRIBUIREMOS COMO OTIMO LOCAL
        solucao_inicial_soma_tempo_medio_maquina = otimo_local_soma_tempo_medio_maquina
        # COM O INTUITO DE MELHORAR A SOLUÇÃO ENCOTRADA TENTA-SE MELHORAR ATRAVÉS
        # DO HILL CLIMBING FAREMOS UMA BUSCA LOCAL DE MELHORES SOLUÇÕES PARA ESTÁ QUE FOI ENCONTRADA
        vizinhos = gerar_vizinhos(solucao_I)
        # UMA VEZ GERADOS OS VIZINHOS ESTES SERÃO CONDICIONADOS AO MÉTODO CALCULA QUE FORAM AS DEVIDAS
        # ATRIBUIÇÕES DAS TAREFAS AS MÁQUINAS RESPEITANDO A RESTRIÇÃO  -1 DE ATENDIMENTO
        # E NOVAMENTE RETIRADO  O VALOR DA MÉDIA DE TEMPO DE FINALIZAÇÃO DAS TAREFAS
        for vizinho in vizinhos:
            (matriz_sequencias_jobs_vizinho, tempo_gasto_vizinho_soma_tempo_medio_maquina,) = calcula(vizinho,
                                                                                                      matriz_de_tempo,
                                                                                                      qtde_maquinas,
                                                                                                      qtde_tarefas)
            # DENTRE OS VIZINHOS É SELECIONADO A MELHOR SOLUÇÃO - SENDO ESTA UMA OTIMO LOCAL
            if (otimo_local_soma_tempo_medio_maquina > tempo_gasto_vizinho_soma_tempo_medio_maquina):
                otimo_local_soma_tempo_medio_maquina = (tempo_gasto_vizinho_soma_tempo_medio_maquina)
                otimo_local_matriz_sequencias_jobs = matriz_sequencias_jobs_vizinho
        # UMA VEZ ENCONTRADO O ÓTIMO LOCAL DENTRE OS VIZINHOS AVALIADOS, AVALIA-SE SE ESTE É A MELHOR SOLUÇÃO ENCONTRADA
        # ATÉ O MOMENTO. SE SIM, ESTÁ É A ÓTIMA GLOBAL.
        # CASO CONTRÁRIO - NADA SE ALTERA
        if otimo_global_soma_tempo_medio_maquina > otimo_local_soma_tempo_medio_maquina:
            otimo_global_soma_tempo_medio_maquina = otimo_local_soma_tempo_medio_maquina
            otimo_global_matriz_sequencias_jobs = otimo_local_matriz_sequencias_jobs

        relatorio.append([iteracao + 1, "{:.2f}".format(float(solucao_inicial_soma_tempo_medio_maquina)),
                          "{:.2f}".format(float(otimo_local_soma_tempo_medio_maquina)),
                          "{:.2f}".format(float(otimo_global_soma_tempo_medio_maquina)), ])

    otimo_global_matriz_sequencias_jobs.reverse()
    otimo_global_matriz_sequencias_jobs.append([otimo_global_soma_tempo_medio_maquina])
    otimo_global_matriz_sequencias_jobs.reverse()

    df_relatorio = pd.DataFrame(data=relatorio)
    df_relatorio.to_csv(arq_relatorio, index=False, sep=";", header=False)

    df_solucao = pd.DataFrame(data=otimo_global_matriz_sequencias_jobs)
    df_solucao = df_solucao.apply(lambda job: job + 1)
    df_solucao.to_csv(arq_solucao, index=False, header=False, sep=";")
    print(otimo_global_matriz_sequencias_jobs[0])

def gerar_vizinhos(solucao_inicial):
    todas_solucoes_temporarias = list()
    solucao_temporaria = solucao_inicial[:]  # FAZ UMA CÓPIA DA SOLUÇÃO INICIAL EM UMA VARIÁVEL TEMPORÁRIA
    quantidade_pontos = len(solucao_inicial) - 1  # O ÚLTIMO ELEMENTO NÃO TEM VIZINHO ADJACENTE
    for ponto_i in range(0, quantidade_pontos):
        # [10, 11, 2, 21, 22, 19, 6, 14, 16, 20, 13, 0, 5, 4, 23, 12, 24, 7, 17, 8, 18, 1, 9, 3, 15]
        # OS PONTOS VIZINHOS SÃO INVERTIDOS
        # [11, 10, 2, 21, 22, 19, 6, 14, 16, 20, 13, 0, 5, 4, 23, 12, 24, 7, 17, 8, 18, 1, 9, 3, 15]
        solucao_temporaria[ponto_i] = solucao_inicial[ponto_i + 1]
        solucao_temporaria[ponto_i + 1] = solucao_inicial[ponto_i]
        todas_solucoes_temporarias.append(solucao_temporaria)
        # O VIZINHO GERADO A PARTIR DA TROCA DOS PONTOS É ADICIONADO
        # COM OS DEMAIS VIZINHOS CRIADO DESSA SOLUÇÃO CANDIDATA
        solucao_temporaria.reverse()
        # ALÉM DE TROCAR OS PONTOS ADJACENTES DESTE VIZINHO - APLICA-SE REVERSE EM SEUS ELEMENTOS
        # OS PONTOS RECÉM TROCADOS SÃO JOGADOS PARA O FINAL
        # [15, 3, 9, 1, 18, 8, 17, 7, 24, 12, 23, 4, 5, 0, 13, 20, 16, 14, 6, 19, 22, 21, 2, 10, 11]
        todas_solucoes_temporarias.append(solucao_temporaria)
        # AQUI SERÁ ARMAZENADO TODOS OS VIZINHOS QUE FORAM  GERADOS A PARTIR DA SOLUÇÃO CANDIDATA
        solucao_temporaria.reverse()
        # CONSIDERANDO ESSE METODO gerar_vizinhos PARA UMA INSTÂNCIA DE 25 TAREFAS SERÃO GERADAS 50 VIZINHOS

    return todas_solucoes_temporarias

def calcula(solucao_I, matriz_de_tempo, qtde_maquinas, qtde_tarefas):
    # CRIA-SE ESTA MATRIZ VAZIA PARA RECEBER AS TAREFAS - CADA LINHA REFERE-SE A UMA MÁQUINA
    matriz_sequecias_jobs = []
    [matriz_sequecias_jobs.append([]) for x in range(0, int(qtde_maquinas))]

    # CRIA-SE ESTA MATRIZ VAZIA PARA RECEBER O TEMPO DE EXECUÇÃO DAS TAREFAS PELAS RESPECTIVAS MÁQUINAS
    matriz_de_tempos_respectivo_ao_sequencias = []
    [matriz_de_tempos_respectivo_ao_sequencias.append([]) for x in range(0, int(qtde_maquinas))]

    copy_solucao_I = solucao_I  # FAZ-SE UMA CÓPIA DA SOLUÇÃO INICIAL
    while copy_solucao_I != []:  # ENQUANTO copy_solucao_I CONTER ELEMENTOS A ITERAÇÃO IRÁ OCORRER
        vetor_auxiliar = []  # IRÁ RECEBER TODAS AS TAREFAS NÃO ATRIBUIDAS A MÁQUINAS
        for tarefa in copy_solucao_I:  # O ITERADOR PERCORRERÁ A SOLUÇÃO INICIAL PARA ATRIBUIR AS TAREFAS NAS MÁQUINAS
            ran_maquina = random.randint(0, int(qtde_maquinas) - 1)  # A ESCOLHA DA MÁQUINA É ALEATORIA
            if matriz_de_tempo[int(tarefa)][ran_maquina] != -1:
                # NO ENTANTO FICARÁ CONDICIONADA AO ATENDIMENTO DA RESTRIÇÃO
                # CASO A MÁQUINA SELECIONADA PARA A TAREFA NÃO CONTIVER -1 NA POSIÇÃO DA MATRIZ - ELA É ACEITA
                matriz_sequecias_jobs[ran_maquina].append(tarefa)  # ADICIONA A TAREFA NA LINHA DA MÁQUINA
                matriz_de_tempos_respectivo_ao_sequencias[ran_maquina].append(matriz_de_tempo[int(tarefa)][ran_maquina])
                # ADICIONA O TEMPOS DA TAREFAS NAS RESPECTIVAS MÁQUINAS
            else:
                # CASO A TAREFA NÃO POSSA SER ADICIONADA A MÁQUINA SELECIONADA -
                # A TAREFA SERÁ ADICIONADA EM: vetor_auxiliar
                vetor_auxiliar.append(tarefa)
        # APÓS REALIZADA TODAS AS ITERAÇÕES DE TAREFA/MÁQUINAS. O vetor_auxiliar QUE RECEBEU TODAS AS TAREFAS
        # QUE NÃO FORAM ATRIBUIDAS A NENHUMA MÁQUINA EM copy_solucao_I
        copy_solucao_I = vetor_auxiliar
        # ENQUANTO copy_solucao_I CONTIVER ELEMENTOS O WHILE NÃO PARARÁ SEU LOOP
        # ESTRATÉGIA PARA GARANTIR QUE NENHUMA TAREFA FIQUE SEM ATENDIMENTO
    total = 0
    # ESTE LOOP IRÁ CRIAR UMA MATRIZ DAS TAREFAS DE TEMPOS ACUMULADOS PARA CADA MÁQUINA
    for maquina in range(0, int(qtde_maquinas)):
        soma_dos_tempos = 0
        iteracao = 0
        # PARA CADA MÁQUINA = ADICIONA EM SEQUENCIA DE FORMA CUMULATIVA OS TEMPOS ANTERIORES COM OS NOVOS
        for job in matriz_de_tempos_respectivo_ao_sequencias[maquina]:
            soma_dos_tempos = soma_dos_tempos + job
            matriz_de_tempos_respectivo_ao_sequencias[maquina][iteracao] = soma_dos_tempos
            iteracao = iteracao + 1
        # UMA VEZ CONSTRUÍDA AS MATRIZES DE TEMPOS ACUMULADOS DE CADA MÁQUINA, ESTAS SÃO SOMADAS NUMA VARIÁVEL
        # ÚNICA total PARA QUE A MÉDIA DE TEMPO DE FINALIZAÇÃO SEJA CALCULADA
        total = total + sum(matriz_de_tempos_respectivo_ao_sequencias[maquina])
        # LOGO TEREMOS COMO RETORNO O SEQUENCIAMENTO DAS TAREFAS PELAS RESPECTIVAS MÁQUINA
        # E O VALOR DA MÉDIA DE TEMPO DE FINALIZAÇÃO SEJA CALCULADA
        # ESTE É VALOR  ALVO DO ALGORITMO - QUE BUSCA MINIMIZÁ-LO

    return matriz_sequecias_jobs, (total / int(qtde_tarefas))
resolve_instancia("Instancias/inst01.csv", "inst01_sol.csv", "inst01_relatorio.csv", 900)