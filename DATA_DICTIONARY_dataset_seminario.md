# Dicionário de dados — `dataset_seminario.csv`

Conjunto derivado do pipeline em `build_dataset_seminario.py` (18º ciclo, um registro por estabelecimento). Separador do arquivo: `;`, codificação UTF-8.

**Número de colunas:** 106

| # | Coluna | Tipo | Descrição | Exemplo (1ª linha) |
|---:|---|---|---|---|
| 1 | `tipo_estabelecimento` | texto (categórico) | Tipo do estabelecimento prisional (texto da base). | Domiciliar com monitoramento eletrônico |
| 2 | `uf` | texto (categórico) | Unidade federativa (sigla). | AC |
| 3 | `municipio` | texto (categórico) | Nome do município. | Brasileia |
| 4 | `gestao` | texto (categórico) | Tipo de gestão (ex.: pública/privada), conforme mapeamento na base intermediária. | Pública |
| 5 | `capacidade_total_final` | numérico | Capacidade total usada nos cálculos; no pipeline atual replica `capacidade_total_calculada`. | 178 |
| 6 | `capacidade_total_calculada` | numérico | Soma das capacidades por regime (provisórios, fechado, semiaberto, aberto, RDD, medida internação, outros). | 178 |
| 7 | `vagas_desativadas_total` | numérico | Total de vagas desativadas (coluna Total mapeada da base). | 0 |
| 8 | `capacidade_masculino_total` | numérico | Capacidade para população masculina. | 157 |
| 9 | `capacidade_feminino_total` | numérico | Capacidade para população feminina. | 21 |
| 10 | `capacidade_provisorios_total` | numérico | Vagas destinadas a provisórios. | 0 |
| 11 | `capacidade_fechado_total` | numérico | Vagas em regime fechado. | 0 |
| 12 | `capacidade_semiaberto_total` | numérico | Vagas em regime semiaberto. | 0 |
| 13 | `capacidade_aberto_total` | numérico | Vagas em regime aberto. | 0 |
| 14 | `capacidade_rdd_total` | numérico | Capacidade RDD (regime disciplinar diferenciado). | 0 |
| 15 | `capacidade_medida_internacao_total` | numérico | Capacidade para medida de internação. | 0 |
| 16 | `capacidade_outros_total` | numérico | Capacidade classificada como outros na base. | 178 |
| 17 | `pop_total_final` | numérico | População total usada nos KPIs: `pop_total` oficial quando existe, senão `pop_total_calculada`. | 178 |
| 18 | `pop_total` | numérico | População total declarada na base (Total), quando disponível. | 178 |
| 19 | `pop_total_calculada` | numérico | Soma das populações por regime (provisórios, fechado, semiaberto, aberto, internação, tratamento ambulatorial). | 178 |
| 20 | `pop_provisorios_total` | numérico | População em regime provisório. | 45 |
| 21 | `pop_fechado_total` | numérico | População em regime fechado. | 0 |
| 22 | `pop_semiaberto_total` | numérico | População em regime semiaberto. | 133 |
| 23 | `pop_aberto_total` | numérico | População em regime aberto. | 0 |
| 24 | `pop_internacao_total` | numérico | População em medida de internação. | 0 |
| 25 | `pop_tratamento_ambulatorial_total` | numérico | População em tratamento ambulatorial. | 0 |
| 26 | `pop_rdd_total` | numérico | População em RDD. | 0 |
| 27 | `taxa_ocupacao` | numérico | Razão `pop_total_final` / `capacidade_total_final` (quando capacidade > 0). | 1 |
| 28 | `flag_superlotacao` | numérico | 1 se `taxa_ocupacao` > 1, caso contrário 0. | 0 |
| 29 | `perc_provisorios` | numérico | Proporção de provisórios sobre `pop_total_final`. | 0.2528089887640449 |
| 30 | `perc_fechado` | numérico | Proporção em fechado sobre `pop_total_final`. | 0 |
| 31 | `perc_semiaberto` | numérico | Proporção em semiaberto sobre `pop_total_final`. | 0.7471910112359551 |
| 32 | `perc_aberto` | numérico | Proporção em aberto sobre `pop_total_final`. | 0 |
| 33 | `mov_entradas_total` | numérico | Movimentação: entradas no período (Total). | 12 |
| 34 | `mov_alvaras_total` | numérico | Movimentação: alvarás de soltura (Total). | 10 |
| 35 | `mov_abandonos_total` | numérico | Movimentação: abandonos (Total). | 0 |
| 36 | `mov_obitos_total` | numérico | Movimentação: óbitos (Total). | 2 |
| 37 | `mov_transf_in_total` | numérico | Transferências recebidas (Total). | 5 |
| 38 | `mov_transf_out_total` | numérico | Transferências enviadas (Total). | 2 |
| 39 | `mov_perm_saida_total` | numérico | Permanências de saída (Total). | 0 |
| 40 | `mov_saida_temp_total` | numérico | Saídas temporárias (Total). | 0 |
| 41 | `pop_18_29_total` | numérico | Soma `idade_18_24_total` + `idade_25_29_total`. | 83 |
| 42 | `perc_18_29` | numérico | Proporção de 18–29 anos sobre `pop_total_final`. | 0.4662921348314606 |
| 43 | `idade_18_24_total` | numérico | População na faixa 18–24 anos (Total). | 29 |
| 44 | `idade_25_29_total` | numérico | População na faixa 25–29 anos (Total). | 54 |
| 45 | `idade_30_34_total` | numérico | População na faixa 30–34 anos (Total). | 28 |
| 46 | `idade_35_45_total` | numérico | População na faixa 35–45 anos (Total). | 42 |
| 47 | `idade_46_60_total` | numérico | População na faixa 46–60 anos (Total). | 22 |
| 48 | `idade_61_70_total` | numérico | População na faixa 61–70 anos (Total). | 2 |
| 49 | `idade_70mais_total` | numérico | População com 70 anos ou mais (Total). | 1 |
| 50 | `idade_nao_info_total` | numérico | População com idade não informada (Total). | 0 |
| 51 | `raca_parda_preta_total` | numérico | Soma `raca_parda_total` + `raca_preta_total`. | 160 |
| 52 | `perc_parda_preta` | numérico | Proporção parda+preta sobre `pop_total_final`. | 0.898876404494382 |
| 53 | `raca_branca_total` | numérico | População autodeclarada branca (Total). | 14 |
| 54 | `raca_preta_total` | numérico | População autodeclarada preta (Total). | 16 |
| 55 | `raca_parda_total` | numérico | População autodeclarada parda (Total). | 144 |
| 56 | `raca_amarela_total` | numérico | População autodeclarada amarela (Total). | 0 |
| 57 | `raca_indigena_total` | numérico | População autodeclarada indígena (Total). | 4 |
| 58 | `raca_nao_info_total` | numérico | População com raça/cor não informada (Total). | 0 |
| 59 | `proc_urb_interior_total` | numérico | Soma procedência urbano interior (M + F). | 173 |
| 60 | `proc_urb_rm_total` | numérico | Soma procedência urbano RM (M + F). | 0 |
| 61 | `proc_rural_total` | numérico | Soma procedência rural (M + F). | 5 |
| 62 | `civil_solteiro_total` | numérico | Estado civil solteiro (Total). | 122 |
| 63 | `civil_uniao_total` | numérico | União estável (Total). | 34 |
| 64 | `civil_casado_total` | numérico | Casado(a) (Total). | 19 |
| 65 | `civil_separado_total` | numérico | Separado(a) (Total). | 1 |
| 66 | `civil_divorciado_total` | numérico | Divorciado(a) (Total). | 2 |
| 67 | `civil_viuvo_total` | numérico | Viúvo(a) (Total). | 0 |
| 68 | `civil_nao_info_total` | numérico | Estado civil não informado (Total). | 0 |
| 69 | `gestao_saude_terceirizada` | texto (categórico) | Resposta Sim/Não: gestão da saúde terceirizada. | Não |
| 70 | `gestao_assist_juridica_terceirizada` | texto (categórico) | Resposta Sim/Não: assistência jurídica terceirizada. | Não |
| 71 | `saude_nao_possui` | texto (categórico) | Estabelecimento não possui módulo de saúde (Sim/Não). | Sim |
| 72 | `saude_consultorio_medico` | texto (categórico) | Possui consultório médico (Sim/Não). | Não |
| 73 | `saude_consultorio_odontologico` | texto (categórico) | Possui consultório odontológico (Sim/Não). | Não |
| 74 | `saude_enfermagem` | texto (categórico) | Possui enfermagem (Sim/Não). | Não |
| 75 | `saude_farmacia` | texto (categórico) | Possui farmácia (Sim/Não). | Não |
| 76 | `flag_sem_modulo_saude` | numérico | 1 se `saude_nao_possui` = Sim, 0 se Não (mapeamento textual). | 1 |
| 77 | `educacao_nao_possui` | texto (categórico) | Não possui módulo de educação (Sim/Não). | Sim |
| 78 | `educacao_sala_aula` | texto (categórico) | Possui sala de aula (Sim/Não). | Não |
| 79 | `educacao_sala_informatica` | texto (categórico) | Possui sala de informática (Sim/Não). | Não |
| 80 | `educacao_biblioteca` | texto (categórico) | Possui biblioteca (Sim/Não). | Não |
| 81 | `flag_sem_modulo_educacao` | numérico | 1 se `educacao_nao_possui` = Sim, 0 se Não. | 1 |
| 82 | `assist_juridica_nao` | texto (categórico) | Sem assistência jurídica listada (Sim/Não conforme base). | Não |
| 83 | `assist_juridica_defensoria` | texto (categórico) | Assistência via defensoria (Sim/Não). | Sim |
| 84 | `assist_juridica_dativos` | texto (categórico) | Assistência via dativos (Sim/Não). | Não |
| 85 | `assist_juridica_ong` | texto (categórico) | Assistência via ONG (Sim/Não). | Não |
| 86 | `flag_assist_juridica_defensoria` | numérico | 1 se `assist_juridica_defensoria` = Sim, 0 se Não. | 1 |
| 87 | `saude_consultas_ext_total` | numérico | Consultas em serviço externo (Total, período). | 0 |
| 88 | `saude_consultas_no_estab_total` | numérico | Consultas no estabelecimento (Total). | 0 |
| 89 | `saude_consultas_psico_total` | numérico | Consultas psicológicas (Total). | 0 |
| 90 | `saude_consultas_odonto_total` | numérico | Consultas odontológicas (Total). | 0 |
| 91 | `saude_exames_total` | numérico | Exames realizados (Total). | 0 |
| 92 | `saude_vacinas_total` | numérico | Vacinas aplicadas (Total). | 0 |
| 93 | `saude_outros_proc_total` | numérico | Outros procedimentos de saúde (Total). | 0 |
| 94 | `mortalidade_natural_total` | numérico | Óbitos por causas naturais (Total). | 0 |
| 95 | `mortalidade_criminal_total` | numérico | Óbitos por causas criminais (Total). | 0 |
| 96 | `mortalidade_suicidio_total` | numérico | Óbitos por suicídio (Total). | 0 |
| 97 | `mortalidade_acidental_total` | numérico | Óbitos acidentais (Total). | 0 |
| 98 | `mortalidade_causa_desconhecida_total` | numérico | Óbitos com causa desconhecida (Total). | 2 |
| 99 | `controle_mais_90_dias` | texto (categórico) | Indicador de controle: mais de 90 dias (texto Sim/Não). | Não |
| 100 | `controle_semiaberto_aguardando_vaga` | texto (categórico) | Semiaberto aguardando vaga (texto Sim/Não). | Não |
| 101 | `proc_urb_interior_masc` | numérico | Procedência urbano interior, sexo masculino. | 152 |
| 102 | `proc_urb_interior_fem` | numérico | Procedência urbano interior, sexo feminino. | 21 |
| 103 | `proc_urb_rm_masc` | numérico | Procedência urbano RM, sexo masculino. | 0 |
| 104 | `proc_urb_rm_fem` | numérico | Procedência urbano RM, sexo feminino. | 0 |
| 105 | `proc_rural_masc` | numérico | Procedência rural, sexo masculino. | 5 |
| 106 | `proc_rural_fem` | numérico | Procedência rural, sexo feminino. | 0 |
