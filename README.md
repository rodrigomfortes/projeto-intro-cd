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

## 📂 Estrutura do Repositório

```bash
├── data/
│   ├── raw/          # Arquivos originais (.csv, .xlsx) baixados do SISDEPEN/CNJ
│   └── processed/    # Datasets limpos e tratados prontos para análise
├── notebooks/        # Jupyter Notebooks com as análises exploratórias e gráficos
├── src/              # Scripts Python de extração e limpeza (ETL)
├── README.md         # Documentação do projeto
└── requirements.txt  # Dependências do projeto
