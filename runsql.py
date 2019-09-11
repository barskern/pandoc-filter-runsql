#!/usr/bin/env python

from os import getenv
import MySQLdb
from panflute import *

host = getenv("MYSQL_HOST", "127.0.0.1")
user = getenv("MYSQL_USER", "root")
passwd = getenv("MYSQL_PASSWORD", "secret")
db = getenv("MYSQL_DATABASE", "trlog")


def action(options, data, element, doc):
    cur = db.cursor()
    cur.execute(element.text)

    cells = [
        TableRow(*[TableCell(Plain(Str(str(v)))) for v in row])
        for row in cur.fetchall()
    ]
    column_names = TableRow(*[TableCell(Plain(Str(i[0]))) for i in cur.description])

    table = Table(*cells, header=column_names)

    element.classes = ["sql"]
    return [
        Header(Str("Query"), level=4),
        element,
        Header(Str("Result"), level=4),
        table,
    ]


if __name__ == "__main__":
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    run_filter(yaml_filter, tag="runsql", function=action)
    db.close()
