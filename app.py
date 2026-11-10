import pandas as pd
import json

def extrair():
    # 1. Detectar o separador automaticamente e ler o arquivo
    with open("Tabela_Escola_2025_V2.csv", 'r', encoding='latin1') as f:
        linha = f.readline()
    separador = ';' if ';' in linha else ','
    
    df = pd.read_csv("Tabela_Escola_2025_V2.csv", sep=separador, encoding="latin1", low_memory=False)
    
    # 2. Limpar os nomes de todas as colunas
    df.columns = (
        df.columns.astype(str)
        .str.replace('\ufeff', '', regex=False)
        .str.lower()
        .str.replace('"', '', regex=False)
        .str.strip()
    )

    # 3. Filtrar a Paraíba
    df_pb = df[df["sg_uf"] == "PB"].copy()

    campos_exigidos = [
        "no_entidade", "co_entidade", "no_uf", "sg_uf", "co_uf",
        "no_municipio", "co_municipio", "no_mesorregiao", "co_mesorregiao",
        "no_microrregiao", "co_microrregiao", "nu_ano_censo", "no_regiao",
        "co_regiao", "qt_mat_bas", "qt_mat_inf", "qt_mat_fund",
        "qt_mat_med", "qt_mat_prof", "qt_mat_eja", "qt_mat_esp"
    ]

    # 4. Garantir que as colunas existam
    for campo in campos_exigidos:
        if campo not in df_pb.columns:
            df_pb[campo] = 0

    # 5. Forçar a conversão de matrículas removendo pontos (ex: 1.500 -> 1500)
    colunas_mat = [c for c in campos_exigidos if c.startswith("qt_mat")]
    for col in colunas_mat:
        df_pb[col] = (
            df_pb[col].astype(str)
            .str.replace('.', '', regex=False) # Remove pontos
            .str.replace(',', '.', regex=False)
            .str.strip()
            .replace('nan', '0')
            .replace('None', '0')
            .replace('', '0')
        )
        # Transforma finalmente em número inteiro
        df_pb[col] = pd.to_numeric(df_pb[col], errors="coerce").fillna(0).astype(int)

    # 6. Ordenar as maiores e salvar
    df_pb = df_pb[campos_exigidos]
    df_pb = df_pb.sort_values(by="qt_mat_bas", ascending=False)
    
    # Nome do arquivo exatamente como você tem no import do React
    df_pb.to_json("ie_paraiba_2025.json", orient="records", force_ascii=False, indent=2)
    
    print("\n--- RESULTADO DA EXTRAÇÃO NO PYTHON ---")
    print(df_pb[["no_entidade", "no_municipio", "qt_mat_bas"]].head(5))
    print("\nExtração finalizada!")

if __name__ == "__main__":
    extrair()