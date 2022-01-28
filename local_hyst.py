# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 10:59:56 2021

@author: 208713
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np
import pandas as pd
import os.path, time
from matplotlib.widgets import CheckButtons
import datetime
import colorsys

path = r"V:\01_Combustion_Private\01_Projects\iXQ2_CVI_Throttle_ACV\04_TEST\iXQ CVI\TESTY\Lifetest\004-Opening_Behavior"

def open(name):
    """ Funkce pro otevření a načten dat, které chci analyzovat."""
    df = pd.read_csv(path + "\{}.csv".format(name), sep=",|;", header =None, engine="python")
    df.columns = ["position", "AD"]
    return df.iloc[14:44,:]  # omezení pro oblast, která se dá číst.. pak mám velké flow!!!
def AD_flow(AD_values):
    """ Přepočet na flow podle měření testovacího, které jsem dělal pro pár bodů."""
    return 0.0038 * AD_values -3.0312

# ================================ Aplikace funkcí ================================
throttle_name = r"\LT03_hyst"   # zde zadej žádaný throttle

hyst1 = open(r"1_4" + throttle_name)    # první test cca 20 %
hyst2 = open(r"2_4" + throttle_name)
hyst3 = open(r"3_4" + throttle_name)
hyst4 = open(r"4_4" + throttle_name)

fig, ax = plt.subplots()
ax.set_xlabel("Position [software step = motor step]")
ax.set_ylabel("Air flow [$m^3/h$]")
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# nastavení grid pro graf
ax.set_axisbelow(True)
ax.plot(hyst1["position"], AD_flow(hyst1["AD"]), "-o", label = "First measurement")
ax.plot(hyst2["position"], AD_flow(hyst2["AD"]), "-o", label = "Second measurement")
plt.legend()
    