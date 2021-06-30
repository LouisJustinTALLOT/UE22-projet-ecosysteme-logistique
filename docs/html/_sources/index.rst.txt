.. Ecosystème logistique documentation master file, created by
   sphinx-quickstart on Sat Jun 26 16:28:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ecosystème logistique - Documentation
======================================
.. toctree::
   :maxdepth: 8
   :caption: Contents:
             generated




Judith Bellon, Gabrielle Vernet, César Almecija, Louis-Justin Tallot
-----------------------------------------------------------------------


Documentation des modules
----------------------------
.. autosummary::
   :toctree: generated
   :template: custom-module-template.rst
   :recursive:
   
   src.clusterizer.clusterizer
   src.clusterizer.utils.clusterizer_utils
   src.clusterizer.utils.NAF_utils
   src.clusterizer.utils.seine_data_utils
   tests.tests_src.test


README
-------
.. include:: ../README.rst

.. Clusterizer
.. -------------------

.. Fichier principal
.. ^^^^^^^^^^^^^^^^^^
.. .. .. automodule:: src.clusterizer.clusterizer
.. ..    :undoc-members:
.. ..    :show-inheritance:
.. ..    :members:

.. .. automodapi:: src.clusterizer.clusterizer


.. ..    src.clusterizer.clusterizer.*
   

.. Fichiers utilitaires
.. ^^^^^^^^^^^^^^^^^^^^^^

.. Utilitaires pour la clusterisation
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. .. automodule:: src.clusterizer.utils.clusterizer_utils
..    :members:
..    :undoc-members:
..    :show-inheritance:

.. Utilitaires pour la gestion des codes NAF
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. .. automodule:: src.clusterizer.utils.NAF_utils
..    :members:
..    :undoc-members:
..    :show-inheritance:


.. .. Utilitaires pour la gestion des codes NAF
.. .. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. .. .. doxygenfile:: NAF_utils.py


.. Utilitaires pour la séparation par la Seine
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. .. automodule:: src.clusterizer.utils.seine_data_utils
..    :members:
..    :undoc-members:
..    :show-inheritance:


.. Traitement de la base SIRENE
.. -----------------------------
.. .. doxygenfile:: traitement_base_sirene.cpp


.. .. .. automodule:: src.traitement_base_SIRENE.traitement_base_sirene
.. ..    :members:


.. Interface Homme-Machine
.. ------------------------
.. Interface complète
.. ^^^^^^^^^^^^^^^^^^^

.. .. automodule:: src.ihm.ihm_complet
..    :undoc-members:
..    :members:
..    :show-inheritance:


.. Interaction avec l'utilisateur *via* fichier CSV
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. .. automodule:: src.ihm.ihm_csv
..    :undoc-members:
..    :show-inheritance:
..    :members:

.. Utilitaire : fenêtre d'accueil pour :code:`ihm_complet`
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. .. automodule:: src.ihm.ihm_pyqt
..    :members:
..    :undoc-members:
..    :show-inheritance:

.. (Obsolète) Ouverture d'un fichier :code:`HTML` dans un navigateur Web : 
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. .. automodule:: src.ihm.web
..    :members:
..    :undoc-members:
..    :show-inheritance:


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



