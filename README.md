# Desafio Cielo S.A - 408524/2025-1

**Formato:** PPT  
**Prazo:** 14/07/25

## Desafio

A logística é um dos principais motores de satisfação dos clientes para qualquer empresa cujo produto é físico e precisa ser entregue para o cliente. Na Cielo, disponibilizamos soluções de pagamento. Uma dessas soluções é a maquininha de cartão. Ao longo do ciclo de vida dos clientes, necessitamos instalar (entregar uma nova máquina para um cliente existente ou a um novo) e trocar (o serviço de manutenção da Cielo consiste em substituir o terminal defeituoso por outro) as máquinas dos nossos clientes.


## Contexto

Você é analista de dados da logística da Cielo e recebeu uma base histórica de atendimentos.  
Essa base possui, para cada chamado logístico, as seguintes informações:

- **LOCAL**: local do atendimento  
- **SERVICO**: se é um chamado de instalação ou de manutenção  
- **STATUS**: o status do chamado (se foi atendido com sucesso ou cancelado)  
- **MOTIVO_CANC**: motivo do cancelamento do chamado (apontado pelo entregador)  
- **DATA_ABERTURA**: data da solicitação do cliente  
- **DATA_ENCERRAMENTO**: data da finalização do chamado  
- **DATA_LIMITE_ATENDIMENTO**: prazo máximo para encerramento do chamado (este é o prazo informado para o cliente durante a solicitação)

## Objetivos

- Realizar uma análise exploratória dos dados visando reconhecer padrões da logística da Cielo  
- Estabelecer um plano de ação visando alavancar a experiência do cliente

### Perguntas guia

- Existe algum local ofensor de experiência do cliente?
- Existe algum serviço deficiente?
- Estamos estabelecendo e praticando bons prazos frente a concorrência (outras adquirentes)?
- Estamos estabelecendo e praticando bons prazos frente à expectativa do cliente com o setor logístico (Mercado Livre, Amazon, etc)?
- Quais outras hipóteses poderiam ser testadas em um segundo momento?

## Entrega final

- Power Point com os resultados principais da sua análise a ser apresentado para o time de logística
- Tempo de apresentação do case: até 30 minutos (seja sucinto)

---

## Como utilizar este repositório

### 1. Pré-requisitos

- **Python 3.8+** instalado  
- **Git** instalado (opcional, para clonar o repositório)

### 2. Instalando o projeto

```bash
# Clone o repositório
git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_REPOSITORIO>

# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente virtual
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate

# Atualize o Pip
pip install --upgrade pip

# Instale as dependências
pip install -r requirements.txt
```

---

## Arquivos: 

### 01_generate_sample_data.py

> **Descrição**:  
> Gera uma base de dados fictícia de chamados de serviço, simulando cenários de atendimentos em cidades brasileiras. Os dados incluem informações sobre local, tipo de serviço, status, motivos de cancelamento, datas e conclusão de chamados, entre outros campos.

> **Parâmetros**:  
> Nesse script você pode definir 2 parâmetros:
> 
> - **NUM_LINHAS:** Número de linhas a serem geradas no conjunto de dados.
> - **OUTPUT_FILENAME:** Nome do arquivo e caminho que o dataset final será gerado.

---

# Análise Exploratória dos Dados de Logística da Cielo

Com base na execução do script `02_primeiras_estatisticas.py` e os resultados apresentados, obtivemos insights valiosos sobre a logística da Cielo.

## Visão Geral do Dataset

*   **Volume de Dados:** O dataset contém 100.000 registros de chamados logísticos, cobrindo o período de janeiro a junho de 2025.
*   **Estrutura:** As colunas como `LOCAL`, `SERVICO`, `STATUS`, `DATA_ABERTURA`, `DATA_ENCERRAMENTO`, `DATA_LIMITE_ATENDIMENTO`, entre outras, estão bem estruturadas e com os tipos de dados corretos.
*   **Dados Ausentes:** Apenas a coluna `MOTIVO_CANCELAMENTO` possui valores nulos (76.396), o que é esperado, já que este campo só é preenchido para chamados com `STATUS` 'Cancelado'.
*   **Novas Colunas:** As colunas `PRAZO_MAXIMO_CONCORRENCIA_DIAS` (2.0 dias) e `EXPECTATIVA_CLIENTE_DIAS` (1.0 dia) foram corretamente integradas, e seus valores constantes indicam que são referências de benchmark.

## Análise Geral do Desempenho

*   **Status dos Chamados:** Do total de 100.000 chamados, **76.396 foram 'Atendido'** e **23.604 foram 'Cancelado'**. Isso representa uma taxa de cancelamento geral de **23.60%**.
*   **Motivos de Cancelamento:** O `Problema técnico` é o motivo de cancelamento mais frequente (5.330 ocorrências), seguido por `Solicitação do cliente` e `Cliente ausente`.
*   **Tempo de Atendimento:** Para os chamados `Atendido`, o tempo médio de atendimento é de aproximadamente **2.12 dias**. A maioria dos atendimentos se concentra entre 1 e 3 dias.
*   **Cumprimento do Prazo Máximo para Encerramento:** Apenas **30.47% dos chamados 'Atendido' foram concluídos dentro do `DATA_LIMITE_ATENDIMENTO`**. Isso é um ponto de atenção crítico, indicando que a grande maioria dos atendimentos está excedendo o prazo prometido ao cliente. Em média, os chamados 'Atendido' excedem o prazo limite em **0.11 dias** (ou seja, estão ligeiramente atrasados em relação ao prazo, em média).
*   **Análise Temporal:** O volume de chamados por mês de abertura é relativamente estável ao longo do período analisado (média de aproximadamente 16.600 chamados/mês), sem grandes variações ou picos que sugiram sazonalidade expressiva neste recorte de seis meses.

---

## Respostas às Perguntas Guia do Desafio

### Realizar uma análise exploratória dos dados visando reconhecer padrões da logística da Cielo

**Resposta:** Sim, realizamos uma Análise Exploratória de Dados (AED) detalhada, cobrindo a distribuição geral dos chamados por local, serviço e status, análise dos motivos de cancelamento, tempo de atendimento, cumprimento do prazo máximo para encerramento e uma análise temporal. Essa AED permitiu identificar os padrões operacionais atuais da logística da Cielo.

### Estabelecer um plano de ação visando alavancar a experiência do cliente

**Resposta:** A análise fornecida estabelece a base sólida para a elaboração deste plano de ação. Ao identificar os "locais ofensores" e "serviços deficientes", e ao comparar os prazos da Cielo com a concorrência e a expectativa do cliente, você tem dados concretos para direcionar as iniciativas de melhoria. As "hipóteses para um segundo momento" também servem como passos iniciais para aprofundamento do plano. O plano de ação em si será a próxima etapa estratégica que você construirá com base nesses achados.

### Existe algum local ofensor de experiência do cliente?

**Resposta:** Sim. A análise identificou `Guarulhos (RM)` como um local ofensor claro, apresentando taxas de cancelamento significativamente mais altas, um percentual de cumprimento de prazo limite muito inferior e um tempo médio de atendimento mais elevado em comparação com os outros bairros/locais simulados.

### Existe algum serviço deficiente?

**Resposta:** Sim. O serviço de `Manutenção` foi identificado como deficiente, com taxas de cancelamento e tempos médios de atendimento superiores, e um percentual de cumprimento de prazo limite inferior ao serviço de `Instalação`.

### Estamos estabelecendo e praticando bons prazos frente a concorrência (outras adquirentes)?

**Resposta:** Não exatamente. A análise mostrou que o tempo médio de atendimento da Cielo (2.12 dias) está ligeiramente acima do prazo máximo simulado da concorrência (2.00 dias), indicando que há espaço para otimização para se equiparar ou superar o mercado.

### Estamos estabelecendo e praticando bons prazos frente a expectativa do cliente com o setor logístico (Mercado Livre, Amazon, etc)?

**Resposta:** Não. Há uma lacuna considerável. O tempo médio de atendimento da Cielo (2.12 dias) é mais do que o dobro da expectativa do cliente para o setor logístico (1.00 dia), sugerindo a necessidade de melhorias substanciais na agilidade.

### Quais outras hipóteses poderiam ser testadas em um segundo momento?

**Resposta:** Sim, fornecemos diversas hipóteses, como a necessidade de análise de causa raiz aprofundada para `Guarulhos (RM)` e o serviço de `Manutenção`, investigar o impacto do `PRAZO_HORAS` interno, expandir a análise de sazonalidade e realizar análise de outliers e correlação de motivos de cancelamento com o tempo.