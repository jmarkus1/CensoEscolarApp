import os
import pandas as pd

CAMPOS_EXIGIDOS = [
    "no_entidade", "co_entidade", "no_uf", "sg_uf", "co_uf",
    "no_municipio", "co_municipio", "no_mesorregiao", "co_mesorregiao",
    "no_microrregiao", "co_microrregiao", "nu_ano_censo", "no_regiao",
    "co_regiao", "qt_mat_bas", "qt_mat_inf", "qt_mat_fund",
    "qt_mat_med", "qt_mat_prof", "qt_mat_eja", "qt_mat_esp"
]

COLUNAS_MAT_ALVO = [
    "qt_mat_bas", "qt_mat_inf", "qt_mat_fund",
    "qt_mat_med", "qt_mat_prof", "qt_mat_eja", "qt_mat_esp"
]

def detectar_sep_e_colunas(caminho):
    with open(caminho, "r", encoding="latin1") as f:
        primeira = f.readline()
    sep = ";" if ";" in primeira else ","
    cols_orig = pd.read_csv(caminho, sep=sep, encoding="latin1", nrows=0).columns
    cols_limpas = (
        cols_orig.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.lower()
        .str.replace('"', "", regex=False)
        .str.strip()
        .tolist()
    )
    return sep, list(cols_orig), cols_limpas

def extrair():
    csvs = [f for f in os.listdir(".") if f.lower().endswith(".csv")]
    print("CSVs encontrados na pasta:", csvs)

    csv_escola = next((f for f in csvs if "escola" in f.lower()), None)
    csv_mat = next((f for f in csvs if "matricula" in f.lower() or "turma" in f.lower()), None)

    if not csv_escola or not csv_mat:
        print("ERRO: Certifique-se de que Tabela_Escola e Tabela_Matricula estão na pasta.")
        return

    # 1. Carregar escolas da Paraíba
    sep_esc, cols_orig_esc, cols_limpas_esc = detectar_sep_e_colunas(csv_escola)
    usar_esc = [o for o, l in zip(cols_orig_esc, cols_limpas_esc) if l in CAMPOS_EXIGIDOS]
    df_esc = pd.read_csv(csv_escola, sep=sep_esc, encoding="latin1", usecols=usar_esc, low_memory=False)
    df_esc.columns = [c.replace("\ufeff", "").lower().replace('"', "").strip() for c in df_esc.columns]

    df_pb = df_esc[df_esc["sg_uf"].astype(str).str.strip().str.upper() == "PB"].copy()
    df_pb["co_entidade"] = pd.to_numeric(df_pb["co_entidade"], errors="coerce").fillna(0).astype("int64")
    codigos_pb = set(df_pb["co_entidade"])

    # 2. Inspecionar colunas reais de Tabela_Matricula_2025_V2.csv
    sep_mat, cols_orig_mat, cols_limpas_mat = detectar_sep_e_colunas(csv_mat)
    print(f"Colunas de '{csv_mat}':", cols_limpas_mat)

    if "co_entidade" not in cols_limpas_mat:
        print("ERRO: Coluna 'co_entidade' não encontrada no arquivo de matrículas.")
        return

    # Caso A: Tabela_Matricula já traz as colunas agregadas qt_mat_*
    cols_qt_presentes = [c for c in COLUNAS_MAT_ALVO if c in cols_limpas_mat]
    if cols_qt_presentes:
        print(f"Lendo colunas agregadas encontradas: {cols_qt_presentes}...")
        desejadas = {"co_entidade", *cols_qt_presentes}
        usar_mat = [o for o, l in zip(cols_orig_mat, cols_limpas_mat) if l in desejadas]

        partes = []
        for chunk in pd.read_csv(csv_mat, sep=sep_mat, encoding="latin1", usecols=usar_mat, chunksize=250_000, low_memory=False):
            chunk.columns = [c.replace("\ufeff", "").lower().replace('"', "").strip() for c in chunk.columns]
            chunk["co_entidade"] = pd.to_numeric(chunk["co_entidade"], errors="coerce").fillna(0).astype("int64")
            chunk = chunk[chunk["co_entidade"].isin(codigos_pb)].copy()
            if chunk.empty:
                continue
            for col in cols_qt_presentes:
                chunk[col] = pd.to_numeric(chunk[col], errors="coerce").fillna(0).astype(int)
            partes.append(chunk)

        if not partes:
            print("ERRO: Nenhuma linha encontrada para escolas da PB.")
            return

        df_mat_pb = pd.concat(partes, ignore_index=True).groupby("co_entidade", as_index=False).sum()
        df_pb = df_pb.merge(df_mat_pb, on="co_entidade", how="left")
        finalizar_exportacao(df_pb)
        return

    # Caso B: Tabela_Matricula traz registros individuais por aluno/etapa
    col_etapa = next((c for c in cols_limpas_mat if "etapa" in c), None)
    col_esp = next((c for c in cols_limpas_mat if "especial" in c), None)
    col_qtd = next((c for c in cols_limpas_mat if c in {"qt_matriculas", "nu_matriculas", "qt_mat"}), None)

    if not col_etapa and not col_qtd:
        print("\nAVISO: Não identifiquei colunas de etapa ou quantidade automaticamente.")
        print("Copie a lista 'Colunas de Tabela_Matricula_2025_V2.csv' acima para ajustarmos.")
        return

    desejadas = {"co_entidade"}
    for c in (col_etapa, col_esp, col_qtd):
        if c:
            desejadas.add(c)
    usar_mat = [o for o, l in zip(cols_orig_mat, cols_limpas_mat) if l in desejadas]

    print(f"Agregando '{csv_mat}' em blocos (etapa={col_etapa}, especial={col_esp}, qtd={col_qtd})...")
    contagens = {}
    for chunk in pd.read_csv(csv_mat, sep=sep_mat, encoding="latin1", usecols=usar_mat, chunksize=250_000, low_memory=False):
        chunk.columns = [c.replace("\ufeff", "").lower().replace('"', "").strip() for c in chunk.columns]
        chunk["co_entidade"] = pd.to_numeric(chunk["co_entidade"], errors="coerce").fillna(0).astype("int64")
        chunk = chunk[chunk["co_entidade"].isin(codigos_pb)]
        if chunk.empty:
            continue

        if col_qtd and col_qtd in chunk.columns:
            peso = pd.to_numeric(chunk[col_qtd], errors="coerce").fillna(0).astype(int)
        else:
            peso = pd.Series(1, index=chunk.index)

        if col_etapa and col_etapa in chunk.columns:
            etapa = pd.to_numeric(chunk[col_etapa], errors="coerce").fillna(0).astype(int)
        else:
            etapa = pd.Series(0, index=chunk.index)

        if col_esp and col_esp in chunk.columns:
            eh_esp = pd.to_numeric(chunk[col_esp], errors="coerce").fillna(0).astype(int) == 1
        else:
            eh_esp = pd.Series(False, index=chunk.index)

        temp = pd.DataFrame({
            "co_entidade": chunk["co_entidade"],
            "qt_mat_bas": peso,
            "qt_mat_inf": peso.where(etapa.isin([1, 2, 3]), 0),
            "qt_mat_fund": peso.where(etapa.isin(list(range(4, 22)) + [41]), 0),
            "qt_mat_med": peso.where(etapa.isin(range(25, 39)), 0),
            "qt_mat_prof": peso.where(etapa.isin([30, 31, 32, 33, 34, 39, 40, 64, 68]), 0),
            "qt_mat_eja": peso.where(etapa.isin([65, 67, 69, 70, 71, 72, 73, 74]), 0),
            "qt_mat_esp": peso.where(eh_esp, 0),
        })

        agrupado = temp.groupby("co_entidade").sum()
        for co_ent, row in agrupado.iterrows():
            if co_ent not in contagens:
                contagens[co_ent] = row.to_dict()
            else:
                for k in row.index:
                    contagens[co_ent][k] += int(row[k])

    if not contagens:
        print("ERRO: Nenhuma matrícula encontrada para escolas da PB.")
        return

    df_mat_pb = pd.DataFrame.from_dict(contagens, orient="index").reset_index().rename(columns={"index": "co_entidade"})
    df_pb = df_pb.merge(df_mat_pb, on="co_entidade", how="left")
    finalizar_exportacao(df_pb)

def finalizar_exportacao(df_pb):
    campos_texto = {
        "no_entidade", "no_uf", "sg_uf", "no_municipio",
        "no_mesorregiao", "no_microrregiao", "no_regiao"
    }
    for campo in CAMPOS_EXIGIDOS:
        if campo not in df_pb.columns:
            df_pb[campo] = "" if campo in campos_texto else 0

    for col in COLUNAS_MAT_ALVO:
        df_pb[col] = pd.to_numeric(df_pb[col], errors="coerce").fillna(0).astype(int)

    df_pb = df_pb[CAMPOS_EXIGIDOS].sort_values(by="qt_mat_bas", ascending=False)
    df_pb.to_json("ie_paraiba_2025.json", orient="records", force_ascii=False, indent=2)

    print("\n--- TOP 10 ESCOLAS DA PARAÍBA (CENSO 2025) ---")
    print(df_pb[["no_entidade", "no_municipio", "qt_mat_bas"]].head(10).to_string(index=False))
    print(f"\nSucesso! {len(df_pb)} escolas exportadas para 'ie_paraiba_2025.json'.")

if __name__ == "__main__":
    extrair()