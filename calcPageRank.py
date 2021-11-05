class Page:
    def __init__(self, name, outgoingLinks: int, refPages: [str]):
        self.name = name
        self.outgoingLinks = outgoingLinks
        self.pageRank = 1
        self.refPages = refPages


def pagerank(pages: dict[str, Page], zz):
    zz += 1
    ldfac = 0.85
    _lowlimit = 0.999999999999999
    _highlimit = 1.000000000000001
    tmpRanks = {}
    for z in pages:
        tmpRanks[z] = calc_formula(z, pages, ldfac)

    test = [_lowlimit < pages[z].pageRank / tmpRanks[z] < _highlimit for z in tmpRanks]
    # test = [pages[z].pageRank / tmpRanks[z] == 1 for z in tmpRanks]
    if all(test):
        print(zz)
        return {z: pages[z].pageRank for z in pages}
    else:
        for z in pages:
            pages[z].pageRank = tmpRanks[z]
        return pagerank(pages, zz)


def calc_formula(calcpage: str, pages: dict[str, Page], ldfac: float):
    x = (1 - ldfac)
    y = 0
    for z in pages[calcpage].refPages:
        if pages[z].outgoingLinks != 0:
            y = y + pages[z].pageRank / pages[z].outgoingLinks

    return x + ldfac * y


print("P1")
a = Page("a", 1, ["b"])
b = Page("b", 1, ["a"])

pagelist = {"a": a, "b": b}
print(pagerank(pagelist, 0))

print("P2")
a = Page("a", 1, ["c"])
b = Page("b", 1, ["a"])
c = Page("c", 1, ["a"])

pagelist = {"a": a, "b": b, "c": c}

print(pagerank(pagelist, 0))

print("P3")
a = Page("a", 2, ["b"])
b = Page("b", 2, ["a"])
c = Page("c", 0, ["a", "b"])

pagelist = {"a": a, "b": b, "c": c}

print(pagerank(pagelist, 0))

print("P4")

a = Page("a", 1, [])
b = Page("b", 1, ["a"])
c = Page("c", 0, ["b"])

pagelist = {"a": a, "b": b, "c": c}

print(pagerank(pagelist, 0))
