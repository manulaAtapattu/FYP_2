from src.StringSimilarity.sorensen_dice import SorensenDice


def main(s1, s2):
    a = SorensenDice(2)
    # distance_format = "distance: {:.4}\t between {} and {}"
    # similarity_format = "similarity: {:.4}\t between {} and {}"
    # print(distance_format.format(str(a.distance(s1, s2)), s1, s2))
    # print(similarity_format.format(str(a.similarity(s1, s2)), s1, s2))
    return a.similarity(s1, s2)