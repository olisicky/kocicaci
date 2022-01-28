import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np
import pandas as pd
import os.path, time
from matplotlib.widgets import CheckButtons
import datetime
import colorsys

path = r"V:\01_Combustion_Private\01_Projects\IXQ 2_Rambler_Throttle_AOS\TEST\Testy\039-mikrotech TR_january\004 - opening"

def open(name):
    """ Funkce pro otevření a načten dat, které chci analyzovat."""
    df = pd.read_csv(path + "\{}.csv".format(name), sep=",|;", header =None, engine="python")
    df.columns = ["position", "AD"]
    return df.iloc[:380,:]  # omezení pro oblast, která se dá číst.. pak mám velké flow!!!
def AD_flow(AD_values):
    """ Přepočet na flow podle měření testovacího, které jsem dělal pro pár bodů."""
    return 0.0038 * AD_values -3.0312
def hysteresis(data):
    """ Určení hystereze ve třech základních bodech. Jedná se o kontrolu, zda se jedná o stejnou
        nebo větší hodnotu než ta startovací v bodě zlomu. Nutno ověřit i manuálně, zda ty hodnoty sedí."""
    ref1 = data.iloc[60,1]
    ref2 = data.iloc[180,1]
    ref3 = data.iloc[310,1]
    hyst1 = data.iloc[61:70,:]
    hyst2 = data.iloc[181:190,:]
    hyst3 = data.iloc[311:320,:]
    # nepodařilo se mi to zadat najednou, takže jsem to musel rozdělit do dvou částí
    hyst1 = hyst1.loc[hyst1.AD >= ref1]
    hyst2 = hyst2.loc[hyst2.AD >= ref2]
    hyst3 = hyst3.loc[hyst3.AD >= ref3]
    return len(hyst1), len(hyst2), len(hyst3)

def mean_response():
    """ Určení mean křivky ze všech průběžných dat. Vynechány místa hystereze.. Jsou zde možné lokální skoky..."""
    names = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            names.append(file)
    together = pd.DataFrame()
    export = pd.DataFrame()
    for i in names:
        df = pd.read_csv(path + "\{}".format(i),
                         sep=",|;", header=None, engine="python", skiprows=0)
        df.columns = ["position", "AD"]
        together["{}".format(i)] = AD_flow(df.AD)
        together["mean"] = together.mean(axis = 1)
        initial = np.linspace(0, 9, 10)
        hyst1 = np.linspace(60, 81, 22)
        hyst2 = np.linspace(180, 201, 22)
        hyst3 = np.linspace(310, 331, 22)
        index = np.concatenate((initial, hyst1, hyst2, hyst3))
    export["mean"] = together["mean"].drop(index)
    export["position"] = df.position.drop(index)
    export["high"] = together["mean"].drop(index)*1.05
    export["low"] = together["mean"].drop(index) * 0.95
    return export.iloc[0:300,:] # tohle záleží na počtu hodnot, které chci vykreslit.. omezeno tím, které indexy posílám do háje!
limits = mean_response()

def opening(data, limits, hysteresis1, hysteresis2, hysteresis3):
    """ Opening curve pro analyzovaný throttle. Zde jsou důležité nějaké výpadky v měření nebo charakteristice,
        které by mohly být odhaleny pak i v 1 step increase."""
    fig, ax = plt.subplots()
    ax.set_xlabel("Position [software step = motor step]")
    ax.set_ylabel("Air flow [$m^3/h$]")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # nastavení grid pro graf
    ax.set_axisbelow(True)
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(0.25))
    ax.yaxis.grid(which = "major", color='gray', linestyle='dashed', alpha = 0.5)
    ax.yaxis.grid(which = "minor", color='gray', linestyle='dashed', alpha = 0.2)

    ax.text(200, 1.2, "Piet range", fontsize=14, color = "red")
    ax.text(300, 1.2, "Erwin range", fontsize=14, color = "blue")
    ax.text(50,2, "HYsteresis: {}".format(hysteresis1))
    ax.text(200, 5.5, "HYsteresis: {}".format(hysteresis2))
    ax.text(250, 8, "HYsteresis: {}".format(hysteresis3))
    ax.axvspan(150, 360, alpha=0.1, color='red')   # ukázání oblasti, kde je pracovní oblast
    ax.axvspan(240, 430, alpha=0.2, color="blue")   # oblast AOS - Erwin
    ax.plot(data.position, AD_flow(data.AD))
    ax.plot(limits.position, limits.low, linestyle=":", color = "red", label = "- 5 %" )
    ax.plot(limits.position, limits.high, linestyle=":", color = "red", label = "+ 5 %")
    plt.legend()
    plt.show()

def increase(data):
    """ Funkce pro vykreslení nárůstu flow. Zde oddělávám body z hystereze, ale ten poslední tam
        zůstává, takže tam jde vidět skok v místě hystereze.. Tohle ignorovat!"""
    fig, ax = plt.subplots()
    ax.set_xlabel("Position [software step = motor step]")
    ax.set_ylabel("1 step increase [%]")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlim(100,420)
    ax.text(200, 2.1, "Piet range", fontsize=14, color = "red")
    ax.text(300, 2.1, "Erwin range", fontsize=14, color = "blue")
    ax.axvspan(150, 360, alpha=0.1, color='red')  # ukázání oblasti, kde je pracovní oblast
    ax.axvspan(240, 430, alpha=0.2, color="blue")   # oblast AOS - Erwin
    ax.hlines(xmin = 100, xmax = 410, y = 1.5, linestyle= ":", color = "red", label = "1.5 % increase limit")
    ax.hlines(xmin = 100, xmax = 410, y = 1, linestyle= ":", color = "green", label = "1 % increase limit")
    ax.hlines(xmin=100, xmax=410, y=0, color="red", linewidth = 2, label="0 % increase limit")
    initial = np.linspace(0,9, 10)
    hyst1 = np.linspace(60,81, 22)
    hyst2 = np.linspace(180,201, 22)
    hyst3 = np.linspace(310,331,22)
    index = np.concatenate((initial, hyst1, hyst2, hyst3))
    increase = AD_flow(data.AD).drop(index).pct_change()*100
    position = data.position.drop(index)
    ax.plot(position, increase, ".-", color = "gray", linewidth = 0.5, label = "sample")
    # vykreslení mean +- std pro increase ... kvůli tomu, že to osciluje
    ax.hlines(xmin = 100, xmax = 480, y = increase.mean(), color = "tab:orange", label = "Mean increase")
    ax.axhspan(increase.mean() - increase.std(), increase.mean() + increase.std(), alpha=0.3, color='gray', label = "STD")
    plt.legend()
    plt.show()

def comparison(limits):
    """ Konečné porovnání všech hodnot, které máme naměřeny. Zde bych vynesl i +- 10 %. To
     bude určeno z několika křivek jako mean! Je zde i možnost vykreslení dat do skupin podle dnů měření."""
    names = []
    dates = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            names.append(file)
            fullPath = os.path.join(path, file)
            try:
                # určení doby vzniku souboru a převedení na datetime
                creation_date = datetime.datetime.strptime(time.ctime(os.path.getctime(fullPath)), "%a %b %d %H:%M:%S %Y")
                creation_date = creation_date.strftime("%m-%d")
                dates.append(creation_date)
            except:
                pass
    measure_groups = pd.DataFrame(names, columns=['throttle'], index = dates)
    measure_groups = measure_groups.sort_index()    # sort podle data vytvoření!
    unique = measure_groups.index.unique()  # nalezení unikátních indexů pro vytvoření skupin
    # vygenerování barev podle počtu skupin (dnů, kdy se měřilo)
    N = len(unique)
    HSV_tuples = [(x * 1.0 / N, 1, 1) for x in range(N)]    # musí se první asi generovAT hue space
    RGB_tuples = list(map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples))   # to se pak namapuje na RGB
    colors_dict = dict(zip(unique, RGB_tuples)) # vytvoření dictionary pro barvičky
    print(colors_dict)
    fig, ax = plt.subplots()
    ax.set_xlabel("Position [software step = motor step]")
    ax.set_ylabel("Air flow [$m^3/h$]")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # nastavení grid pro graf
    ax.set_axisbelow(True)
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(0.25))
    ax.yaxis.grid(which = "major", color='gray', linestyle='dashed', alpha = 0.5)
    ax.yaxis.grid(which = "minor", color='gray', linestyle='dashed', alpha = 0.2)

    #ax.text(200, 1.2, "Piet range", fontsize=14, color = "red")
    #ax.text(300, 1.2, "Erwin range", fontsize=14, color = "blue")
    #ax.axvspan(150, 360, alpha=0.1, color='red')  # ukázání oblasti, kde je pracovní oblast
    #ax.axvspan(240, 430, alpha = 0.2, color = "blue")   # oblast AOS / Erwin
    # vykreslení limit +- 5 % od průměru
    ax.plot(limits.position, limits.low, linestyle=":", color = "red", label = "- 5 %" )
    ax.plot(limits.position, limits.high, linestyle=":", color = "red", label = "+ 5 %")
    # uměle vytvořená legenda pro barvy
    markers = [plt.Line2D([0, 0], [0, 0], color=color, marker='o', linestyle='') for color in colors_dict.values()]
    plt.legend(markers, colors_dict.keys(), numpoints=1)
    lines = []
    for i in names:
        df = pd.read_csv(path + "\{}".format(i),
                         sep=",|;", header=None, engine="python")
        df.columns = ["position", "AD"]
        df = df.iloc[:380, :]  # záleží na počtu dat!
        index = measure_groups.index[
            measure_groups['throttle'] == i]  # hledám index z předpřipraveného df, podle kterého budu přiřazovat barvu
        #i, = ax.plot(df.position, AD_flow(df.AD), label="{}".format(i), c=index.map(colors_dict)[0])  # přiřazení proměnné kvůli check bottom v další fázi
        i, = ax.plot(df.position, AD_flow(df.AD), label="{}".format(i))  # přiřazení proměnné kvůli check bottom v další fázi
        lines.append(i)
    plt.legend()
    # ========================================= CHECK BUTTONS =========================================================
    #plt.subplots_adjust(left=0.3)   # posunutí kvůli těm check button
    # vytvoření možnosti CHECK BUTTON, abych mohl v grafu potom zaklikávat, o chci zobrazit
    #rax = plt.axes([0.0, 0.0, 0.25, 1],frameon = True)
    #labels = [str(line.get_label())[:12] for line in lines] # zde je slicing u názvu, aby tam nebyl celý název! Jinak to jen vezme názvy křivek, které vykresluji
    #visibility = [line.get_visible() for line in lines]
    #check = CheckButtons(rax, labels, visibility)   # funkce přímo od matplotlib widgets
    #for r in check.labels:
    #    r.set_fontsize(8)
    #def func(label):
    #    index = labels.index(label)
    #    lines[index].set_visible(not lines[index].get_visible())
    #    plt.draw()
    #check.on_clicked(func)  # inicializace funkce od matplotlib
    plt.show()

# ================================ Aplikace funkcí ================================
throttle_name = "FRAM_2204_374"   # zde zadej žádaný throttle
hyst1, hyst2, hyst3 = hysteresis(open(throttle_name))  # zde zadej žádaný throttle
opening(open(throttle_name), limits, hyst1, hyst2, hyst3)
increase(open(throttle_name))

comparison(limits)

