import pandas as pd

import sys
sys.path.append("../..")

from src.clusterizer import clusterizer
from src.clusterizer.utils import clusterizer_utils
from src.clusterizer.utils import NAF_utils

df_test = clusterizer.nettoyer(pd.read_json("../../data/base_sirene_shortened.json"), reduce=True, threshold=2)

def test_calculer_poids_cluster():
    result = clusterizer_utils.calculer_poids_cluster(df_test, "apet700")
    assert result == 5  # le premier commence par 68 -> 1 et le deuxième par 49 -> 4

def test_ajouter_point():
    result = NAF_utils.ajouter_point("6820A")
    assert result == "68.20A"

def test_retirer_point():
    result = NAF_utils.retirer_point("68.20A")
    assert result == "6820A"

def test_get_description():
    result = NAF_utils.get_description("011")
    assert result == "Cultures non permanentes"

def test_get_NAFs_by_section():
    result = NAF_utils.get_NAFs_by_section("D")
    print(result)
    assert (result == ["35", "35.1", "35.11", "35.11Z", "35.12", "35.12Z", "35.13", "35.13Z", "35.14", "35.14Z", "35.2", "35.21", "35.21Z", "35.22", "35.22Z", "35.23", "35.23Z", "35.3", "35.30", "35.30Z" ]).all