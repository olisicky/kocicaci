# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 19:15:04 2021

@author: lisicky
"""
""" Tahle část je jenom k tomu, aby se nastavila do cesty environmentu 
    tato adresa k PROJ_LIB. Kdybych nainstaloval Basemap pod virtual
    environment, tak to nejspíše nebylo potřeba!!"""
import os
import conda
conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = r"C:\Users\lisicky\anaconda3\Library\share"

import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import numpy as np
import matplotlib.cm


fig, ax = plt.subplots()
# EVROPA
m = Basemap(resolution='h', projection='merc', lat_0=53.4, lon_0=15.6,
            llcrnrlon=-11.8, llcrnrlat= 35.4, urcrnrlon=43.0, urcrnrlat=71.4)
#Czech republic
# m = Basemap(resolution='h', projection='merc', lat_0=49.805, lon_0=15.495,
#             llcrnrlon=11.75, llcrnrlat= 48.46, urcrnrlon=19.24, urcrnrlat=51.15)
# Abych mohl něco rozumného vykreslit, tak potřebuji informace o hranicích! Takhle mám oblast, která není omezena vodou, takže nemám hranici!
m.fillcontinents(color="#FFFFFF", lake_color='#DDEEFF')
m.drawmapboundary(fill_color="#DDEEFF")
# Vytvoření hranic států evropy z oficiálních stránek
m.readshapefile(r'd:\LISICKY\PhD\Python\Basemap\Areas\EU\europe', 'areas')



# přidání informace do dané oblasti
df_poly = pd.DataFrame({'shapes': [Polygon(np.array(shape), True) for shape in m.areas], 
                        'Country': [area['NUTS_ID'] for area in m.areas_info]})
# =================================== načtení vstupu uživatele ====================================
# =================================== načtení vstupu uživatele ====================================
df_input = pd.read_csv("navstevy_EU.txt", skiprows = None)
counts = pd.DataFrame(df_input["Occurence"].value_counts())
counts["Country"] = counts.index

# ================================= Přidání statistik když ji mám =================================
# vytvoření fiktivního DataFrame, kde mám informace o návštěvách!
# visit = pd.DataFrame({"area": [area['NAZEV_LAU1'] for area in m.areas_info],
#                       "visits": np.random.randint(5, size=df_poly.shape[0])})

# spojení obou DataFrame, abych přiřadil určitý polygon odfkresu k poštu návštěv!
df_poly = df_poly.merge(counts, on='Country', how='left')

cmap = plt.get_cmap('Oranges')   
pc = PatchCollection(df_poly.shapes, zorder=2)
norm = Normalize()

pc.set_facecolor(cmap(norm(df_poly['Occurence'].fillna(0).values)))
ax.add_collection(pc)
# přidání škály do obrazu na základě hodnot
mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
mapper.set_array(df_poly['Occurence'])
plt.colorbar(mapper, shrink=0.4)





