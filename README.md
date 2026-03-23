# 📊 Análise de Dados do Sistema Carcerário Brasileiro

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-orange)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

> **Tema:** Superlotação, Reincidência e a "Fila Invisível" da Ressocialização: Uma análise da assimetria entre a oferta estatal e a demanda prisional.

## 👥 Integrantes do Grupo
* **Gerson Gonçalves de Freitas**
* **Nicolas Kleiton da Silva Melo**
* **Pedro Falconi**
* **Rodrigo Monteiro Fortes de Oliveira**

---

## 🎯 Objetivo do Projeto
Este projeto visa ir além da simples contagem demográfica da população carcerária. O objetivo central é utilizar **Ciência de Dados** para auditar a eficiência do Estado na gestão penal.

Buscamos responder perguntas críticas através dos dados:
1.  **Existe uma "fila" estrutural?** O preso não trabalha/estuda por falta de interesse ou por falta de vagas (demanda reprimida)?
2.  **Superlotação e Justiça:** Qual a correlação entre o déficit de vagas e o tempo de prisão provisória?
3.  **Seletividade:** O sistema pune perfis sociais específicos ou condutas criminosas de forma isonômica?

---

## 🛠️ Abordagem de Coleta e Metodologia (ETL)

Utilizamos dados públicos agregados (para garantir anonimidade e ética) processados via pipeline em **Python**.

### Fontes de Dados
* **SISDEPEN (antigo InfoPen/SENAPPEN):** Dados de infraestrutura, capacidade, perfil dos internos e gestão.
* **CNJ (BNMP 3.0 e Painéis):** Dados processuais, fluxo de entrada/saída e tipificação penal.
* **IPEA (Atlas da Violência):** Referência para definições e taxas de reincidência.

### Engenharia de Dados
Não utilizamos apenas as colunas brutas. Criamos **variáveis calculadas** para medir fenômenos sociais:

* `indice_oferta_educacao`: Vagas de Estudo Disponíveis / População Prisional Apta.
* `demanda_reprimida_trabalho`: Diferença entre população disponível para trabalho e postos ofertados pelo Estado.
* `taxa_superlotacao_real`: Comparativo entre capacidade de projeto vs. população total (incluindo provisórios).

---
# 18º Ciclo — Base de Dados (2025/1)
Este repositório documenta e disponibiliza um conjunto de dados do **18º ciclo** com referência **2025/1**, contendo informações sobre **estabelecimentos ligados ao sistema prisional**. O arquivo original está em formato **CSV** (separado por `;`, UTF‑8).

- Arquivo analisado: `18o-ciclo-base-de-dados-2025-1-semestre.csv`
- Tamanho: **1555 linhas** × **1737 colunas**

---

## (2) Descrição do conjunto de dados

O conjunto de dados reúne informações do **18º ciclo (Ano 2025, referência 2025/1)**. Cada registro (linha) representa **um estabelecimento** e contém:

- **Campos de identificação** (ex.: UF, município, código IBGE, endereço, tipo e situação do estabelecimento).
- Um grande volume de **variáveis/indicadores de questionário**, organizados por seções numeradas (ex.: `1.x`, `2.x`, `5.14`, `6.3`…), frequentemente com recortes por sexo (ex.: Masculino/Feminino/Total) e outras segmentações (regime, faixas, tipos, etc.).

Por ser um arquivo muito ‘largo’ (muitas colunas), ele é adequado para análises descritivas e comparações entre estabelecimentos (por UF/município/tipo), além de estudos por recortes.

## (3) Processo de coleta dos dados (resumo)

Os dados foram coletados no contexto do **ciclo 18 (2025/1)** por meio de **preenchimento/registro de informações por estabelecimento** em um instrumento padronizado (questionário/indicadores). O arquivo possui uma coluna de **situação de preenchimento** (ex.: ‘Validado’), o que sugere uma etapa de conferência/validação do registro.

> **Fonte (preencher):** https://www.gov.br/senappen/pt-br/servicos/sisdepen/bases-de-dados

## (4) Dicionário de dados (colunas)

O dataset possui **1737 colunas**. Para manter o README legível, o dicionário completo (Nome / Descrição / Exemplo) foi gerado automaticamente em:

- `DATA_DICTIONARY_18o_ciclo_2025_1.md`

Abaixo, um recorte das principais colunas de identificação (exemplo real da 1ª linha do arquivo):

| Nome da coluna | Descrição da coluna | Exemplo |
|---|---|---|
| ciclo | ciclo | 18 |
| Ano | Ano | 2025 |
| Referência | Referência | 2025/1 |
| Tipo do Estabelecimento | Tipo do Estabelecimento | Domiciliar com monitoramento eletrônico |
| Situação de Preenchimento | Situação de Preenchimento | Validado |
| Nome do Estabelecimento | Nome do Estabelecimento | NÚCLEO DE MONITORAMENTO ELETRÔNICO DOMICILIAR DE BRASILÉIA |
| Situação do Estabelecimento | Situação do Estabelecimento | Ativo |
| Outras Denominações | Outras Denominações | (vazio) |
| Endereço | Endereço | Travessa Santos Dumond, 2 |
| Bairro | Bairro | Centro |
| CEP | CEP | 69934000 |
| Âmbito | Âmbito | Estadual |
| UF | UF | AC |
| Município | Município | Brasileia |
| Código IBGE | Código IBGE | 1200104 |

### Dicionário completo

O arquivo `DATA_DICTIONARY_18o_ciclo_2025_1.md` contém uma linha por coluna com: **Nome da coluna**, **Descrição** e **Exemplo** (valor da 1ª linha; quando vazio, aparece `(vazio)`).

## (5) Armazenamento dos dados (Google Drive)

Os dados (arquivo CSV original) foram adicionados em um serviço de nuvem para facilitar o acesso:

- Link (Google Drive ou similar): **(https://drive.google.com/drive/folders/1mbPYSqTbY7Ta-p4c8MBlkS6149_XRcRB?usp=sharing)**

## 📂 Estrutura do Repositório

```bash
├── data/
│   ├── raw/          # Arquivos originais (.csv, .xlsx) baixados do SISDEPEN/CNJ
│   └── processed/    # Datasets limpos e tratados prontos para análise
├── notebooks/        # Jupyter Notebooks com as análises exploratórias e gráficos
├── src/              # Scripts Python de extração e limpeza (ETL)
├── README.md         # Documentação do projeto
└── requirements.txt  # Dependências do projeto

