#!/usr/bin/env python

import sys
from os import getenv
import MySQLdb
import sqlparse
from panflute import *

host = getenv("MYSQL_HOST", "127.0.0.1")
user = getenv("MYSQL_USER", "root")
passwd = getenv("MYSQL_PASSWORD", "secret")
db = getenv("MYSQL_DATABASE", "trlog")


def action(options, data, element, doc):

    # print(options, file=sys.stderr)

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

    # Remove yaml block so that the output can still be nicly formatted
    yaml_idx = element.text.find("---")
    if yaml_idx >= 0:
        fmt_data = element.text[yaml_idx + 4 :]
    else:
        fmt_data = element.text

    if no_result:
        if err:
            return [CodeBlock(fmt_data, classes=["sql"]), *err]
        else:
            return CodeBlock(fmt_data, classes=["sql"])

    cells = [
        TableRow(*[TableCell(Plain(Str(str(v)))) for v in row])
        for row in cur.fetchall()
    ]
    column_names = TableRow(*[TableCell(Plain(Str(i[0]))) for i in cur.description])

    table = Table(*cells, header=column_names)

    if err:
        return [
            Header(Str("Query"), level=4),
            CodeBlock(fmt_data, classes=["sql"]),
            Header(Str("Result"), level=4),
            *err,
            table,
        ]
    else:
        return [
            Header(Str("Query"), level=4),
            CodeBlock(fmt_data, classes=["sql"]),
            Header(Str("Result"), level=4),
            table,
        ]


if __name__ == "__main__":
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    run_filter(yaml_filter, tag="runsql", function=action)
    db.close()
