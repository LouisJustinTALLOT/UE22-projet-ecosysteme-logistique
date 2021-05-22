import pandas as pd
import numpy as np

#==============================================================
# Cette DataFrame contient toutes les descrptions des codes NAF
#==============================================================
df_naf_descriptions = pd.read_csv("..\\ressources\\naf_descriptions.csv", sep=";", encoding='utf8')

#==============================================================
# Cette fonction permet de vérifier l'appartenance (vectorisée)
#==============================================================
vectorized_belongs = np.vectorize(lambda code, codes_naf : code in codes_naf)


def get_description(code_naf):
    """
    Fournit la description correspondant au code NAF.

    :param code_naf: le code, avec ou sans point.
    :return: la description complète.
    """
    code_naf = ajouter_point(code_naf)
    return df_naf_descriptions[df_naf_descriptions["code"] == code_naf].reset_index().loc[0, "description"]

def filter_by_naf(df, codes_naf, column_codes):
    """
    Retourne les établissements dont le code NAF est contenu dans la liste.

    :param df: La liste des établissements
    :param codes_naf: Le code NAF (avec ou sans le point)
    :param column_codes: La colonne où est située le code NAF dans la DataFrame des établissements
    :return: La DataFrame filtrée.
    """
    return df[vectorized_belongs(df[column_codes], codes_naf)].reset_index()



# ====== FONCTION DE CONVENTIONS ======

def ajouter_point(code_naf):
    """
    Fait passer le code NAF à la convention avec point (s'il n'y est pas)

    :param code_naf: Le code à changer
    :return: Le code avec un point.
    """
    if code_naf[2] != ".":
        # Il n'y a pas de point, on l'ajoute
        return code_naf[0] + code_naf[1] + "." + code_naf[2:]

def retirer_point(code_naf):
    """
    Fait passer le code NAF à la convention sans point (s'il y est)

    :param code_naf: Le code à changer
    :return: Le code sans point.
    """
    if code_naf[2] == ".":
        # Il y a un point, on le retire
        return code_naf[0] + code_naf[1] + code_naf[3:]

