import pandas as pd

import sys
sys.path.append("../..")

from src.clusterizer import clusterizer
from src.clusterizer.utils import clusterizer_utils
from src.clusterizer.utils import NAF_utils

df_test = clusterizer.nettoyer(pd.read_json("../../data/base_sirene_shortened.json"), reduce=True, threshold=2)

def test_calculer_poids_cluster():
    """ 
    Teste la fonction calculer_poids_cluster du module clusterizer_utils sur la Dataframe df_test, composée de deux établissements
    """
    result = clusterizer_utils.calculer_poids_cluster(df_test, "apet700")
    assert result == 2  # pour l'instant chaque établissement a un poids de 1

def test_ajouter_point():
    """ 
    Teste la fonction ajouter_point du module NAF_utils sur le code NAF sans point "6820A" 
    """
    result = NAF_utils.ajouter_point("6820A")
    assert result == "68.20A"

def test_retirer_point():
    """ 
    Teste la fonction retirer_point du module NAF_utils sur le code NAF avec point "68.20A" 
    """
    result = NAF_utils.retirer_point("68.20A")
    assert result == "6820A"

def test_get_description():
    """ 
    Teste la fonction get_description du module NAF_utils sur le code NAF "011", qui correspond à l'activitée "Cultures non permanentes" 
    """
    result = NAF_utils.get_description("011")
    assert result == "Cultures non permanentes"

def test_get_NAFs_by_section():
    """ 
    Teste la fonction get_NAFs_by_section du module NAF_utils sur la section "D"
    """
    result = NAF_utils.get_NAFs_by_section("D")
    print(result)
    assert (result == ["35", "35.1", "35.11", "35.11Z", "35.12", "35.12Z", "35.13", "35.13Z", "35.14", "35.14Z", "35.2", "35.21", "35.21Z", "35.22", "35.22Z", "35.23", "35.23Z", "35.3", "35.30", "35.30Z" ]).all


df_test_cl, df_test_infos = clusterizer.clusterize(df_test, 1, "geometry", is_dict=True)

def test_numero_cluster():
    """ 
    Teste l'ajout des numéros de clusters pour chaque point à la fin du clustering, dans un cas très simple à deux établissements et un seul cluster.
    """
    assert (df_test_cl["cluster"] == [0, 0]).all  # les deux établissements sont dans le premier (et seul) cluster

def test_get_infos_clusters_taille():
    """ 
    Teste la fonction get_infos_clusters_taille du module clusterizer_utils, dans un cas très simple à deux établissements et un seul cluster.
    """
    result = clusterizer_utils.get_infos_clusters_taille(df_test_cl)
    assert (result == [2]).all   # un seul cluster, contenant deux établisseùents

def test_centre_de_masse():
    """ 
    Teste le calcul du centre de masse des clusters à la fin du clustering, dans un cas très simple à deux établissements et un seul cluster.
    """
    assert (df_test_infos["centroids"] == [{(2.348872+2.297082)/2, (48.863495+48.881103)/2}]).all