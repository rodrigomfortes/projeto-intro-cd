# -*- coding: utf-8 -*-
"""
Gera uma versão v3 do dataset, focada em seminário:
- reduz colunas da v2 para um conjunto analítico e narrativo
- prioriza colunas Total
- mantém poucas colunas binárias de estrutura
- cria métricas derivadas prontas para gráfico

Uso:
    python build_dataset_seminario.py

Ajuste apenas SRC e OUT se quiser.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

SRC = Path("dataset_seminario_v2.csv")
OUT = Path("dataset_seminario.csv")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s.lower().strip()


def safe_num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def pick_col(columns: list[str], includes: list[str], excludes: list[str] | None = None) -> str | None:
    excludes = excludes or []
    norm_cols = [(c, norm(c)) for c in columns]

    for col, ncol in norm_cols:
        if all(term in ncol for term in includes) and not any(term in ncol for term in excludes):
            return col
    return None


def pick_many(columns: list[str], patterns: list[tuple[list[str], list[str] | None]]) -> dict[str, str | None]:
    out: dict[str, str | None] = {}
    for alias, (includes, excludes) in patterns:
        out[alias] = pick_col(columns, includes, excludes)
    return out


def add_numeric_if_exists(df_in: pd.DataFrame, df_out: pd.DataFrame, src_col: str | None, dst_col: str) -> None:
    if src_col and src_col in df_in.columns:
        df_out[dst_col] = safe_num(df_in[src_col])


def add_text_if_exists(df_in: pd.DataFrame, df_out: pd.DataFrame, src_col: str | None, dst_col: str) -> None:
    if src_col and src_col in df_in.columns:
        df_out[dst_col] = df_in[src_col]


def main() -> None:
    if not SRC.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {SRC.resolve()}")

    df = pd.read_csv(SRC, sep=";", encoding="utf-8", low_memory=False)
    cols = list(df.columns)

    # ---------------------------
    # 1) Mapear colunas centrais
    # ---------------------------
    patterns = [
        ("tipo_estabelecimento", (["tipo do estabelecimento"], None)),
        ("uf", (["uf"], None)),
        ("municipio", (["municipio"], None)),
        ("gestao", (["gestao do estabelecimento"], None)),

        # Capacidade
        ("capacidade_provisorios_total", (["capacidade do estabelecimento", "presos provisorios", "total"], None)),
        ("capacidade_fechado_total", (["capacidade do estabelecimento", "regime fechado", "total"], None)),
        ("capacidade_semiaberto_total", (["capacidade do estabelecimento", "regime semiaberto", "total"], None)),
        ("capacidade_aberto_total", (["capacidade do estabelecimento", "regime aberto", "total"], None)),
        ("capacidade_rdd_total", (["capacidade do estabelecimento", "regime disciplinar diferenciado", "total"], None)),
        ("capacidade_medida_internacao_total", (["capacidade do estabelecimento", "medidas de seguranca de internacao", "total"], None)),
        ("capacidade_outros_total", (["capacidade do estabelecimento", "outro(s). qual(is)?", "total"], None)),
        ("capacidade_masculino_total", (["capacidade do estabelecimento", "masculino", "total"], ["vagas desativadas"])),
        ("capacidade_feminino_total", (["capacidade do estabelecimento", "feminino", "total"], ["vagas desativadas"])),
        ("vagas_desativadas_total", (["capacidade do estabelecimento", "total de vagas desativadas"], None)),

        # Estrutura/serviços
        ("gestao_saude_terceirizada", (["quais servicos sao terceirizados?", "saude"], None)),
        ("gestao_assist_juridica_terceirizada", (["quais servicos sao terceirizados?", "assistencia juridica"], None)),
        ("saude_nao_possui", (["modulo de saude", "nao possui modulo de saude"], None)),
        ("saude_consultorio_medico", (["modulo de saude", "consultorio medico"], ["quantidade", "outras finalidades"])),
        ("saude_consultorio_odontologico", (["modulo de saude", "consultorio odontologico"], ["quantidade", "outras finalidades"])),
        ("saude_enfermagem", (["modulo de saude", "sala de curativos, suturas, vacinas e posto de enfermagem"], ["quantidade", "outras finalidades"])),
        ("saude_farmacia", (["modulo de saude", "farmacia ou sala de estoque/ dispensacao de medicamentos"], ["quantidade", "outras finalidades"])),
        ("educacao_nao_possui", (["modulo de educacao", "nao possui"], None)),
        ("educacao_sala_aula", (["modulo de educacao", "sala de aula"], ["quantidade", "capacidade"])),
        ("educacao_sala_informatica", (["modulo de educacao", "sala de informatica"], ["quantidade", "capacidade"])),
        ("educacao_biblioteca", (["modulo de educacao", "biblioteca"], ["quantidade", "capacidade"])),
        ("assist_juridica_nao", (["prestacao sistematica de assistencia juridica", "| nao"], None)),
        ("assist_juridica_defensoria", (["prestacao sistematica de assistencia juridica", "defensoria publica"], None)),
        ("assist_juridica_dativos", (["prestacao sistematica de assistencia juridica", "advogados conveniados/ dativos"], None)),
        ("assist_juridica_ong", (["prestacao sistematica de assistencia juridica", "ong ou outra entidade sem fins lucrativos"], None)),

        # População
        ("pop_provisorios_total", (["populacao prisional", "presos provisorios", "total"], None)),
        ("pop_fechado_total", (["populacao prisional", "regime fechado", "total"], None)),
        ("pop_semiaberto_total", (["populacao prisional", "regime semiaberto", "total"], None)),
        ("pop_aberto_total", (["populacao prisional", "regime aberto", "total"], None)),
        ("pop_internacao_total", (["populacao prisional", "medida de seguranca - internacao", "total"], None)),
        ("pop_tratamento_ambulatorial_total", (["populacao prisional", "tratamento ambulatorial", "total"], None)),
        ("pop_total", (["populacao prisional", "| total"], ["regime", "provisorios", "internacao", "tratamento", "rdd"])),
        ("pop_rdd_total", (["populacao prisional", "regime disciplinar diferenciado"], None)),

        # Controle / gargalo processual
        ("controle_mais_90_dias", (["tem controle da informacao sobre quantos presos provisorios tem mais de 90 dias"], ["sim. quantos"])),
        ("controle_semiaberto_aguardando_vaga", (["tem controle da informacao sobre quantos presos sentenciados no regime fechado", "aguardam vaga"], ["sim. quantos"])),

        # Movimentação
        ("mov_entradas_total", (["movimentacao no sistema prisional", "entradas", "numero de inclusoes originarias", "total"], None)),
        ("mov_alvaras_total", (["movimentacao no sistema prisional", "saidas", "alvaras de soltura", "total"], None)),
        ("mov_abandonos_total", (["movimentacao no sistema prisional", "saidas", "abandonos", "total"], None)),
        ("mov_obitos_total", (["movimentacao no sistema prisional", "saidas", "total de obitos", "total"], None)),
        ("mov_transf_in_total", (["movimentacao no sistema prisional", "transferencias/remocoes", "numero de inclusoes por transferencias ou remocoes", "total"], None)),
        ("mov_transf_out_total", (["movimentacao no sistema prisional", "transferencias/remocoes", "deste para outro estabelecimento", "total"], None)),
        ("mov_perm_saida_total", (["movimentacao no sistema prisional", "autorizacoes de saida", "permissao de saida", "total"], None)),
        ("mov_saida_temp_total", (["movimentacao no sistema prisional", "autorizacoes de saida", "saida temporaria", "total"], None)),

        # Faixa etária
        ("idade_18_24_total", (["faixa etaria", "18 a 24 anos", "total"], None)),
        ("idade_25_29_total", (["faixa etaria", "25 a 29 anos", "total"], None)),
        ("idade_30_34_total", (["faixa etaria", "30 a 34 anos", "total"], None)),
        ("idade_35_45_total", (["faixa etaria", "35 a 45 anos", "total"], None)),
        ("idade_46_60_total", (["faixa etaria", "46 a 60 anos", "total"], None)),
        ("idade_61_70_total", (["faixa etaria", "61 a 70 anos", "total"], None)),
        ("idade_70mais_total", (["faixa etaria", "mais de 70 anos", "total"], None)),
        ("idade_nao_info_total", (["faixa etaria", "nao informado", "total"], None)),

        # Raça/cor
        ("raca_branca_total", (["cor de pele/raca/etnia", "branca", "total"], None)),
        ("raca_preta_total", (["cor de pele/raca/etnia", "preta", "total"], None)),
        ("raca_parda_total", (["cor de pele/raca/etnia", "parda", "total"], None)),
        ("raca_amarela_total", (["cor de pele/raca/etnia", "amarela", "total"], None)),
        ("raca_indigena_total", (["cor de pele/raca/etnia", "indigena", "total"], None)),
        ("raca_nao_info_total", (["cor de pele/raca/etnia", "nao informado", "total"], None)),

        # Procedência
        ("proc_urb_interior_masc", (["procedencia", "area urbana - municipios do interior", "masculino"], None)),
        ("proc_urb_interior_fem", (["procedencia", "area urbana - municipios do interior", "feminino"], None)),
        ("proc_urb_rm_masc", (["procedencia", "area urbana - municipios em regioes metropolitanas", "masculino"], None)),
        ("proc_urb_rm_fem", (["procedencia", "area urbana - municipios em regioes metropolitanas", "feminino"], None)),
        ("proc_rural_masc", (["procedencia", "zona rural", "masculino"], None)),
        ("proc_rural_fem", (["procedencia", "zona rural", "feminino"], None)),

        # Estado civil
        ("civil_solteiro_total", (["estado civil", "solteiro/a", "total"], None)),
        ("civil_uniao_total", (["estado civil", "uniao estavel/amasiado", "total"], None)),
        ("civil_casado_total", (["estado civil", "casado/a", "total"], None)),
        ("civil_separado_total", (["estado civil", "separado/a judicialmente", "total"], None)),
        ("civil_divorciado_total", (["estado civil", "divorciado/a", "total"], None)),
        ("civil_viuvo_total", (["estado civil", "viuvo/a", "total"], None)),
        ("civil_nao_info_total", (["estado civil", "nao informado", "total"], None)),

        # Saúde / mortalidade do período
        ("saude_consultas_ext_total", (["informacoes da area de saude - total do periodo", "consultas medicas realizadas externamente", "total"], None)),
        ("saude_consultas_no_estab_total", (["informacoes da area de saude - total do periodo", "consultas medicas realizadas no estabelecimento", "total"], None)),
        ("saude_consultas_psico_total", (["informacoes da area de saude - total do periodo", "consultas psicologicas", "total"], None)),
        ("saude_consultas_odonto_total", (["informacoes da area de saude - total do periodo", "consultas odontologicas", "total"], None)),
        ("saude_exames_total", (["informacoes da area de saude - total do periodo", "quantidade de exames e testagem", "total"], None)),
        ("saude_vacinas_total", (["informacoes da area de saude - total do periodo", "quantidade de vacinas", "total"], None)),
        ("saude_outros_proc_total", (["informacoes da area de saude - total do periodo", "outros procedimentos", "total"], None)),

        ("mortalidade_natural_total", (["mortalidade no sistema prisional", "obitos naturais/ obitos por motivos de saude", "total"], None)),
        ("mortalidade_criminal_total", (["mortalidade no sistema prisional", "obitos criminais", "total"], None)),
        ("mortalidade_suicidio_total", (["mortalidade no sistema prisional", "obitos suicidios", "total"], None)),
        ("mortalidade_acidental_total", (["mortalidade no sistema prisional", "obitos acidentais", "total"], None)),
        ("mortalidade_causa_desconhecida_total", (["mortalidade no sistema prisional", "obitos com causa desconhecida", "total"], None)),
    ]

    mapped = {}
    for alias, (includes, excludes) in patterns:
        mapped[alias] = pick_col(cols, includes, excludes)

    # ---------------------------
    # 2) Construir dataset v3
    # ---------------------------
    out = pd.DataFrame(index=df.index)

    text_fields = [
        "tipo_estabelecimento", "uf", "municipio", "gestao",
        "gestao_saude_terceirizada", "gestao_assist_juridica_terceirizada",
        "saude_nao_possui", "saude_consultorio_medico", "saude_consultorio_odontologico",
        "saude_enfermagem", "saude_farmacia",
        "educacao_nao_possui", "educacao_sala_aula", "educacao_sala_informatica", "educacao_biblioteca",
        "assist_juridica_nao", "assist_juridica_defensoria", "assist_juridica_dativos", "assist_juridica_ong",
        "controle_mais_90_dias", "controle_semiaberto_aguardando_vaga",
    ]

    num_fields = [k for k in mapped.keys() if k not in text_fields]

    for alias in text_fields:
        add_text_if_exists(df, out, mapped.get(alias), alias)

    for alias in num_fields:
        add_numeric_if_exists(df, out, mapped.get(alias), alias)

    # ---------------------------
    # 3) Consolidações e métricas
    # ---------------------------
    # Capacidade total calculada
    cap_parts = [
        "capacidade_provisorios_total",
        "capacidade_fechado_total",
        "capacidade_semiaberto_total",
        "capacidade_aberto_total",
        "capacidade_rdd_total",
        "capacidade_medida_internacao_total",
        "capacidade_outros_total",
    ]
    existing_cap_parts = [c for c in cap_parts if c in out.columns]
    if existing_cap_parts:
        out["capacidade_total_calculada"] = out[existing_cap_parts].fillna(0).sum(axis=1)
    else:
        out["capacidade_total_calculada"] = np.nan

    # População total calculada por regimes
    pop_parts = [
        "pop_provisorios_total",
        "pop_fechado_total",
        "pop_semiaberto_total",
        "pop_aberto_total",
        "pop_internacao_total",
        "pop_tratamento_ambulatorial_total",
    ]
    existing_pop_parts = [c for c in pop_parts if c in out.columns]
    if existing_pop_parts:
        out["pop_total_calculada"] = out[existing_pop_parts].fillna(0).sum(axis=1)
    else:
        out["pop_total_calculada"] = np.nan

    # Escolher pop_total oficial se existir, senão usar calculada
    if "pop_total" in out.columns:
        out["pop_total_final"] = out["pop_total"].fillna(out["pop_total_calculada"])
    else:
        out["pop_total_final"] = out["pop_total_calculada"]

    # Escolher capacidade final
    out["capacidade_total_final"] = out["capacidade_total_calculada"]

    # Taxa de ocupação
    out["taxa_ocupacao"] = np.where(
        out["capacidade_total_final"].fillna(0) > 0,
        out["pop_total_final"] / out["capacidade_total_final"],
        np.nan,
    )

    # Percentuais por regime
    for src, dst in [
        ("pop_provisorios_total", "perc_provisorios"),
        ("pop_fechado_total", "perc_fechado"),
        ("pop_semiaberto_total", "perc_semiaberto"),
        ("pop_aberto_total", "perc_aberto"),
    ]:
        if src in out.columns:
            out[dst] = np.where(out["pop_total_final"].fillna(0) > 0, out[src] / out["pop_total_final"], np.nan)

    # Jovens 18-29
    if {"idade_18_24_total", "idade_25_29_total"}.issubset(out.columns):
        out["pop_18_29_total"] = out["idade_18_24_total"].fillna(0) + out["idade_25_29_total"].fillna(0)
        out["perc_18_29"] = np.where(out["pop_total_final"].fillna(0) > 0, out["pop_18_29_total"] / out["pop_total_final"], np.nan)

    # Parda + preta
    if {"raca_parda_total", "raca_preta_total"}.issubset(out.columns):
        out["raca_parda_preta_total"] = out["raca_parda_total"].fillna(0) + out["raca_preta_total"].fillna(0)
        out["perc_parda_preta"] = np.where(out["pop_total_final"].fillna(0) > 0, out["raca_parda_preta_total"] / out["pop_total_final"], np.nan)

    # Procedência consolidada
    proc_cols = [
        "proc_urb_interior_masc", "proc_urb_interior_fem",
        "proc_urb_rm_masc", "proc_urb_rm_fem",
        "proc_rural_masc", "proc_rural_fem",
    ]
    for c in proc_cols:
        if c not in out.columns:
            out[c] = np.nan

    out["proc_urb_interior_total"] = out[["proc_urb_interior_masc", "proc_urb_interior_fem"]].fillna(0).sum(axis=1)
    out["proc_urb_rm_total"] = out[["proc_urb_rm_masc", "proc_urb_rm_fem"]].fillna(0).sum(axis=1)
    out["proc_rural_total"] = out[["proc_rural_masc", "proc_rural_fem"]].fillna(0).sum(axis=1)

    # Flags úteis
    if "taxa_ocupacao" in out.columns:
        out["flag_superlotacao"] = np.where(out["taxa_ocupacao"] > 1, 1, 0)

    if "saude_nao_possui" in out.columns:
        out["flag_sem_modulo_saude"] = out["saude_nao_possui"].astype(str).str.strip().str.lower().map({"sim": 1, "não": 0, "nao": 0})

    if "educacao_nao_possui" in out.columns:
        out["flag_sem_modulo_educacao"] = out["educacao_nao_possui"].astype(str).str.strip().str.lower().map({"sim": 1, "não": 0, "nao": 0})

    if "assist_juridica_defensoria" in out.columns:
        out["flag_assist_juridica_defensoria"] = out["assist_juridica_defensoria"].astype(str).str.strip().str.lower().map({"sim": 1, "não": 0, "nao": 0})

    # ---------------------------
    # 4) Ordenação final
    # ---------------------------
    preferred_order = [
        # Identificação
        "tipo_estabelecimento", "uf", "municipio", "gestao",

        # Capacidade e população
        "capacidade_total_final", "capacidade_total_calculada", "vagas_desativadas_total",
        "capacidade_masculino_total", "capacidade_feminino_total",
        "capacidade_provisorios_total", "capacidade_fechado_total", "capacidade_semiaberto_total",
        "capacidade_aberto_total", "capacidade_rdd_total", "capacidade_medida_internacao_total", "capacidade_outros_total",

        "pop_total_final", "pop_total", "pop_total_calculada",
        "pop_provisorios_total", "pop_fechado_total", "pop_semiaberto_total", "pop_aberto_total",
        "pop_internacao_total", "pop_tratamento_ambulatorial_total", "pop_rdd_total",

        # KPIs
        "taxa_ocupacao", "flag_superlotacao",
        "perc_provisorios", "perc_fechado", "perc_semiaberto", "perc_aberto",

        # Movimentação
        "mov_entradas_total", "mov_alvaras_total", "mov_abandonos_total", "mov_obitos_total",
        "mov_transf_in_total", "mov_transf_out_total", "mov_perm_saida_total", "mov_saida_temp_total",

        # Perfil
        "pop_18_29_total", "perc_18_29",
        "idade_18_24_total", "idade_25_29_total", "idade_30_34_total", "idade_35_45_total",
        "idade_46_60_total", "idade_61_70_total", "idade_70mais_total", "idade_nao_info_total",

        "raca_parda_preta_total", "perc_parda_preta",
        "raca_branca_total", "raca_preta_total", "raca_parda_total", "raca_amarela_total",
        "raca_indigena_total", "raca_nao_info_total",

        "proc_urb_interior_total", "proc_urb_rm_total", "proc_rural_total",

        "civil_solteiro_total", "civil_uniao_total", "civil_casado_total",
        "civil_separado_total", "civil_divorciado_total", "civil_viuvo_total", "civil_nao_info_total",

        # Estrutura
        "gestao_saude_terceirizada", "gestao_assist_juridica_terceirizada",
        "saude_nao_possui", "saude_consultorio_medico", "saude_consultorio_odontologico",
        "saude_enfermagem", "saude_farmacia", "flag_sem_modulo_saude",
        "educacao_nao_possui", "educacao_sala_aula", "educacao_sala_informatica",
        "educacao_biblioteca", "flag_sem_modulo_educacao",
        "assist_juridica_nao", "assist_juridica_defensoria", "assist_juridica_dativos",
        "assist_juridica_ong", "flag_assist_juridica_defensoria",

        # Saúde do período / mortalidade
        "saude_consultas_ext_total", "saude_consultas_no_estab_total", "saude_consultas_psico_total",
        "saude_consultas_odonto_total", "saude_exames_total", "saude_vacinas_total", "saude_outros_proc_total",
        "mortalidade_natural_total", "mortalidade_criminal_total", "mortalidade_suicidio_total",
        "mortalidade_acidental_total", "mortalidade_causa_desconhecida_total",

        # Controle
        "controle_mais_90_dias", "controle_semiaberto_aguardando_vaga",
    ]

    final_cols = [c for c in preferred_order if c in out.columns] + [c for c in out.columns if c not in preferred_order]
    out = out[final_cols]

    # Remover colunas 100% vazias na v3
    non_empty_cols = []
    for c in out.columns:
        s = out[c]
        if s.isna().all():
            continue
        if s.dtype == object and s.fillna("").astype(str).str.strip().eq("").all():
            continue
        non_empty_cols.append(c)
    out = out[non_empty_cols]

    # ---------------------------
    # 5) Saída e resumo
    # ---------------------------
    out.to_csv(OUT, sep=";", index=False, encoding="utf-8")

    print("=" * 80)
    print("DATASET SEMINARIO V3 GERADO")
    print("=" * 80)
    print(f"Arquivo origem : {SRC.resolve()}")
    print(f"Arquivo saída  : {OUT.resolve()}")
    print(f"Linhas         : {len(out):,}".replace(",", "."))
    print(f"Colunas finais : {len(out.columns):,}".replace(",", "."))
    print()

    print("Primeiras 20 colunas:")
    for i, c in enumerate(out.columns[:20], start=1):
        print(f"{i:02d}. {c}")

    print()
    print("Preview:")
    pd.set_option("display.max_columns", 12)
    pd.set_option("display.width", 180)
    print(out.head(5).to_string(index=False))


if __name__ == "__main__":
    main()