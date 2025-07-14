import os
import random
import pandas as pd
import numpy as np

from datetime import datetime, timedelta

def generate_cielo_dataset(
    num_chamados,
    data_inicio_str,
    data_fim_str,
    local_ofensor,
    servico_deficiente,
    output_dir,
    output_filename
):
    """
    Gera um dataset sintético de chamados logísticos da Cielo, simulando cenários específicos.

    Args:
        num_chamados (int): Número total de chamados a gerar.
        data_inicio_str (str): Data de início da simulação no formato 'dd/mm/aaaa'.
        data_fim_str (str): Data de fim da simulação no formato 'dd/mm/aaaa'.
        local_ofensor (str): Local simulado com pior desempenho.
        servico_deficiente (str): Serviço simulado com pior desempenho.
        output_dir (str): Diretório para salvar o arquivo CSV.
        output_filename (str): Nome do arquivo CSV de saída.
    """
    # Converte strings de data para objetos datetime
    data_inicio_simulacao = datetime.strptime(data_inicio_str, '%d/%m/%Y')
    data_fim_simulacao = datetime.strptime(data_fim_str, '%d/%m/%Y')

    # Listas de valores para geração
    BAIRROS_SP = [
        'Pinheiros', 'Moema', 'Jardins', 'Vila Madalena', 'Lapa', 'Santo Amaro',
        'Itaim Bibi', 'Barra Funda', 'Tatuapé', 'Guarulhos', 'Osasco'
    ]
    SERVICOS = ['Instalação', 'Manutenção']
    STATUS = ['Atendido', 'Cancelado']
    MOTIVOS_CANCELAMENTO = [
        'Cliente ausente', 'Solicitação do cliente', 'Problema técnico',
        'Equipamento indisponível', 'Endereço errado'
    ]

    # Parâmetros de simulação para cenários específicos
    PROB_CANCELAMENTO_OFENSOR = 0.35
    DESVIO_TEMPO_ATENDIMENTO_OFENSOR = 1.0
    PROB_PRAZO_LIMITE_EXCEDIDO_OFENSOR = 0.40
    MOTIVO_CANCELAMENTO_PRINCIPAL_OFENSOR = 'Problema técnico'

    PROB_CANCELAMENTO_SERVICO_DEFICIENTE = 0.30
    DESVIO_TEMPO_ATENDIMENTO_SERVICO_DEFICIENTE = 0.5
    PROB_PRAZO_LIMITE_EXCEDIDO_SERVICO_DEFICIENTE = 0.35

    PROB_CANCELAMENTO_PADRAO = 0.15
    DESVIO_TEMPO_ATENDIMENTO_PADRAO = 0.0
    PROB_PRAZO_LIMITE_EXCEDIDO_PADRAO = 0.20
    PRAZO_HORAS_MEDIO_PADRAO = 48
    PRAZO_HORAS_DESVIO_PADRAO = 24

    # Dados de benchmarking
    PRAZO_MAXIMO_CONCORRENCIA_DIAS = 2.0
    EXPECTATIVA_CLIENTE_DIAS = 1.0

    # Geração dos dados
    data = []
    dias_simulacao = (data_fim_simulacao - data_inicio_simulacao).days

    for i in range(num_chamados):
        data_abertura = data_inicio_simulacao + timedelta(days=random.randint(0, dias_simulacao))
        local = random.choice(BAIRROS_SP)
        servico = random.choice(SERVICOS)

        # Define parâmetros baseados nos cenários de ofensores
        prob_cancelamento = PROB_CANCELAMENTO_PADRAO
        desvio_tempo_atendimento = DESVIO_TEMPO_ATENDIMENTO_PADRAO
        prob_prazo_limite_excedido = PROB_PRAZO_LIMITE_EXCEDIDO_PADRAO
        motivo_cancelamento_choices = list(MOTIVOS_CANCELAMENTO)
        motivo_cancelamento_weights = [1 / len(MOTIVOS_CANCELAMENTO)] * len(MOTIVOS_CANCELAMENTO)

        if local == local_ofensor:
            prob_cancelamento = PROB_CANCELAMENTO_OFENSOR
            desvio_tempo_atendimento += DESVIO_TEMPO_ATENDIMENTO_OFENSOR
            prob_prazo_limite_excedido = PROB_PRAZO_LIMITE_EXCEDIDO_OFENSOR
            if MOTIVO_CANCELAMENTO_PRINCIPAL_OFENSOR in motivo_cancelamento_choices:
                idx = motivo_cancelamento_choices.index(MOTIVO_CANCELAMENTO_PRINCIPAL_OFENSOR)
                principal_weight = 0.40
                remaining_weight = 1.0 - principal_weight
                num_other_motives = len(MOTIVOS_CANCELAMENTO) - 1
                other_motive_weight = remaining_weight / num_other_motives if num_other_motives > 0 else 0
                new_weights = [other_motive_weight] * len(MOTIVOS_CANCELAMENTO)
                new_weights[idx] = principal_weight
                motivo_cancelamento_weights = new_weights

        if servico == servico_deficiente:
            prob_cancelamento = max(prob_cancelamento, PROB_CANCELAMENTO_SERVICO_DEFICIENTE)
            desvio_tempo_atendimento += DESVIO_TEMPO_ATENDIMENTO_SERVICO_DEFICIENTE
            prob_prazo_limite_excedido = max(prob_prazo_limite_excedido, PROB_PRAZO_LIMITE_EXCEDIDO_SERVICO_DEFICIENTE)

        status = 'Cancelado' if random.random() < prob_cancelamento else 'Atendido'
        motivo_cancelamento = None
        if status == 'Cancelado':
            motivo_cancelamento = random.choices(motivo_cancelamento_choices, weights=motivo_cancelamento_weights, k=1)[0]

        prazo_horas = max(0, int(np.random.normal(PRAZO_HORAS_MEDIO_PADRAO, PRAZO_HORAS_DESVIO_PADRAO)))
        data_limite_atendimento = data_abertura + timedelta(hours=prazo_horas)

        tempo_atendimento_dias_base = max(0, np.random.normal(2.0, 1.0) + desvio_tempo_atendimento)

        if status == 'Cancelado':
            data_encerramento = data_abertura + timedelta(days=random.uniform(0, 1.0))
        else: # Atendido
            data_encerramento = data_abertura + timedelta(days=tempo_atendimento_dias_base)
            if random.random() < prob_prazo_limite_excedido:
                data_encerramento = max(data_encerramento, data_limite_atendimento + timedelta(days=random.uniform(0.5, 2)))
            if data_encerramento < data_abertura:
                data_encerramento = data_abertura + timedelta(hours=1)

        entrega = 'Sim' if status == 'Atendido' else 'Não'

        data.append([
            local, servico, status, motivo_cancelamento,
            data_abertura, data_encerramento, data_limite_atendimento,
            prazo_horas, entrega, PRAZO_MAXIMO_CONCORRENCIA_DIAS, EXPECTATIVA_CLIENTE_DIAS
        ])

    df = pd.DataFrame(data, columns=[
        'LOCAL', 'SERVICO', 'STATUS', 'MOTIVO_CANCELAMENTO',
        'DATA_ABERTURA', 'DATA_ENCERRAMENTO', 'DATA_LIMITE_ATENDIMENTO',
        'PRAZO_HORAS', 'ENTREGA', 'PRAZO_MAXIMO_CONCORRENCIA_DIAS', 'EXPECTATIVA_CLIENTE_DIAS'
    ])

    output_path = f'{output_dir}/{output_filename}'
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Dataset de {num_chamados} chamados gerado com sucesso em '{output_path}'")
    print(f"Período de simulação: {data_inicio_simulacao.strftime('%d/%m/%Y')} a {data_fim_simulacao.strftime('%d/%m/%Y')}")
    print("\nPrimeiras 5 linhas do DataFrame:")
    print(df.head())
    print("\nInformações do DataFrame:")
    df.info()

if __name__ == "__main__":
    # Configurações globais para execução direta
    NUM_CHAMADOS_GLOBAL = 100000
    DATA_INICIO_SIMULACAO_GLOBAL_STR = '01/01/2025'
    DATA_FIM_SIMULACAO_GLOBAL_STR = '30/06/2025'
    LOCAL_OFENSOR_GLOBAL = 'Guarulhos'
    SERVICO_DEFICIENTE_GLOBAL = 'Manutenção'
    OUTPUT_DIR_GLOBAL = 'input'
    OUTPUT_FILENAME_GLOBAL = 'dataset_cielo.csv'

    # Chama a função principal de geração de dataset
    generate_cielo_dataset(
        num_chamados=NUM_CHAMADOS_GLOBAL,
        data_inicio_str=DATA_INICIO_SIMULACAO_GLOBAL_STR,
        data_fim_str=DATA_FIM_SIMULACAO_GLOBAL_STR,
        local_ofensor=LOCAL_OFENSOR_GLOBAL,
        servico_deficiente=SERVICO_DEFICIENTE_GLOBAL,
        output_dir=OUTPUT_DIR_GLOBAL,
        output_filename=OUTPUT_FILENAME_GLOBAL
    )
