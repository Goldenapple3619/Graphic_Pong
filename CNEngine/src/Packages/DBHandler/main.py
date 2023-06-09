#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.ABC import *
from src.libs import *
from src.DB import *
from src.CNQL import *

def main(args: tuple) -> int:
    #if len(args) <= 1:
    #    args = (args[0], "-n")

    #if args[1] == "-d":
    M = MyServer()
    M.launch_loop(web_view)

    #if args[1] == "-t":
    #    D = DataBase("./src/assets/TestDBs/test.cnd")
    #    D.write_db((5,"\"t\"", "true"))
    #    D.save_db("t.cnd")
    #    print(D)

    #if args[1] == "-c":
    #    M = MyServer()
    #    D = DataBase("./src/assets/TestDBs/test.cnd")
    #    M.launch_loop(api_mode,D)
        #read_commands(D,ez_reader("t.cql"))

    #if args[1] == '-n':
    #    D = DataBase("./src/assets/TestDBs/test.cnd")
    #    print(read_commands(D,ez_reader("t.cql")))

    return 0


if __name__ == "__main__":
    main(tuple(argv))