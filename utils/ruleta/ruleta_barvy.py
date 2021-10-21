from .model import ruleta_barvy

class ruleta_barva_passer:

    def __init__(self, choice):
        choice = choice.lower()

        if choice == ruleta_barvy.CERNA:
            self.choice = ruleta_barvy.CERNA
        elif choice == ruleta_barvy.CERVENA:
            self.choice = ruleta_barvy.CERVENA
        elif choice == ruleta_barvy.CERVENA2:
            self.choice = ruleta_barvy.CERVENA
        elif choice == ruleta_barvy.CERNA2:
            self.choice = ruleta_barvy.CERNA
        else:
            raise