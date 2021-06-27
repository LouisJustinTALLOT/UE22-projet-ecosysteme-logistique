import pandas as pd
import numpy as np

#==================================================================================
# Fonctions pour switcher les conventions de NAF (avec ou sans point intermédiaire)
#==================================================================================

def ajouter_point(code_naf):
    """
    Fait passer le code NAF à la convention avec point (s'il n'y est pas)

    :param code_naf: Le code à changer
    :return: Le code avec un point.
    """
    if code_naf is None or len(code_naf) < 3:
        # S'il ne s'agit pas d'un code NAF, on ne fait rien
        return code_naf

    if code_naf[2] != ".":
        # Il n'y a pas de point, on l'ajoute
        return code_naf[0] + code_naf[1] + "." + code_naf[2:]

def retirer_point(code_naf):
    """
    Fait passer le code NAF à la convention sans point (s'il y est)

    :param code_naf: Le code à changer
    :return: Le code sans point.
    """
    if code_naf is None or len(code_naf) < 3:
        # S'il ne s'agit pas d'un code NAF, on ne fait rien
        return code_naf

    if code_naf[2] == ".":
        # Il y a un point, on le retire
        return code_naf[0] + code_naf[1] + code_naf[3:]

#==============================================================
# Cette DataFrame contient toutes les descrptions des codes NAF
#==============================================================
df_naf_descriptions = pd.read_csv("..\\..\\src\\ressources\\naf_descriptions.csv", sep=";", encoding='utf8')

#==============================================================
# Fonctions vectorisées
#==============================================================
vectorized_belongs = np.vectorize(lambda code, codes_naf : code in codes_naf, excluded=[1])
vectorized_starts_with = np.vectorize(lambda str1, str2: str(str1).startswith(str2), excluded=[1])
vectorized_retirer_points = np.vectorize(retirer_point)

#==============================================================
# Fonctions utiles pour le projet
#==============================================================

def get_description(code_naf):
    """
    Fournit la description correspondant au code NAF.

    :param code_naf: le code, avec ou sans point.
    :return: la description complète.
    """
    code_naf = ajouter_point(code_naf)
    return df_naf_descriptions[df_naf_descriptions["code"] == code_naf].reset_index(drop=True).loc[0, "description"]

def get_NAFs_by_section(section):
    """
    Fournit la liste des codes NAF de la section correspondante.

    :param section: La lettre de la section
    :returns La liste des codes NAF contenus dans la section (convention : avec points)
    """ 
    masque = df_naf_descriptions["code"] == ("SECTION " + section)
    # normalement ce masque n'est à True qu'à un seul endroit
    # du coup, comme True=1, on utilise cette astuce pour récupérer l'indice de la ligne
    debut_section = np.argmax(masque) + 1

    masque = vectorized_starts_with(df_naf_descriptions["code"], "SECTION")
    longueur_section = np.argmax(masque[debut_section:])

    fin_section = debut_section + longueur_section
    # debut_section est inclusif, fin_section exclusif

    return df_naf_descriptions["code"][debut_section:fin_section].dropna()

def filter_by_naf(df, codes_naf, column_codes):
    """
    Retourne les établissements dont le code NAF est contenu dans la liste.

    :param df: La liste des établissements (convention NAF : sans le point)
    :param codes_naf: Les codes NAF (avec ou sans le point) (sous forme de liste)
    :param column_codes: La colonne où est située le code NAF dans la DataFrame des établissements
    :return: La DataFrame filtrée.
    """
    return df[vectorized_belongs(df[column_codes], vectorized_retirer_points(codes_naf))].reset_index(drop=True)