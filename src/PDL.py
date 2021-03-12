class PDL:
    """
    Classe représentant un Point De Livraison (PDL)
    """

    def __init__(self, typo, nom, uid, poids, loc):
        """
        typo : typologie (respectant la convention NAF)
        nom : nom
        uid : SIRET
        poids : poids relatif de ce point à livrer.
            - si c'est un commerce, c'est le nb d'employés (ou la surface ?)
            - si c'est une habitation, on verra (mettre 1 pour l'instant)
        loc : tuple de coordonnées (lat, long) (adresse non-nécessaire)
        """
        self.typo = typo
        self.nom = nom
        self.uid = uid
        self.poids = poids
        self.loc = loc