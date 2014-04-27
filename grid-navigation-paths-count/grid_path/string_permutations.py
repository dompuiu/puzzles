from itertools import permutations
class Permutations:

    def __init__(self, string):
        self.string = string

    def get_permutations(self):
        return self.permute(self.string)

    def permute(self, string):
        if len(string) == 0:
            return set([''])
        elif len(string) == 1:
            return set([string])

        l = set()

        for i in range(len(string)):
            letter = string[i]
            rest = self.permute(string[0:i] + string[i+1:])

            for w in rest:
                l.add(w + letter)
                l.add(letter + w)

        return l