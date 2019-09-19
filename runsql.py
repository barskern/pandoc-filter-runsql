#!/usr/bin/env python

import sys
from os import getenv
import MySQLdb
import sqlparse
from panflute import *
import sqlparse

host = getenv("MYSQL_HOST", "127.0.0.1")
user = getenv("MYSQL_USER", "root")
passwd = getenv("MYSQL_PASSWORD", "secret")
db = getenv("MYSQL_DATABASE", "trlog")


def action(options, data, element, doc):
    if isinstance(options, dict):
        no_result = options.get("no_result", False)
    else:
        # If options is not a dict, it is the actual data
        no_result = False
        data = str(options)

    err = None

    cur = db.cursor()
    try:
        cur.execute(data)
    except MySQLdb.IntegrityError as e:
        err = convert_text(f"Error: {e}")

    fmt_data = sqlparse.format(data, reindent=True, keyword_case="upper")

    if no_result:
        if err:
            return [CodeBlock(fmt_data, classes=["sql"]), *err]
        else:
            return [
                CodeBlock(fmt_data, classes=["sql"]),
                *convert_text(f"Query successfully: {cur.rowcount} row{'s' if cur.rowcount > 1 else ''} affected"),
            ]

    cells = [
        TableRow(*[TableCell(Plain(Str(str(v)))) for v in row])
        for row in cur.fetchall()
    ]
    column_names = TableRow(*[TableCell(Plain(Str(i[0]))) for i in cur.description])

    table = Table(*cells, header=column_names)

    if err:
        return [CodeBlock(fmt_data, classes=["sql"]), *err, table]
    else:
        return [CodeBlock(fmt_data, classes=["sql"]), table]


if __name__ == "__main__":
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    run_filter(yaml_filter, tag="runsql", function=action)
    db.close()
