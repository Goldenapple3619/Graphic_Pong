from .ABC import *

class DataBase:
    def __init__(self, db_path):
        self.load_db(db_path)
        self.db_path = db_path
        self.data = self.raw_to_column()

    def __repr__(self):
        max_sized = 5

        k_l = len(self.keys)-1

        return ''.join (
            self.keys[i].split(':')[0] + ': ' + item + '\n'
            if i == k_l

            else
            self.keys[i].split(':')[0] + ': ' + item + ' '*max_sized

            for items in self.values
            for i, item in enumerate(items)
        )

    def clear(self):
        self.data=[]
        self.values=[]

    def load_db(self, path):
        raw_data = code_formater(ez_reader(path))

        if raw_data == '':
            self.keys, self.values = [], []
            return

        bals = get_balises(raw_data)

        if bals["values"] == ['']:
            self.values = []

        if bals["keys"] == ['']:
            self.keys = []

        try:
            bals["values"]
            bals["keys"]
        except NameError:
            self.keys, self.values = [], []
            return

        if bals["values"] != ['']:
            bals["values"] = [item.split('|') for item in bals["values"]]

        self.keys, self.values = bals["keys"], bals["values"]

    def save_db(self, path=None):
        if path is None:
            path= self.db_path
        k_l = len(self.keys) - 1

        to_write = "![keys]\n" + ',\n'.join (
            f"    {i}" for i in self.keys
        ) + '\n' + "![values]\n" + ''.join (
            f"{item},\n"
            if i == k_l

            else
            f"{item}|"
            if i != 0

            else
            f"    {item}|"

            for row in self.values
            for i, item in enumerate(row)
        )[:-2]

        ez_writer(path, to_write)

    def raw_to_column(self):
        keys = tuple((item.split(':')[0], types[item.split(':')[1]], item.split(':')[1]) for item in self.keys)

        columns = {key[0]:[] for key in keys}

        for row in self.values:
            for i,item in enumerate(row):
                key,classifie,type_t = keys[i]

                if type_t == "string":
                    size = len(item)

                if type_t == "int":
                    item = int(item)
                    size = round(item // 256)

                if type_t == "float":
                    item = float(item)
                    size = round(item // 256)

                if type_t == "bool":
                    if (item == "true" or item == "1"):
                        item = True

                    elif (item == "false" or item == "0"):
                        item = False

                columns[key].append(classifie(item, size))

        return columns

    def write_db(self, values):
        values = list(values)
        while len(values) != len(self.keys):
            values.append(None)

        self.values.append([str(value) for value in values])

        self.data = self.raw_to_column()

    def write_key(self, keys_types):
        self.keys.append(f'{keys_types[0]}:{keys_types[1]}')
        self.data = self.raw_to_column()

    def normalize_data(self, item):
        if item.m_typ == "string":
            return str('"'.join('"'.join(item.value.replace('\\n', '\n').split('"')[1:]).split('"')[:-1]))
        if item.m_typ == "char":
            return str('\''.join('\''.join(item.value.replace('\\n', '\n').split('\'')[1:]).split('\'')[:-1]))
        if item.m_typ == "int":
            return int(item.value)
        if item.m_typ == "float":
            return float(item.value)
        if item.m_typ == "bool":
            return bool(item.value)

    def data_to_list(self, normalize=True):
        data = self.data
        keys = data.keys()

        incr = 0

        end_list = []
        while incr < len(self.values):

            end_list.append({})

            for key in keys:

                if normalize:
                    end_list[incr][key] = self.normalize_data(data[key][incr])
                else:
                    end_list[incr][key] = data[key][incr]

            incr += 1

        return end_list
