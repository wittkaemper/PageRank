import sqlite3 as sql

from Page import Page as p


class PageHandler:
    def __init__(self):
        self.pages: dict[str, p] = {}
        db = sql.connect("my_wiki.sqlite")

        curs = db.execute(
            '''
            SELECT p.page_title, COUNT(pl.pl_from) 
            FROM page p LEFT JOIN pagelinks pl ON p.page_id = pl.pl_from 
            GROUP BY 1''')

        for i in curs:
            incommingLinks = [y[0] for y in db.execute('''
            SELECT p.page_title
            FROM page p LEFT JOIN pagelinks pl ON p.page_id = pl.pl_from 
            WHERE pl.pl_title = ?
            ''', [i[0]]) if y[0] is not None]
            self.pages[i[0]] = p(i[0], i[1], incommingLinks)

    def calcPageRank(self):
        ldfac = 0.85
        _lowlimit = 0.99999999999999
        _highlimit = 1.00000000000001
        tmpRanks = {}
        for z in self.pages:
            tmpRanks[z] = self.pages[z].calc_formula(self.pages, ldfac)

        test = [_lowlimit < self.pages[z].pageRank / tmpRanks[z] < _highlimit for z in tmpRanks]
        # test = [pages[z].pageRank / tmpRanks[z] == 1 for z in tmpRanks]
        if all(test):
            return {z: self.pages[z].pageRank for z in self.pages}
        else:
            for z in self.pages:
                self.pages[z].pageRank = tmpRanks[z]
            return self.calcPageRank()

    def printPageRank(self):
        self.calcPageRank()
        maxlen = "<" + str(max([len(x) for x in self.pages.keys()]) + 1)
        for i in sorted(self.pages.keys(), key=lambda item: self.pages[item].pageRank, reverse=True):
            print(f"{str(i) + ':':{maxlen}}",
                  f"{self.pages[i].pageRank:<18}")

        print(f"{'Sum:':{maxlen}}", sum([x.pageRank for x in self.pages.values()]))


if __name__ == "__main__":
    PageHandler().printPageRank()
