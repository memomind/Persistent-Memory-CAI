from DM.kg_io import *

tmp = kg_query('''MATCH (o:Object {Name: "Tao"})
RETURN o.Interests''')
print(tmp)