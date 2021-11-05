import sqlite3 as sql
import time as t

import sympy as sym

from PageHandler import PageHandler as pH
from calcPageRank import pagerank

sym.init_printing()

dfac = 0.85
tmp = (1 - dfac)

a, b, c = sym.symbols('a,b,c')

f = sym.Eq(tmp + dfac * a, b)
g = sym.Eq(tmp + dfac * b, a)

print(sym.solve([f, g], (a, b)))

f = sym.Eq(tmp + dfac * b, a)
g = sym.Eq(tmp + dfac * c, b)
h = sym.Eq(tmp + dfac * a, c)

print(sym.solve([f, g, h], (a, b, c)))

f = sym.Eq(tmp + dfac * (b / 2), a)
g = sym.Eq(tmp + dfac * (a / 2), b)
h = sym.Eq(tmp + dfac * (a / 2 + b / 2), c)

print(sym.solve([f, g, h], (a, b, c)))

f = sym.Eq(tmp, a)
g = sym.Eq(tmp + 0.85 * a, b)
h = sym.Eq(tmp + 0.85 * b, c)

print(sym.solve([f, g, h], (a, b, c)))

lowlimit = 0.9999999
highlimit = 1.0000001


def pagerank3(a1, b1, c1):
    ldfac = 0.85
    a2 = (1 - ldfac) + ldfac * (b1 / 2)
    b2 = (1 - ldfac) + ldfac * (a1 / 2)
    c2 = (1 - ldfac) + ldfac * (a1 / 2 + b1 / 2)

    if lowlimit < (a1 / a2) < highlimit and lowlimit < (b1 / b2) < highlimit and lowlimit < (c1 / c2) < highlimit:
        return a1, b1, c1
    else:
        return pagerank3(a2, b2, c2)


def pagerank4(a1, b1, c1):
    ldfac = 0.85
    a2 = (1 - ldfac)
    b2 = (1 - ldfac) + ldfac * a1
    c2 = (1 - ldfac) + ldfac * b1

    if lowlimit < (a1 / a2) < highlimit and lowlimit < (b1 / b2) < highlimit and lowlimit < (c1 / c2) < highlimit:
        return a1, b1, c1
    else:
        return pagerank4(a2, b2, c2)


print(pagerank3(1, 1, 1))
print(pagerank4(1, 1, 1))


class Page:
    def __init__(self, name: str, outgoingLinks, refPages: list[str]):
        self.name = name
        self.outgoingLinks = outgoingLinks
        self.refPages = refPages
        self.pageRank = 1
        self.symbol = sym.symbols(name.replace("-", "_"))
        self.eq = sym.Eq(1, self.symbol)


def calcEq(pages: dict[str, Page]):
    ldfac = 0.85
    for z in pages:
        exp = "(1 -" + str(ldfac) + ")"
        if len(pages[z].refPages) > 0:
            exp += "+" + str(ldfac) + "*" + "("
            for lcnt, y in enumerate(pages[z].refPages):
                if lcnt > 0:
                    exp += "+"
                if pages[y].outgoingLinks == 0:
                    exp += "0"
                else:
                    exp += str(pages[y].symbol) + "/" + str(pages[y].outgoingLinks)
            exp += ")"
        pages[z].eq = sym.Eq(sym.parse_expr(exp), pages[z].symbol)


print("P1")
a = Page("a", 1, ["b"])
b = Page("b", 1, ["a"])

pagelist = {"a": a, "b": b}
calcEq(pagelist)
print(sym.solve([pagelist[z].eq for z in pagelist], [pagelist[z].symbol for z in pagelist]))

print("P2")
a = Page("a", 1, ["c"])
b = Page("b", 1, ["a"])
c = Page("c", 1, ["a"])

pagelist = {"a": a, "b": b, "c": c}

calcEq(pagelist)
print(sym.solve([pagelist[z].eq for z in pagelist], [pagelist[z].symbol for z in pagelist]))

print("P3")
a = Page("a", 2, ["b"])
b = Page("b", 2, ["a"])
c = Page("c", 0, ["a", "b"])

pagelist = {"a": a, "b": b, "c": c}

calcEq(pagelist)
print(sym.solve([pagelist[z].eq for z in pagelist], [pagelist[z].symbol for z in pagelist]))

print("P4")

a = Page("a", 1, [])
b = Page("b", 1, ["a"])
c = Page("c", 0, ["b"])

pagelist = {"a": a, "b": b, "c": c}

calcEq(pagelist)
print(sym.solve([pagelist[z].eq for z in pagelist], [pagelist[z].symbol for z in pagelist]))

print("\nDB")
db = sql.connect("my_wiki.sqlite")

curs = db.execute(
    '''
    SELECT p.page_title, COUNT(pl.pl_from) 
    FROM page p LEFT JOIN pagelinks pl ON p.page_id = pl.pl_from 
    GROUP BY 1''')

pagelist = {}
for i in curs:
    incommingLinks = [y[0] for y in db.execute('''
    SELECT p.page_title
    FROM page p LEFT JOIN pagelinks pl ON p.page_id = pl.pl_from 
    WHERE pl.pl_title = ?
    ''', [i[0]]) if y[0] is not None]
    pagelist[i[0]] = Page(i[0], i[1], incommingLinks)

start_time = t.time()
pagerankdict = pagerank(pagelist, 0)
print("iterativ", t.time() - start_time, "seconds")

start_time = t.time()
calcEq(pagelist)
# for z in pagelist:
#     print(pagelist[z].eq)
solvedPageRankDict = sym.solve([pagelist[z].eq for z in pagelist], [pagelist[z].symbol for z in pagelist])
print("sympy", t.time() - start_time, "seconds")

for z in pagelist:
    pagelist[z].pageRank = solvedPageRankDict[pagelist[z].symbol]

# for x, y in sorted(solvedPageRankDict.items(),
#                    key=lambda item: item[1], reverse=True):
#     print(str(x) + ": " + str(y))

maxlen = "<" + str(max([len(x) for x in pagelist.keys()]) + 1)
for i in sorted(pagelist.keys(), key=lambda item: pagelist[item].pageRank, reverse=True):
    print(f"{str(i) + ':':{maxlen}}",
          f"{(x1 := pagelist[i].pageRank):<18}",
          f"{(x2 := pagerankdict[pagelist[i].name]):<20}",
          f"{x3 :+.17f}" if (x3 := x2 - x1) != 0 else f"{0 :+.17f}")

pH().printPageRank()
