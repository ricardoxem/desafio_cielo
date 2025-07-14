import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def analyze_cielo_data(filepath):
    """
    Realiza a análise exploratória dos dados de chamados da Cielo.
    """
    plt.style.use('seaborn-v0_8')

    # Carregar os dados
    try:
        df = pd.read_csv(filepath, sep=',',
                         parse_dates=['DATA_ABERTURA', 'DATA_ENCERRAMENTO', 'DATA_LIMITE_ATENDIMENTO'],
                         dayfirst=True)
        print("Dados carregados com sucesso!")
        print(f"Total de linhas no dataset: {len(df)}")
    except FileNotFoundError:
        print(f"Erro: O arquivo '{filepath}' não foi encontrado.")
        print("Certifique-se de que o script '01_gerar_arquivos_de_exemplos.py' foi executado e gerou o arquivo.")
        return

    # Resumo Geral do Dataset
    print(f"\n{'#' * 30}\n# Visão Geral do Dataset\n{'#' * 30}")
    print(df.head())
    print("\nInformações do DataFrame:")
    df.info()
    print("\nEstatísticas Descritivas:")
    print(df.describe(include='all'))
    print("\nValores Nulos por Coluna:")
    print(df.isnull().sum())

    # Análise da Distribuição por LOCAL
    print(f"\n{'#' * 30}\n# Análise por LOCAL\n{'#' * 30}")
    print("Contagem de chamados por LOCAL:")
    print(df['LOCAL'].value_counts())
    plt.figure(figsize=(12, 7))
    ax = sns.countplot(data=df, x='LOCAL', order=df['LOCAL'].value_counts().index, palette='viridis')
    plt.title('Chamados por Local de Atendimento')
    plt.xlabel('Local')
    plt.ylabel('Quantidade de Chamados')
    plt.xticks(rotation=45, ha='right')
    # Adiciona os valores nas barras
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.show()

    # Análise da Distribuição por SERVICO
    print(f"\n{'#' * 30}\n# Análise por SERVICO\n{'#' * 30}")
    print("Contagem de chamados por SERVICO:")
    print(df['SERVICO'].value_counts())
    plt.figure(figsize=(8, 6))
    ax = sns.countplot(data=df, x='SERVICO', order=df['SERVICO'].value_counts().index, palette='viridis')
    plt.title('Chamados por Tipo de Serviço')
    plt.xlabel('Serviço')
    plt.ylabel('Quantidade de Chamados')
    # Adiciona os valores nas barras
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.show()

    # Análise da Distribuição por STATUS
    print(f"\n{'#' * 30}\n# Análise por STATUS\n{'#' * 30}")
    print("Contagem de chamados por STATUS:")
    print(df['STATUS'].value_counts())
    plt.figure(figsize=(8, 6))
    ax = sns.countplot(data=df, x='STATUS', order=df['STATUS'].value_counts().index, palette='viridis')
    plt.title('Distribuição de Status dos Chamados')
    plt.xlabel('Status')
    plt.ylabel('Quantidade de Chamados')
    # Adiciona os valores nas barras
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.show()

    # Análise dos Motivos de Cancelamento
    print(f"\n{'#' * 30}\n# Análise de Motivos de Cancelamento\n{'#' * 30}")
    if 'MOTIVO_CANCELAMENTO' in df.columns:
        cancelados = df[df['STATUS'] == 'Cancelado'].copy()
        if not cancelados.empty:
            print("Contagem de motivos de cancelamento:")
            print(cancelados['MOTIVO_CANCELAMENTO'].value_counts())
            plt.figure(figsize=(10, 7))
            ax = sns.countplot(data=cancelados, y='MOTIVO_CANCELAMENTO',
                               order=cancelados['MOTIVO_CANCELAMENTO'].value_counts().index, palette='viridis')
            plt.title('Motivos de Cancelamento Mais Comuns')
            plt.xlabel('Quantidade de Chamados Cancelados')
            plt.ylabel('Motivo de Cancelamento')
            # Adiciona os valores nas barras
            for p in ax.patches:
                ax.annotate(f'{int(p.get_width())}', (p.get_width(), p.get_y() + p.get_height() / 2.),
                            ha='left', va='center', xytext=(5, 0), textcoords='offset points')
            plt.tight_layout()
            plt.show()
        else:
            print("Não há chamados com status 'Cancelado' para analisar motivos.")
    else:
        print("Coluna 'MOTIVO_CANCELAMENTO' não encontrada no dataset.")

    # Cálculo e Análise do Tempo de Atendimento
    print(f"\n{'#' * 30}\n# Análise do Tempo de Atendimento\n{'#' * 30}")
    df['TEMPO_ATENDIMENTO_DIAS'] = (df['DATA_ENCERRAMENTO'] - df['DATA_ABERTURA']).dt.days

    # Filtra chamados 'Atendido' para análise de tempo
    atendidos = df[df['STATUS'] == 'Atendido'].copy()
    if not atendidos.empty and 'TEMPO_ATENDIMENTO_DIAS' in atendidos.columns:
        print("Estatísticas do TEMPO_ATENDIMENTO_DIAS (Chamados 'Atendido'):")
        tempo_atendimento_media = atendidos['TEMPO_ATENDIMENTO_DIAS'].dropna().mean()
        print(atendidos['TEMPO_ATENDIMENTO_DIAS'].dropna().describe())
        print(f"Média do Tempo de Atendimento: {tempo_atendimento_media:.2f} dias")

        plt.figure(figsize=(10, 6))
        # Removido 'kde=True' para não gerar a linha azul
        ax = sns.histplot(atendidos['TEMPO_ATENDIMENTO_DIAS'].dropna(), bins=20, palette='viridis')
        plt.title('Distribuição do Tempo de Atendimento (Dias) para Chamados Atendidos')
        plt.xlabel('Tempo de Atendimento (Dias)')
        plt.ylabel('Frequência')
        plt.tight_layout()

        # Adiciona linha da média
        plt.axvline(tempo_atendimento_media, color='red', linestyle='--',
                    label=f'Média: {tempo_atendimento_media:.2f} dias')
        plt.legend()

        # Adiciona os valores nas barras do histograma
        for p in ax.patches:
            height = p.get_height()
            if height > 0:  # Anota apenas barras com altura > 0
                ax.annotate(f'{int(height)}', (p.get_x() + p.get_width() / 2., height),
                            ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=8)
        plt.show()
    else:
        print("Não há chamados 'Atendido' ou a coluna 'TEMPO_ATENDIMENTO_DIAS' não pôde ser calculada.")

    # Análise do Cumprimento do Prazo Máximo para Encerramento
    print(f"\n{'#' * 30}\n# Análise do Cumprimento do Prazo Máximo para Encerramento\n{'#' * 30}")
    if 'DATA_LIMITE_ATENDIMENTO' in df.columns and 'DATA_ENCERRAMENTO' in df.columns:
        atendidos_prazo = df[df['STATUS'] == 'Atendido'].copy()
        if not atendidos_prazo.empty:
            atendidos_prazo['DENTRO_DO_PRAZO_LIMITE'] = atendidos_prazo['DATA_ENCERRAMENTO'] <= atendidos_prazo[
                'DATA_LIMITE_ATENDIMENTO']

            pct_dentro_prazo = atendidos_prazo['DENTRO_DO_PRAZO_LIMITE'].mean() * 100
            print(
                f"Percentual de chamados 'Atendido' dentro do Prazo Máximo para Encerramento: {pct_dentro_prazo:.2f}%")

            plt.figure(figsize=(8, 6))
            ax = sns.countplot(data=atendidos_prazo, x='DENTRO_DO_PRAZO_LIMITE', palette='viridis')
            plt.title('Cumprimento do Prazo Máximo para Encerramento para Chamados Atendidos')
            plt.xlabel('Dentro do Prazo Limite')
            plt.ylabel('Quantidade de Chamados')
            plt.xticks([0, 1], ['Não (Excedido)', 'Sim (No Prazo)'])
            # Adiciona os valores nas barras
            for p in ax.patches:
                ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', xytext=(0, 5), textcoords='offset points')
            plt.tight_layout()
            plt.show()

            # Análise do tempo de atraso/adiantamento em relação ao Prazo Limite
            atendidos_prazo['DIAS_EM_RELACAO_AO_PRAZO_LIMITE'] = (
                    atendidos_prazo['DATA_ENCERRAMENTO'] - atendidos_prazo['DATA_LIMITE_ATENDIMENTO']).dt.days

            # Calcula a média dos dias em relação ao prazo limite
            media_dias_em_relacao_prazo = atendidos_prazo['DIAS_EM_RELACAO_AO_PRAZO_LIMITE'].dropna().mean()

            print("\nEstatísticas dos DIAS_EM_RELACAO_AO_PRAZO_LIMITE (positivo = atraso, negativo = adiantamento):")
            print(atendidos_prazo['DIAS_EM_RELACAO_AO_PRAZO_LIMITE'].dropna().describe())
            print(f"Média de Dias em Relação ao Prazo Limite: {media_dias_em_relacao_prazo:.2f} dias")  # Mostra a média

            plt.figure(figsize=(10, 6))
            ax = sns.histplot(atendidos_prazo['DIAS_EM_RELACAO_AO_PRAZO_LIMITE'].dropna(), bins=30, palette='viridis')
            plt.title('Distribuição de Dias em Relação ao Prazo Máximo para Encerramento (Atendidos)')
            plt.xlabel('Dias (Encerramento - Limite do Prazo)')
            plt.ylabel('Frequência')
            plt.axvline(0, color='red', linestyle='--', label='Limite do Prazo')  # Linha para o limite do prazo

            # Adiciona a linha da média dos dias em relação ao prazo limite
            # A legenda será 'Média: X.XX dias (Atraso)' ou 'Média: X.XX dias (Adiantamento)'
            if media_dias_em_relacao_prazo > 0:
                label_media = f'Média: {media_dias_em_relacao_prazo:.2f} dias (Atraso)'
            elif media_dias_em_relacao_prazo < 0:
                label_media = f'Média: {abs(media_dias_em_relacao_prazo):.2f} dias (Adiantamento)'
            else:
                label_media = f'Média: {media_dias_em_relacao_prazo:.2f} dias (No Prazo)'

            plt.axvline(media_dias_em_relacao_prazo, color='blue', linestyle='-.', label=label_media)

            plt.legend()
            plt.tight_layout()
            # Adiciona os valores nas barras do histograma
            for p in ax.patches:
                height = p.get_height()
                if height > 0:  # Anota apenas barras com altura > 0
                    ax.annotate(f'{int(height)}', (p.get_x() + p.get_width() / 2., height),
                                ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=8)
            plt.show()

        else:
            print("Não há chamados 'Atendido' para analisar o Prazo Máximo para Encerramento.")
    else:
        print(
            "Colunas 'DATA_LIMITE_ATENDIMENTO' ou 'DATA_ENCERRAMENTO' não encontradas para análise do Prazo Máximo para Encerramento.")

    # Análise Temporal (Evolução dos Chamados por Mês)
    print(f"\n{'#' * 30}\n# Análise Temporal\n{'#' * 30}")
    if 'DATA_ABERTURA' in df.columns:
        df['ANO_MES_ABERTURA'] = df['DATA_ABERTURA'].dt.to_period('M')

        chamados_por_mes = df['ANO_MES_ABERTURA'].value_counts().sort_index()

        print("Chamados por Mês de Abertura:")
        print(chamados_por_mes)

        plt.figure(figsize=(10, 6))  # Largura ajustada
        ax = chamados_por_mes.plot(kind='line', marker='o', color='skyblue')
        plt.title('Evolução Mensal do Volume de Chamados')
        plt.xlabel('Mês da Abertura')
        plt.ylabel('Número de Chamados')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        for x, y in chamados_por_mes.items():
            ax.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0, 10), ha='center', va='bottom')
        plt.show()
    else:
        print("Coluna 'DATA_ABERTURA' não encontrada para análise temporal.")

    # Análise Aprofundada: Desempenho por Local
    print(f"\n{'#' * 30}\n# Análise Aprofundada: Desempenho por Local\n{'#' * 30}")

    # Taxa de Cancelamento por Local
    print(f"\n{'=' * 20} Taxa de Cancelamento por Local {'=' * 20}")
    cancelamentos_por_local = df.groupby('LOCAL')['STATUS'].value_counts(normalize=True).unstack().fillna(0)
    cancelamentos_por_local['Taxa_Cancelamento'] = cancelamentos_por_local['Cancelado'] * 100
    cancelamentos_por_local_ordenado = cancelamentos_por_local.sort_values(by='Taxa_Cancelamento', ascending=False)

    print("Taxa de Cancelamento (%) por Local:")
    print(cancelamentos_por_local_ordenado[['Taxa_Cancelamento']])

    fig, ax = plt.subplots(figsize=(10, 7))  # Usamos plt.subplots para capturar a figura e o eixo
    sns.barplot(x=cancelamentos_por_local_ordenado.index, y=cancelamentos_por_local_ordenado['Taxa_Cancelamento'],
                palette='viridis', ax=ax)  # Passa o 'ax' para o seaborn

    plt.title('Taxa de Cancelamento por Local de Atendimento')
    plt.xlabel('Local')
    plt.ylabel('Taxa de Cancelamento (%)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.show()

    # Percentual de Prazo Máximo para Encerramento Cumprido por Local
    print(f"\n{'=' * 20} Percentual de Prazo Máximo para Encerramento Cumprido por Local {'=' * 20}")
    atendidos_prazo_por_local = df[df['STATUS'] == 'Atendido'].copy()
    atendidos_prazo_por_local['DENTRO_DO_PRAZO_LIMITE'] = atendidos_prazo_por_local['DATA_ENCERRAMENTO'] <= \
                                                          atendidos_prazo_por_local['DATA_LIMITE_ATENDIMENTO']

    prazo_cumprido_por_local = atendidos_prazo_por_local.groupby('LOCAL')['DENTRO_DO_PRAZO_LIMITE'].mean() * 100
    prazo_cumprido_por_local_ordenado = prazo_cumprido_por_local.sort_values(ascending=True)

    print("Percentual de Prazo Máximo para Encerramento Cumprido (%) por Local (Apenas Atendidos):")
    print(prazo_cumprido_por_local_ordenado)

    plt.figure(figsize=(10, 7))
    ax = sns.barplot(x=prazo_cumprido_por_local_ordenado.index, y=prazo_cumprido_por_local_ordenado.values,
                     palette='viridis')
    plt.title('Percentual de Prazo Máximo para Encerramento Cumprido por Local de Atendimento')
    plt.xlabel('Local')
    plt.ylabel('% Prazo Cumprido')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.show()

    # Tempo Médio de Atendimento por Local
    print(f"\n{'=' * 20} Tempo Médio de Atendimento por Local {'=' * 20}")
    tempo_atendimento_por_local = atendidos.groupby('LOCAL')['TEMPO_ATENDIMENTO_DIAS'].mean()
    tempo_atendimento_por_local_ordenado = tempo_atendimento_por_local.sort_values(ascending=False)

    print("Tempo Médio de Atendimento (Dias) por Local (Apenas Atendidos):")
    print(tempo_atendimento_por_local_ordenado)

    plt.figure(figsize=(12, 7))
    ax = sns.barplot(x=tempo_atendimento_por_local_ordenado.index, y=tempo_atendimento_por_local_ordenado.values,
                     palette='viridis')
    plt.title('Tempo Médio de Atendimento por Local de Atendimento')
    plt.xlabel('Local')
    plt.ylabel('Tempo Médio de Atendimento (Dias)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.show()

    # Análise Aprofundada: Desempenho por Serviço
    print(f"\n{'#' * 30}\n# Análise Aprofundada: Desempenho por Serviço\n{'#' * 30}\n")

    # Taxa de Cancelamento por Serviço
    print(f"\n{'=' * 20} Taxa de Cancelamento por Serviço {'=' * 20}")
    cancelamentos_por_servico = df.groupby('SERVICO')['STATUS'].value_counts(normalize=True).unstack().fillna(0)
    cancelamentos_por_servico['Taxa_Cancelamento'] = cancelamentos_por_servico['Cancelado'] * 100
    cancelamentos_por_servico_ordenado = cancelamentos_por_servico.sort_values(by='Taxa_Cancelamento', ascending=False)

    print("Taxa de Cancelamento (%) por Serviço:")
    print(cancelamentos_por_servico_ordenado[['Taxa_Cancelamento']])

    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=cancelamentos_por_servico_ordenado.index,
                     y=cancelamentos_por_servico_ordenado['Taxa_Cancelamento'],
                     palette='magma')
    plt.title('Taxa de Cancelamento por Tipo de Serviço')
    plt.xlabel('Serviço')
    plt.ylabel('Taxa de Cancelamento (%)')
    # Adiciona os valores nas barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.show()

    # Percentual de Prazo Máximo para Encerramento Cumprido por Serviço
    print(f"\n{'=' * 20} Percentual de Prazo Máximo para Encerramento Cumprido por Serviço {'=' * 20}")
    prazo_cumprido_por_servico = atendidos_prazo.groupby('SERVICO')['DENTRO_DO_PRAZO_LIMITE'].mean() * 100
    prazo_cumprido_por_servico_ordenado = prazo_cumprido_por_servico.sort_values(ascending=True)

    print("Percentual de Prazo Máximo para Encerramento Cumprido (%) por Serviço (Apenas Atendidos):")
    print(prazo_cumprido_por_servico_ordenado)

    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=prazo_cumprido_por_servico_ordenado.index, y=prazo_cumprido_por_servico_ordenado.values,
                     palette='magma')
    plt.title('Percentual de Prazo Máximo para Encerramento Cumprido por Tipo de Serviço')
    plt.xlabel('Serviço')
    plt.ylabel('% Prazo Cumprido')
    # Adiciona os valores nas barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.show()

    # Tempo Médio de Atendimento por Serviço
    print(f"\n{'=' * 20} Tempo Médio de Atendimento por Serviço {'=' * 20}")
    tempo_atendimento_por_servico = atendidos.groupby('SERVICO')['TEMPO_ATENDIMENTO_DIAS'].mean()
    tempo_atendimento_por_servico_ordenado = tempo_atendimento_por_servico.sort_values(ascending=False)

    print("Tempo Médio de Atendimento (Dias) por Serviço (Apenas Atendidos):")
    print(tempo_atendimento_por_servico_ordenado)

    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=tempo_atendimento_por_servico_ordenado.index, y=tempo_atendimento_por_servico_ordenado.values,
                     palette='magma')
    plt.title('Tempo Médio de Atendimento por Tipo de Serviço')
    plt.xlabel('Serviço')
    plt.ylabel('Tempo Médio de Atendimento (Dias)')
    # Adiciona os valores nas barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.show()

    # Distribuição de Motivos de Cancelamento por Serviço
    print(f"\n{'=' * 20} Distribuição de Motivos de Cancelamento por Serviço {'=' * 20}")
    if not cancelados.empty:
        plt.figure(figsize=(12, 7))
        # Para este gráfico (countplot com hue), a lógica de anotação é um pouco mais complexa se quisermos o total por barra.
        # Mas para manter a clareza e não poluir muito, vamos deixar os valores de contagem no eixo Y.
        ax = sns.countplot(data=cancelados, x='SERVICO', hue='MOTIVO_CANCELAMENTO', palette='tab10')
        plt.title('Motivos de Cancelamento por Tipo de Serviço')
        plt.xlabel('Tipo de Serviço')
        plt.ylabel('Quantidade de Cancelamentos')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Motivo de Cancelamento', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
    else:
        print("Não há chamados cancelados para analisar motivos por serviço.")

    # Análise Comparativa de Prazos (Concorrência e Expectativa do Cliente)
    print(f"\n{'#' * 30}\n# Análise Comparativa de Prazos\n{'#' * 30}")

    if 'PRAZO_MAXIMO_CONCORRENCIA_DIAS' in df.columns and 'EXPECTATIVA_CLIENTE_DIAS' in df.columns:
        df['PRAZO_HORAS_DIAS'] = df['PRAZO_HORAS'] / 24.0
        media_tempo_atendimento = atendidos['TEMPO_ATENDIMENTO_DIAS'].mean()

        prazo_concorrencia = df['PRAZO_MAXIMO_CONCORRENCIA_DIAS'].iloc[0] if not df.empty else None
        expectativa_cliente = df['EXPECTATIVA_CLIENTE_DIAS'].iloc[0] if not df.empty else None

        print(f"\nTempo Médio de Atendimento da Cielo (Chamados Atendidos): {media_tempo_atendimento:.2f} dias")
        if prazo_concorrencia is not None:
            print(f"Prazo Máximo da Concorrência (Outras Adquirentes): {prazo_concorrencia:.2f} dias")
        if expectativa_cliente is not None:
            print(f"Expectativa do Cliente (Setor Logístico Geral): {expectativa_cliente:.2f} dias")

        if media_tempo_atendimento is not None and prazo_concorrencia is not None and expectativa_cliente is not None:
            prazos_comp = pd.DataFrame({
                'Métrica': ['Cielo (Nosso Prazo Real)', 'Concorrência', 'Expectativa Cliente'],
                'Dias': [media_tempo_atendimento, prazo_concorrencia, expectativa_cliente]
            })

            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x='Métrica', y='Dias', data=prazos_comp, palette='coolwarm')
            plt.title('Comparativo: Nosso Prazo vs. Concorrência vs. Expectativa do Cliente')
            plt.xlabel('Métrica de Prazo')
            plt.ylabel('Tempo em Dias')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            # Adiciona os valores nas barras
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', xytext=(0, 5), textcoords='offset points')
            plt.tight_layout()
            plt.show()
        else:
            print("Dados insuficientes para análise comparativa de prazos.")
    else:
        print("Colunas de comparação de prazos não encontradas.")

    # Conclusão
    print(f"\n{'#' * 30}\n# Fim da Análise Exploratória\n{'#' * 30}")
    print("Revise os gráficos e as estatísticas para identificar padrões e possíveis problemas.")
    print("As análises acima fornecem subsídios para responder às perguntas guias do desafio.")


if __name__ == "__main__":
    INPUT_FILE = 'input/dataset_cielo.csv'
    analyze_cielo_data(INPUT_FILE)