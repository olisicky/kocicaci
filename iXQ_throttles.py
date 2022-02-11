import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np
import pandas as pd
import os.path, time
import seaborn as sns
sns.set(style="darkgrid")

class plot_results():

    def __init__(self, name, throttle = None):
        """
        :param name: Throttle batch, e.g., FRAM_2150
        :param throttle: The throttle type: CVI, RAMBLER
        """
        self.batch_name = name  # to self mi značí proměnné pro scope toho objektu, takže u metod to nemusím deklarovat pro celou class, ale jen ať to zůstane u té metody
        self.throttle = throttle
        if self.throttle == "RAMBLER":
            self.initial = np.linspace(0, 9, 10)
            self.hyst1 = np.linspace(60, 81, 22)
            self.hyst2 = np.linspace(180, 201, 22)
            self.hyst3 = np.linspace(310, 331, 22)

        elif self.throttle == "CVI":
            self.initial = np.linspace(0, 14, 15)
            self.hyst1 = np.linspace(115, 136, 22)
            self.hyst2 = np.linspace(175, 196, 22)
            self.hyst3 = np.linspace(235, 254, 20)
        else:
            print("Wrong throttle type")
    def AD_flow(self, AD_values):
        """ Přepočet na flow podle měření testovacího, které jsem dělal pro pár bodů."""
        return 0.0038 * AD_values - 3.0312

    def show_image(self, data, limits, names, xlabel, ylabel):
        """ Zobrazení požadované charakteristiky"""
        dpi = 40
        fig, ax = plt.subplots(figsize = (10, 6))
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_axisbelow(True)
        # ax.yaxis.set_major_locator(MultipleLocator(1))
        # ax.yaxis.set_minor_locator(MultipleLocator(0.5))
        ax.yaxis.grid(which = "major", color='gray', linestyle='dashed', alpha = 0.5)
        ax.yaxis.grid(which = "minor", color='gray', linestyle='dashed', alpha = 0.2)
        ax.plot(limits.X, limits.low, linestyle=":", color = "red", label = "- 5 %" )
        ax.plot(limits.X, limits.high, linestyle=":", color = "red", label = "+ 5 %")
        # na základě vstupních souborů to vykreslí ten počet křivek
        for item, name in zip(data, names):
            # musel to převést do numeric kvůli datům z torque-to-rotate!
            ax.plot(pd.to_numeric(item.X), pd.to_numeric(item.Y), label = name)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()

    def get_names(self, path):
        """ Získá jména souborů ve složce. Prozatím pro .csv"""
        names = []
        for file in os.listdir(path):
            if file.endswith(".csv") or file.endswith(".log"):
                names.append(file)
        return names

    def open_file(self, path, name):
        """ Funkce pro otevření a načten dat, které chci analyzovat."""
        df = pd.read_csv(path + "\{}".format(name), sep="\s+|,|\t", header=None, engine="python")
        df = df.rename(columns={df.columns[0]: 'X', df.columns[1]: 'Y'})
        return df[(df.T != 0).any()]   # Výstup pouze hodnoty, kde není 0, tj. ty, kde jsou zaznamenána data

    def limits_(self, path, method):
        """
        :param path: The path to data which will be used to create limits
        :return: The method returns limits
        """
        together = pd.DataFrame()
        export = pd.DataFrame()
        for i in self.get_names(path):
            df = self.open_file(path, i)   # využití metody open
            if method == "opening":
                together["{}".format(i)] = self.AD_flow(df.Y)   # pro opening
            elif method == "capacity":
                together["{}".format(i)] = df.Y    # pro capacity nemusím převádět!
            else:
                raise ValueError("Unknown method")
        # jakmile se stanovují limity pro opening, tak je třeba přepočítat hodnoty a dropnout index, kde je hystereze
        if method == "opening": 
            together["mean"] = together.mean(axis=1)
            index = np.concatenate((self.initial, self.hyst1, self.hyst2, self.hyst3))
            export["mean"] = together["mean"].drop(index)
            export["X"] = df.X.drop(index)
            export["high"] = together["mean"].drop(index) * 1.05
            export["low"] = together["mean"].drop(index) * 0.95
        # u capacity není třeba přepočítat ani dropnout hysterezi !
        elif method == "capacity":
            together["mean"] = together.mean(axis=1)
            export["mean"] = together["mean"]
            export["X"] = df.X
            export["high"] = together["mean"] * 1.05
            export["low"] = together["mean"] * 0.95
        return export

    def capacity(self, path, throttle_name, limits = None):
        """
        :param path: Path to capacity measurements.
        :param limits: Limits for comparison. In None than default limits are used from reference measurements.
        :return: Should return the comparison.
        """
        ylabel = "Air flow [$m^3/h$]"
        xlabel = "$\delta$p [mbar]"
        if limits == "current":
            boundary = self.limits_(path, "capacity")  # zde už self musí být, protože se odkazuji na metodu této funkce, jinak neví o co se jedná!
        else:
            pass    # zde budou doplněny default hodnoty, které budou načteny ze souboru.
        
        if throttle_name == "full":    # keyword pro vykreslení celku. Bude v seznamu případně
            all_throttles = self.get_names(path)
        else:
            all_throttles = []    # očekává se list, tak i když je jeden, tak jej dám do listu
            all_throttles.append(throttle_name + ".csv")    # nevím proč zde musím mít to .csv :(

        # Vytvoření listu, který obsahuje všechna požadovaná data jako DataFrame pro vykreslení
        for_analysis = []
        for item in all_throttles:
            single = self.open_file(path, item)
            for_analysis.append(single)
        # Zavolání show_image na požadovaná data
        self.show_image(for_analysis, boundary, all_throttles,  xlabel, ylabel)
        

    def opening(self, path, throttle_name, limits = None):
        """
        :param path: Path to capacity measurements.
        :param limits: Limits for comparison. In None than default limits are used from reference measurements.
        :return: Should return the comparison.
        """
        ylabel = "Air flow [$m^3/h$]"
        xlabel = "Position [software step = motor step]"
        if limits == "current":
            boundary = self.limits_(path, "opening")  # zde už self musí být, protože se odkazuji na metodu této funkce, jinak neví o co se jedná!
        else:
            pass    # zde budou doplněny default hodnoty, které budou načteny ze souboru.

        if throttle_name == "full":    # keyword pro vykreslení celku. Bude v seznamu případně
            all_throttles = self.get_names(path)
        else:
            all_throttles = []    # očekává se list, tak i když je jeden, tak jej dám do listu
            all_throttles.append(throttle_name + ".csv")    # nevím proč zde musím mít to .csv :(

        # Vytvoření listu, který obsahuje všechna požadovaná data jako DataFrame pro vykreslení

        for_analysis = []
        for item in all_throttles:
            single = self.open_file(path, item)
            single["Y"] = self.AD_flow(single.Y)
            for_analysis.append(single)
        # Zavolání show_image na požadovaná data
        self.show_image(for_analysis, boundary, all_throttles,  xlabel, ylabel)
    def torque(self, path, throttle_name):
        """
        :param path: Path to toruqe-to-rotate measurements.
        :param throttle_name: The name of the throttle which should be analysed.
        """
        xLabel = "Time []"
        yLabel = "Torque [cNm]"
        boundary = pd.DataFrame({"X": [0, 1], "low": [-0.5, -0.5], "high": [0.5, 0.5]})
        if throttle_name == "full":
            all_throttles = self.get_names(path)
        else:
            all_throttles = []
            all_throttles.append(throttle_name + ".log")    # data z torque jsou asi primárně v .log
        
        for_analysis = []
        for item in all_throttles:
            single = self.open_file(path, item)
            single = single.drop([0, 1, 2, 3, 4])
            single["X"] = np.linspace(0, 1, single.Y.shape[0])    # přidání normalizovaného času
            for_analysis.append(single)
        self.show_image(for_analysis, boundary, all_throttles, xLabel, yLabel)
        
        
    def increase(self, path, throttle_name):
        """
        One-step increase pro jednotlivé vzorky.
        :param data: Naměřená data pro vzorek
        :return: percentual increase where hysteresis areas are ommitted.
        """
        ylabel = "Flow increase [%]"
        xlabel = "Position [software step = motor step]"
        index = np.concatenate((self.initial, self.hyst1, self.hyst2, self.hyst3))

        if throttle_name == "full":    # keyword pro vykreslení celku. Bude v seznamu případně
            all_throttles = self.get_names(path)
        else:
            all_throttles = []    # očekává se list, tak i když je jeden, tak jej dám do listu
            all_throttles.append(throttle_name + ".csv")    # nevím proč zde musím mít to .csv :(
        if self.throttle == "RAMBLER":
            boundary = pd.DataFrame({"X": [100, 400], "low": [0.5, 0.5], "high": [1.5, 1.5]})
        elif self.throttle == "CVI":
            boundary = pd.DataFrame({"X": [300, 480], "low": [0.5, 0.5], "high": [1.5, 1.5]})
        
        # Vytvoření listu, který obsahuje všechna požadovaná data jako DataFrame pro vykreslení
        for_analysis = []
        for item in all_throttles:
            single = self.open_file(path, item).drop(index)
            single.columns = ["X", "Y"]
            single["Y"] = self.AD_flow(single.Y).pct_change() * 100
            for_analysis.append(single)

        # Zavolání show_image na požadovaná data
        self.show_image(for_analysis, boundary, all_throttles,  xlabel, ylabel)



x = plot_results("FMK_2205", "CVI")

opening_res = x.opening(r".\Opening_CVI", throttle_name = "full", limits = "current")
increase = x.increase(r".\Opening_CVI", throttle_name = "full")
cap = x.capacity(r".\Capacity", throttle_name = "full", limits = "current")
tor = x.torque(r".\Torque", throttle_name = "FRAM_2204_372")