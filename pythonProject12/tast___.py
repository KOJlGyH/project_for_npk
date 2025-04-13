data = "update" "test" "results=\"17ll2, Truek, l4, Falsek, l3, Truekk***\"", "key=\"GVpsNqmX\""
data = data.split(', ')
data = list(map(lambda x: x.rstrip('"').lstrip('"'), data))
data1 = []
for el in data:
    string = ''
    for symbol in el:
        if symbol != '\\':
            string += symbol
    data1.append(string)
data = data1.copy()
print(data)
table = data[1]
values = data[2] + '"'
where = data[3] + '"'