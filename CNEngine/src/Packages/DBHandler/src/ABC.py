from .types import *
from .CNQL import *

def ez_reader(file):
    with open(file, 'r') as f:
        content = f.read()

    return content

def ez_writer(file, content):
    with open(file, 'w') as f:
        f.write(content)

def code_formater(code):
    if not '#' in code:
        return code

    code = code.split('\n')

    for i, item in enumerate(code):
        if not '#' in item:
            continue

        test_code = item.replace("\\\"", '').replace("\\'", '').split('"')

        if len(test_code) != 1:
            test_code = ''.join(i for i in [item for i, item in enumerate(test_code) if i == 0 or i % 1 == 1]).split('\'')


        if len(test_code) != 1:
            test_code = ''.join(i for i in [item for i, item in enumerate(test_code) if i == 0 or i % 1 == 1])

        if '#' in test_code:
            code[i] = ''

    return '\n'.join(item for item in code if item != '')

def get_balises(raw):
    if not '!' in raw:
        return raw

    bals = {}

    raw = raw.split('![')[1:]
    for item in raw:
        if "]\n" in item:
            name,data = item.split("]\n")
        else:
            name,data = item.split("]")

        data = data.replace('\n', '').split(',')

        for i, items in enumerate(data):
            inner = False, None

            word = []

            for letter in items:

                if letter == '"' and (not inner[0] or inner[1] == '"'):
                    inner = not inner[0], '"'
                elif letter == '\'' and (not inner[0] or inner[1] == '\''):
                    inner = not inner[0], '\''

                if not inner[0]:
                    if letter != ' ':
                        word.append(letter)

                else:
                    word.append(letter)

            data[i] = ''.join(i for i in word)
        bals[name] = data

    return bals

def read_db():
    pass


def api_mode(address, string_list, connection, db):

    method = string_list[0]

    if len(string_list) < 2:
        print(f'No file request, address: {address[0]}:{address[1]}, mehod: {method}')
        return

    requesting_file = string_list[1]

    print(f'Client request {requesting_file}, address: {address[0]}:{address[1]}, mehod: {method}')

    path = "./src/assets"
    myfile = requesting_file.split('?')[0]
    myfile = myfile.lstrip('/')

    if(myfile == ''):
        myfile = f'index.html'

    try:
        print(path + '/' + myfile)
        file = open(path + '/' + myfile,'r')
        response = str(read_commands(db, file.read())).encode("UTF-8", errors='ignore')

        header = 'HTTP/1.1 200 OK\n'

        mimetype = 'application/json'

        header += 'Content-Type: '+str(mimetype)+'\n\n'
        file.close()

    except Exception as e:
        print(e)
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')

    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()

def web_view(address, string_list, connection):

    method = string_list[0]

    if len(string_list) < 2:
        print(f'No file request, address: {address[0]}:{address[1]}, mehod: {method}')
        return

    requesting_file = string_list[1]

    print(f'Client request {requesting_file}, address: {address[0]}:{address[1]}, mehod: {method}')

    path = "./src/assets"
    myfile = requesting_file.split('?')[0]
    myfile = myfile.lstrip('/')

    if(myfile == ''):
        myfile = f'index.html'

    try:
        print(path + '/' + myfile)
        file = open(path + '/' + myfile,'rb')
        response = file.read()

        header = 'HTTP/1.1 200 OK\n'

        if(myfile.endswith(".jpg")):
            mimetype = 'image/jpg'
        elif(myfile.endswith(".css")):
            mimetype = 'text/css'
        elif(myfile.endswith(".js")):
            mimetype = "text/javascript"
        elif(myfile.endswith(".ttf")):
            mimetype = "font/ttf"
        elif(myfile.endswith(".cql")):
            mimetype = 'text/plain'
        else:
            mimetype = 'text/html'

        header += 'Content-Type: '+str(mimetype)+'\n\n'
        file.close()

    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')

    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()