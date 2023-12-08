# class State:
#
#     def __init__(self, L1=None, L2=None, H1="", H2=""):
#         self.h1 = H1
#         self.h2 = H2
#         self.l1 = L1 if L1 is not None else []
#         self.l2 = L2 if L2 is not None else []
#     def __hash__(self):
#         return hash((tuple(self.l1), tuple(self.l2), self.h1, self.h2))
#     def print_state(self):
#         print(f"{self.h1},{self.h2},{self.l1},{self.l2}")
#
class State:

    def __init__(self, L1=None, L2=None, H1="", H2=""):
        self.h1 = H1
        self.h2 = H2
        self.l1 = L1 if L1 is not None else []
        self.l2 = L2 if L2 is not None else []
    def __hash__(self):
        return hash((tuple(self.l1), tuple(self.l2), self.h1, self.h2))
    def print_state(self):
        print(f"{self.h1},{self.h2},{self.l1},{self.l2}")

