import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

# Create output directory if it doesn't exist
output_dir = '../../results/RQ3'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def split_discriminacoes(texto):
    if not isinstance(texto, str):
        return []
    return re.split(r',\s(?=\w+\s?\()', texto)

df = pd.read_csv("../../data/analysis_i&d_up.csv")

col_model = "Qual seu modelo de trabalho?"
col_setor = "Qual o setor da organização para qual você trabalha atualmente?"
col_tam = "Qual o tamanho da empresa para a qual você trabalha atualmente?"
col_discriminacao = "Qual(is) dos tipos de discriminação você acha que são mais recorrentes dentro da área de desenvolvimento de software?"

df = df[[col_setor, col_tam, col_model,col_discriminacao]].dropna()
df[col_discriminacao] = df[col_discriminacao].apply(split_discriminacoes)
df = df.explode(col_discriminacao)
df[col_discriminacao] = df[col_discriminacao].str.strip()

mapa_modelo = {
    "presencial": "On-site",
    "remoto": "Remote",
    "hibrido": "Hybrid"
}

mapa_setor = {
    "setor público": "Public",
    "setor privado": "Private",
    "organização não governamental": "Non-profit / NGO",
    "organização sem fins lucrativos": "Non-profit / NGO",
    "startup": "Startup"
}

mapa_tamanho = {
    "até 9": "Small company",
    "de 10 a 49": "Small company",
    "de 50 a 99": "Small company",
    "de 100 a 499": "Big company",
    "de 500 a 999": "Big company",
    "mais de 1000": "Big company"
}

tipos_validos = [
    "Etarismo", "Machismo", "Homofobia",
    "Racismo", "Elitismo", "Capacitismo"
]
tipos_traduzidos = {
    "Etarismo": "Ageism",
    "Machismo": "Sexism",
    "Homofobia": "Homophobia",
    "Racismo": "Racism",
    "Elitismo": "Elitism",
    "Capacitismo": "Ableism"
}

def mapear_discriminacao(val):
    if not isinstance(val, str):
        return
    val = val.strip()
    tipo = val.split("(")[0].strip()
    return tipos_traduzidos.get(tipo)

df["Discriminação Label"] = df[col_discriminacao].apply(mapear_discriminacao)

df[col_model] = df[col_model].str.strip().str.lower().map(mapa_modelo).fillna("Others")
df[col_setor] = df[col_setor].str.strip().str.lower().map(mapa_setor).fillna("Others")
df[col_tam] = df[col_tam].str.strip().str.lower().map(mapa_tamanho).fillna("Others")


df_modelo = df.rename(columns={col_model: "Perfil"})[["Perfil", "Discriminação Label"]]
df_setor = df.rename(columns={col_setor: "Perfil"})[["Perfil", "Discriminação Label"]]
df_tamanho = df.rename(columns={col_tam: "Perfil"})[["Perfil", "Discriminação Label"]]
df_total_org = df.copy()
df_total_org["Perfil"] = "Total (overall)"

df_final_org = pd.concat([
    df_modelo,
    df_setor,
    df_tamanho,
    df_total_org[["Perfil", "Discriminação Label"]]
], ignore_index=True)


df_resp = pd.read_csv("../../data/analysis_i&d_up.csv")
total_por_perfil_org = {}
df_resp[col_model] = df_resp[col_model].str.strip().str.lower().map(mapa_modelo).fillna("Others")
df_resp[col_setor] = df_resp[col_setor].str.strip().str.lower().map(mapa_setor).fillna("Others")
df_resp[col_tam] = df_resp[col_tam].str.strip().str.lower().map(mapa_tamanho).fillna("Others")

for c in [col_model, col_setor, col_tam]:
    for val in df_resp[c].dropna().unique():
        total_por_perfil_org[val] = len(df_resp[df_resp[c] == val])

total_por_perfil_org["Total (overall)"] = len(df_resp)


counts_org = df_final_org.groupby(["Perfil", "Discriminação Label"]).size().reset_index(name="count")
counts_org["percent"] = counts_org.apply(
    lambda row: (row["count"] / total_por_perfil_org.get(row["Perfil"], 1)) * 100,
    axis=1
)

ordem_discriminacao = ["Ableism", "Ageism", "Elitism", "Homophobia", "Racism", "Sexism"]
heatmap_data_org = counts_org.pivot_table(
    index="Perfil",
    columns="Discriminação Label",
    values="percent",
    fill_value=0
)

heatmap_data_org = heatmap_data_org[ordem_discriminacao]

ordem_perfis = [
    "Big company", "Small company",
    "On-site", "Remote", "Hybrid",
    "Public", "Private", "Non-profit / NGO",
    "Total (overall)"
]

heatmap_data_org = heatmap_data_org.reindex(ordem_perfis)

plt.figure(figsize=(10,7))
sns.heatmap(
    heatmap_data_org,
    annot=True,
    fmt=".1f",
    cmap="Reds",
    linewidths=.5,
    annot_kws={'size': 14},
    cbar_kws={'label': '% of respondents'}
)

plt.xticks(rotation=0, ha='center', fontsize=12)
plt.yticks(rotation=0, fontsize=12)
plt.tight_layout()
plt.savefig(f'{output_dir}/company.png', dpi=300, bbox_inches='tight')
plt.show()
