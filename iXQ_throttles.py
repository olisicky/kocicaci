import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
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

    def show_image(self, data, limits, names, xlabel, ylabel):
        """ Zobrazení požadované charakteristiky"""
        dpi = 40
        fig, ax = plt.subplots()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_axisbelow(True)
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_minor_locator(MultipleLocator(0.25))
        ax.yaxis.grid(which = "major", color='gray', linestyle='dashed', alpha = 0.5)
        ax.yaxis.grid(which = "minor", color='gray', linestyle='dashed', alpha = 0.2)
        ax.plot(limits.X, limits.low, linestyle=":", color = "red", label = "- 5 %" )
        ax.plot(limits.X, limits.high, linestyle=":", color = "red", label = "+ 5 %")
        # na základě vstupních souborů to vykreslí ten počet křivek
        for item, name in zip(data, names):
            ax.plot(item.X, item.Y, label = name)
        plt.legend()
        plt.show()

    def get_names(self, path):
        """ Získá jména souborů ve složce. Prozatím pro .csv"""
        names = []
        for file in os.listdir(path):
            if file.endswith(".csv"):
                names.append(file)
        return names

    def open(self, path, name):
        """ Funkce pro otevření a načten dat, které chci analyzovat."""
        df = pd.read_csv(path + "\{}".format(name), sep=",|;", header=None, engine="python")
        df.columns = ["X", "Y"]
        return df[(df.T != 0).any()]   # Výstup pouze hodnoty, kde není 0, tj. ty, kde jsou zaznamenána data

    def opening_limits(self, path):
        """
        :param path: The path to data which will be used to create limits
        :return: The method returns limits
        """
        together = pd.DataFrame()
        export = pd.DataFrame()
        for i in self.get_names(path):
            df = self.open(path, i)   # využití metody open
            together["{}".format(i)] = self.AD_flow(df.Y)
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
        export["X"] = df.X.drop(index)
        export["high"] = together["mean"].drop(index) * 1.05
        export["low"] = together["mean"].drop(index) * 0.95
        return export


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

    def opening(self, path, throttle_name, limits = None):
        """
        :param path: Path to capacity measurements.
        :param limits: Limits for comparison. In None than default limits are used from reference measurements.
        :return: Should return the comparison.
        """
        ylabel = "Air flow [$m^3/h$]"
        xlabel = "Position [software step = motor step]"
        if limits == "current":
            boundary = self.opening_limits(path)  # zde už self musí být, protože se odkazuji na metodu této funkce, jinak neví o co se jedná!
        else:
            pass    # zde budou doplněny default hodnoty, které budou načteny ze souboru.

        if throttle_name == "full":    # keyword pro vykreslení celku. Bude v seznamu případně
            all = self.get_names(path)
        else:
            all = []    # očekává se list, tak i když je jeden, tak jej dám do listu
            all.append(throttle_name + ".csv")    # nevím proč zde musím mít to .csv :(

        # Vytvoření listu, který obsahuje všechna požadovaná data jako DataFrame pro vykreslení

        for_analysis = []
        for item in all:
            single = self.open(path, item)
            single["Y"] = self.AD_flow(single.Y)
            for_analysis.append(single)
        for_analysis.append(all)
        # Zavolání show_image na požadovaná data
        self.show_image(for_analysis, boundary, all,  xlabel, ylabel)

    def increase(self, path, throttle_name):
        """
        One-step increase pro jednotlivé vzorky.
        :param data: Naměřená data pro vzorek
        :return: percentual increase where hysteresis areas are ommitted.
        """
        ylabel = "Flow increase [%]"
        xlabel = "Position [software step = motor step]"

        if self.throttle == "RAMBLER":
            initial = np.linspace(0, 9, 10)
            hyst1 = np.linspace(60, 81, 22)
            hyst2 = np.linspace(180, 201, 22)
            hyst3 = np.linspace(310, 331, 22)
            boundary = pd.DataFrame({"X": [100, 400], "low": [0.5, 0.5], "high": [1.5, 1.5]})
        elif self.throttle == "CVI":
            initial = np.linspace(0, 14, 15)
            hyst1 = np.linspace(115, 136, 22)
            hyst2 = np.linspace(175, 196, 22)
            hyst3 = np.linspace(235, 254, 20)
            boundary = pd.DataFrame({"X": [300, 480], "low": [0.5, 0.5], "high": [1.5, 1.5]})
        else:
            raise ValueError
        index = np.concatenate((initial, hyst1, hyst2, hyst3))

        if throttle_name == "full":    # keyword pro vykreslení celku. Bude v seznamu případně
            all = self.get_names(path)
        else:
            all = []    # očekává se list, tak i když je jeden, tak jej dám do listu
            all.append(throttle_name + ".csv")    # nevím proč zde musím mít to .csv :(

        # Vytvoření listu, který obsahuje všechna požadovaná data jako DataFrame pro vykreslení

        for_analysis = []
        for item in all:
            single = self.open(path, item).drop(index)
            single.columns = ["X", "Y"]
            single["Y"] = self.AD_flow(single.Y).pct_change() * 100
            for_analysis.append(single)

        # Zavolání show_image na požadovaná data
        self.show_image(for_analysis, boundary, all,  xlabel, ylabel)



x = plot_results("FRAM_2150", "CVI")

opening_res = x.opening(r".\Opening_CVI", throttle_name = "full", limits = "current")
increase = x.increase(r".\Opening_CVI", throttle_name = "full")
