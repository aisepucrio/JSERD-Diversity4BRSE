import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

# Create output directory if it doesn't exist
output_dir = '../../results/RQ2'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def split_disc(texto):
    if not isinstance(texto, str):
        return []
    return re.split(r',\s(?=\w+\s?\()', texto)

df = pd.read_csv("../../data/analysis_i&d_up.csv")

col_seniority = "Por favor indique a senioridade do posição que ocupa.  "
col_race = "Como voce se autodeclara?"
col_pcd = "Você é uma pessoa com deficiência? "
col_gen = "Como você se identifica em relação à sua identidade de gênero?"
col_sex = "Como você se identifica em relação à sua orientação sexual?  "
col_disc = "Qual(is) dos tipos de discriminação você acha que são mais recorrentes dentro da área de desenvolvimento de software?"

df = df[[col_gen, col_sex, col_race, col_pcd, col_seniority,col_disc]].dropna()
df[col_disc] = df[col_disc].apply(split_disc)
df = df.explode(col_disc)
df[col_disc] = df[col_disc].str.strip()

gender_map = {
    "homem cisgênero": "Men",
    "homem trans": "Men",
    "mulher cisgênero": "Women",
    "mulher trans": "Women",
}

def mapping_gender(val):
    if not isinstance(val, str):
        return 
    val = val.strip().lower()
    return gender_map.get(val)

df["Gender Agg"] = df[col_gen].apply(mapping_gender)

sexuality_map = {
    "heterossexual": "Heterosexual",
    "homossexual": "LGBTQ+",
    "bissexual": "LGBTQ+",
    "pansexual": "LGBTQ+",
}

def mapping_sexuality(val):
    if not isinstance(val, str):
        return
    val = val.strip().lower()
    return sexuality_map.get(val)

df["Sexuality Agg"] = df[col_sex].apply(mapping_sexuality)

def mapear_pcd(val):
    if not isinstance(val, str):
        return
    val = val.strip().lower()
    if val.startswith("sim"):
        return "Disabled"
    elif "não" in val:
        return "Not disabled"
    else:
        return "Disabled"

df["PCD"] = df[col_pcd].apply(mapear_pcd)

mapa_raca = {
    "preto(a)": "PoC",
    "branco(a)": "White",
    "pardo(a)": "PoC",
    "indígena": "PoC",
}

def mapear_raca(val):
    if not isinstance(val, str):
        return
    val = val.strip().lower()
    return mapa_raca.get(val)

df["Race Agg"] = df[col_race].apply(mapear_raca)

mapa_senioridade = {
    "estagiário": "Intern",
    "júnior (até 5 anos)": "Junior",
    "pleno (6 a 9 anos)": "Mid-level",
    "sênior (10+ anos)": "Senior"
}

def mapear_senioridade(val):
    if not isinstance(val, str):
        return
    val = val.strip().lower()
    return mapa_senioridade.get(val)

df["Seniority Agg"] = df[col_seniority].apply(mapear_senioridade)

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

def mapping_disc(val):
    if not isinstance(val, str):
        return
    val = val.strip()
    tipo = val.split("(")[0].strip()
    return tipos_traduzidos.get(tipo)

df["Disc Label"] = df[col_disc].apply(mapping_disc)

df_genero = df.rename(columns={"Gender Agg": "Profile"})[["Profile", "Disc Label"]]
df_pcd = df.rename(columns={"PCD": "Profile"})[["Profile", "Disc Label"]]
df_sexualidade = df.rename(columns={"Sexuality Agg": "Profile"})[["Profile", "Disc Label"]]
df_raca = df.rename(columns={"Race Agg": "Profile"})[["Profile", "Disc Label"]]
df_senioridade = df.rename(columns={"Seniority Agg": "Profile"})[["Profile", "Disc Label"]]
df_total = df.copy()
df_total["Profile"] = "Total (overall)"

df_final = pd.concat([
    df_genero,
    df_sexualidade,
    df_raca,
    df_senioridade,
    df_pcd,
    df_total[["Profile", "Disc Label"]]
], ignore_index=True)

df_resp = pd.read_csv("../../data/analysis_i&d_up.csv")
df_resp["Gender Agg"] = df_resp[col_gen].apply(mapping_gender)
df_resp["Sexuality Agg"] = df_resp[col_sex].apply(mapping_sexuality)
df_resp["Race Agg"] = df_resp[col_race].apply(mapear_raca)
df_resp["Seniority Agg"] = df_resp[col_seniority].apply(mapear_senioridade)
df_resp["PCD"] = df_resp[col_pcd].apply(mapear_pcd)

total_por_Profile = {}
for g in df_resp["Gender Agg"].unique():
    total_por_Profile[g] = len(df_resp[df_resp["Gender Agg"] == g])
for s in df_resp["Sexuality Agg"].unique():
    total_por_Profile[s] = len(df_resp[df_resp["Sexuality Agg"] == s])
for r in df_resp["Race Agg"].unique():
    total_por_Profile[r] = len(df_resp[df_resp["Race Agg"] == r])
for s in df_resp["Seniority Agg"].unique():
    total_por_Profile[s] = len(df_resp[df_resp["Seniority Agg"] == s])
for d in df_resp["PCD"].unique():
    total_por_Profile[d] = len(df_resp[df_resp["PCD"] == d])
total_por_Profile["Total (overall)"] = len(df_resp)

counts = df_final.groupby(["Profile", "Disc Label"]).size().reset_index(name="count")
counts["percent"] = counts.apply(
    lambda row: (row["count"] / total_por_Profile.get(row["Profile"], 1)) * 100,
    axis=1
)

disc_order = ["Ableism", "Ageism", "Elitism", "Homophobia", "Racism", "Sexism"]
heatmap_data = counts.pivot_table(
    index="Profile",
    columns="Disc Label",
    values="percent",
    fill_value=0
)

heatmap_data = heatmap_data[disc_order]

profile_order = [
    "Women", "Men",
    "Heterosexual", "LGBTQ+",
    "White", "PoC",
    "Intern", "Junior", "Mid-level", "Senior",
    "Not disabled", "Disabled",
    "Total (overall)"
]

heatmap_data = heatmap_data.reindex(profile_order)

plt.figure(figsize=(10,7))
sns.heatmap(
    heatmap_data,
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
plt.savefig(f'{output_dir}/profile.png', dpi=300, bbox_inches='tight')
plt.show()