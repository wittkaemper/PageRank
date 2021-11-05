from __future__ import annotations


class Page:
    def __init__(self, name:str, outgoingLinks: int, refPages: list[str]):
        self.name = name
        self.outgoingLinks = outgoingLinks
        self.pageRank = 1
        self.refPages = refPages

    def calc_formula(self, pages: dict[str, Page], ldfac: float) -> float:
        x = (1 - ldfac)
        y = 0
        for z in self.refPages:
            if pages[z].outgoingLinks != 0:
                y = y + pages[z].pageRank / pages[z].outgoingLinks

        return x + ldfac * y
