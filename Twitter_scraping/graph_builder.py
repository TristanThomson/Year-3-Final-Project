import os
import networkx as nx
import pandas as pd
from pathlib import Path
from Twitter_scraping.scraper_helper import RandomPicker

G = nx.DiGraph()  # initialises empty NetworkX graph
min_list = RandomPicker().min_df["Twitter"].dropna()  # Pandas series from the "Twitter" col of the SYI dataset
mep_list = RandomPicker().all_df["Twitter"].dropna()
rootdir = os.getcwd()  # path to parent folder of current file


def check_minorities():
    for path in Path(rootdir).rglob('*.csv'):
        curparent = str(path.parent.name)
        if curparent in map(lambda x: x.lower(),min_list["Twitter"].dropna()) and not path.parent.parent.name == "minority":
            print(curparent)
            original = str(rootdir) + "/" + str(path.parent.parent.parent.name) + "/majority/" + str(
                curparent) + "/" + str(path.name)
            new = str(rootdir) + "/" + str(path.parent.parent.parent.name) + "/minority/" + str(curparent) + "/" + str(
                path.name)
            os.rename(original, new)

for path in Path(rootdir).rglob('*.csv'):
    curparent = str(path.parent.name)
    curfile = pd.read_csv(path, encoding='utf-8-sig')
    if curparent.lower() in map(lambda x: x.lower(), min_list):
        G.add_node(curparent, is_mep=1)
        if str(path.name) == "following.csv":
            print(path.name)
            for i in curfile["username"]:
                if i in map(lambda x: x.lower(), mep_list):
                    G.add_node(str(i), is_mep=1)
                else:
                    G.add_node(str(i), is_mep=0)
                G.add_edge(curparent, i)
        else:
            print(path.name)
            for i in curfile["username"]:
                if i in map(lambda x: x.lower(), mep_list):
                    G.add_node(str(i), is_mep=1)
                else:
                    G.add_node(str(i), is_mep=0)
                G.add_edge(str(i), curparent)

nx.write_gexf(G, "minority.gexf")
