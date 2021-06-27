.. Ecosystème logistique documentation master file, created by
   sphinx-quickstart on Sat Jun 26 16:28:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ecosystème logistique - Documentation
======================================

.. toctree::
   :maxdepth: 4
   :caption: Contents:



Interface Homme-Machine
========================
Interface complète
-------------------

.. automodule:: src.ihm.ihm_complet
   :members:


Interaction avec l'utilisateur *via* fichier CSV
-------------------------------------------------
.. automodule:: src.ihm.ihm_csv
   :members:

Utilitaire : fenêtre d'accueil pour :code:`ihm_complet`
--------------------------------------------------------
.. automodule:: src.ihm.ihm_pyqt
   :members:

(Obsolète) Ouverture d'un fichier :code:`HTML` dans un navigateur Web : 
-------------
.. automodule:: src.ihm.web
   :members:

Clusterizer
===================

Fichier principal
------------------
.. automodule:: src.clusterizer.clusterizer
   :show-inheritance:
   :members:
.. .. autosummary::
..    :recursive:
..    :nosignatures:

..    src.clusterizer.clusterizer.*
   

Fichiers utilitaires
----------------------

Utilitaires pour la clusterisation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: src.clusterizer.utils.clusterizer_utils
   :members:

Utilitaires pour la gestion des codes NAF
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: src.clusterizer.utils.NAF_utils
   :members:


.. Utilitaires pour la gestion des codes NAF
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. .. doxygenfile:: NAF_utils.py


.. Utilitaires pour la séparation par la Seine
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. .. automodule:: src.clusterizer.utils.seine_data_utils
..    :members:


Traitement de la base SIRENE
=============================
.. doxygenfile:: traitement_base_sirene.cpp


.. .. automodule:: src.traitement_base_SIRENE.traitement_base_sirene
..    :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



