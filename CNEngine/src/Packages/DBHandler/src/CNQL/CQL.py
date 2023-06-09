from ..libs import replace

def format(text):
    return text.replace('\n', ' ').split(';')


def get_key_index(db, key):
    for i,item in enumerate(db.keys):
        item = item.split(':')[0]
        if item == key:
            return i

def inferior(c1, c2):
    return c1 < c2

def superior(c1,c2):
    return c1 > c2

def equal(c1, c2):
    return c1 == c2

def classifie_c2(object_c2):
    if '.' in object_c2 and object_c2.replace('.', '').isnumeric():
        return float(object_c2)
    if object_c2.isnumeric():
        return int(object_c2)
    elif object_c2 == 'true':
        return True
    elif object_c2 == 'false':
        return False
    elif '"' in object_c2:
        splitted = object_c2.split('"')
        if splitted[0] == '' and splitted[-1] == '':
            return '"'.join(i for i in splitted[1:-1])
    elif "'" in object_c2:
        splitted = object_c2.split("'")
        if splitted[0] == '' and splitted[-1] == '':
            return "'".join(i for i in splitted[1:-1])

def do_condition(condition, data, db, func, char):
    ret = []
    collumn = get_key_index(db, condition.split(char)[0])
    object_c2 = classifie_c2(condition.split(char)[1])
    for item in data:
        if func(item[collumn].value, object_c2):
            ret.append(item)
    return ret

def do_reverse_condition(condition, data, db, func, char):
    ret = []
    collumn = get_key_index(db, condition.split(char)[0])
    object_c2 = classifie_c2(condition.split(char)[1])
    for item in data:
        if not func(item[collumn].value, object_c2):
            ret.append(item)
    return ret

def calc_operator(condition, data, db, reverse):
    if not reverse:
        func = do_condition
    else:
        func = do_reverse_condition
    if '=' in condition:
        return func(condition, data, db, equal, "=")
    elif '>' in condition:
        return func(condition, data, db, superior, ">")
    elif '<' in condition:
        return func(condition, data, db, inferior, "<")
    return data


def check_condition(db, line, data, reverse=False, index=0):
    if len(line) <= index:
        return data
    if line[index].upper() != 'IF' and line[index].upper() != 'NIF':
        return data
    if len(line) <= index+1:
        return data
    if line[index].upper() == "NIF":
        reverse = not reverse
    return calc_operator(line[index+1], data, db, reverse)

def goodify_data(data):
    if data != []:
        if type(data[0]) == list or type(data[0]) == tuple or type(data[0]) == set:
            for i,item in enumerate(data):
                data[i] = [it.value for it in item]

        else:
            data = [item.value for item in data]

    return data

def good_me(it):

    if it.m_typ == 'bool':
        if it.value == True:
            return "true"
        elif it.value == False:
            return "false"
    else:
        return str(it.value)

def exam_command(com, db, line):
    data = []
    if com == "READ":
        data = get_all(db)
        data = check_condition(db, line, data, False ,2)
        if line[1] != '*':
            index = get_key_index(db, line[1])
            if index is not None:
                data = [i[index] for i in data]

        data = goodify_data(data)

        return data

    if com == "WRITE":
        if len(line) > 1:
            db.write_db(' '.join(i for i in line[1:]).split(','))

    if com == "SAVE":
        db.save_db()

    if com == "DELETE":
        dat = check_condition(db, line, get_all(db, False), True ,1)
        db.clear()
        for item in dat:
            db.write_db([good_me(it) for it in item])

def read_commands(db, text):
    ret = []
    for line in format(text):
        line = tuple(i for i in line.replace('\r', '').split(' ') if i != '')
        if not line:
            continue
        com = line[0].upper()
        command_ret = exam_command(com, db, line)
        if command_ret is not None:
            ret.append(command_ret)

    return ret

def get_collumn(db, name):
    return db.data[name]

def get_all(db, string_replace=True):
    result = []
    for col in db.data.keys():
        for i,item in enumerate(get_collumn(db, col)):
            if i > len(result) - 1:
                result.append([])

            item = replace(item)

            if string_replace:
                if item.m_typ == "string":
                    item.value = '"'.join('"'.join(item for item in item.value.split('"')[1:]).split('"')[:-1])
                if item.m_typ == "char":
                    item.value = '\''.join('\''.join(item for item in item.value.split('\'')[1:]).split('\'')[:-1])


            result[i].append(item)

    return result