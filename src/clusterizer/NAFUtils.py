import pandas as pd

def charger():
    """
    Charge le fichier de description des codes NAF

    :return: la DataFrame correspondante.
    """
    return pd.read_csv("..\\ressources\\naf_descriptions.csv", sep=";", encoding='utf8')

df_naf_descriptions = charger()

def get_description(code_naf):
    """
    Fournit la description correspondant au code NAF.

    :param code_naf: le code, avec ou sans point.
    :return: la description complète.
    """
    if code_naf[2] != ".":
        # Convention sans point
        code_naf = code_naf[0] + code_naf[1] + "." + code_naf[2:]
    return df_naf_descriptions[df_naf_descriptions["code"] == code_naf].reset_index().loc[0, "description"]