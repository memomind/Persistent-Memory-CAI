from typing import List, Dict

from py2neo import Graph
import toml

with open('.secrets.toml', 'r') as f:
    secrets = toml.load(f)

graph = Graph(secrets['kg_auth']['url'], auth=(secrets['kg_auth']['username'], secrets['kg_auth']['password']))

def kg_query(cypher:str) -> List[Dict]:
    return graph.run(cypher).data()