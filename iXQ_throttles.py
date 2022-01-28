import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os.path, time


class plot_results():

    def __init__(self, name, throttle = None):
        """
        :param name: Throttle batch, e.g., FRAM_2150
        :param throttle: The throttle type: CVI, RAMBLER
        """
        self.batch_name = name  # to self mi značí proměnné pro scope toho objektu, takže u metod to nemusím deklarovat pro celou class, ale jen ať to zůstane u té metody
        self.throttle = throttle

    def AD_flow(self, AD_values):
        """ Přepočet na flow podle měření testovacího, které jsem dělal pro pár bodů."""
        return 0.0038 * AD_values - 3.0312

    def get_names(self, path):
        """ Získá jména souborů ve složce. Prozatím pro .csv"""
        names = []
        for file in os.listdir(path):
            if file.endswith(".csv"):
                names.append(file)
        return names


    def opening_limits(self, path):
        """
        :param path: The path to data which will be used to create limits
        :return: The method returns limits
        """
        together = pd.DataFrame()
        export = pd.DataFrame()
        for i in self.get_names(path):
            df = pd.read_csv(path + "\{}".format(i),
                             sep=",|;", header=None, engine="python", skiprows=0)
            df.columns = ["position", "AD"]
            together["{}".format(i)] = self.AD_flow(df.AD)
            together["mean"] = together.mean(axis=1)
            if self.throttle == "RAMBLER":
                initial = np.linspace(0, 9, 10)
                hyst1 = np.linspace(60, 81, 22)
                hyst2 = np.linspace(180, 201, 22)
                hyst3 = np.linspace(310, 331, 22)

            elif self.throttle == "CVI":
                initial = np.linspace(0, 14, 15)
                hyst1 = np.linspace(115, 136, 22)
                hyst2 = np.linspace(175, 196, 22)
                hyst3 = np.linspace(235, 254, 20)
            else:
                print("Wrong throttle type")
            index = np.concatenate((initial, hyst1, hyst2, hyst3))
        export["mean"] = together["mean"].drop(index)
        export["position"] = df.position.drop(index)
        export["high"] = together["mean"].drop(index) * 1.05
        export["low"] = together["mean"].drop(index) * 0.95
        return export.iloc[0:300,:]

    def capacity(self, path, limits = None):
        """
        :param path: Path to capacity measurements.
        :param limits: Limits for comparison. In None than default limits are used from reference measurements.
        :return: Should return the comparison.
        """
        if limits == "current":
            boundary = self.capacity_limits(path)  # zde už self musí být, protože se odkazuji na metodu této funkce, jinak neví o co se jedná!
        else:
            pass    # zde budou doplněny default hodnoty, které budou načteny ze souboru.
        return boundary

    def opening(self, path, limits = None):
        """
        :param path: Path to capacity measurements.
        :param limits: Limits for comparison. In None than default limits are used from reference measurements.
        :return: Should return the comparison.
        """
        if limits == "current":
            boundary = self.opening_limits(path)  # zde už self musí být, protože se odkazuji na metodu této funkce, jinak neví o co se jedná!
        else:
            pass    # zde budou doplněny default hodnoty, které budou načteny ze souboru.
        return boundary




x = plot_results("FRAM_2150", "RAMBLER")
# bla = x.capacity(r"V:\01_Combustion_Private\01_Projects\IXQ 2_Rambler_Throttle_AOS\TEST\Testy\038-unique blade holder_proto\004 - opening", limits = "current")
blaa = x.opening(r"V:\01_Combustion_Private\01_Projects\IXQ 2_Rambler_Throttle_AOS\TEST\Testy\038-unique blade holder_proto\004 - opening", limits = "current")

print(blaa)
