import psutil as ps

import networkx as nx

import pylab as pl

g = nx.DiGraph()

for pid in ps.pids():
    p = ps.Process(pid)
    print p.cpu_percent()
    g.add_edge(p.parent(), p)


nx.draw_networkx(g)
pl.show()

