import classes
from typing import List
import json

def rowsToNodo(rows: list) -> List[classes.Nodo]:
    retorno = []
    for r in rows["nodes"]:
        r = list(r.values())
        retorno.append(classes.Nodo(r))
    return retorno

def jsonToGateway(rows: list, state: bool) -> List[classes.Gateway]:

    r = list(list(rows.values())[0].values())
  
    l = r[:4]
    d = list(r[4].values())
    for i in d:
        l.append(i)
    l.append(state)
    gateway_info = classes.Gateway(l)
    return gateway_info


def nodesNames(data):
    names = []
    for d in data["nodes"]:
        names.append(d['name'])
    return names
