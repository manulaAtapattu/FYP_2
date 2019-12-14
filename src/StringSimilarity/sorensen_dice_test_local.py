
from sorensen_dice import SorensenDice

def main():
    a = SorensenDice(2)
    # s0 = ""
    # s1 = ""
    s2 = "That's interesting"
    s3 = " That's very interesting "
    distance_format = "distance: {:.4}\t between {} and {}"
    similarity_format = "similarity: {:.4}\t between {} and {}"
    # print(distance_format.format(str(a.distance(s0, s1)), s0, s1))
    # print(distance_format.format(str(a.distance(s0, s2)), s0, s2))
    # print(distance_format.format(str(a.distance(s0, s3)), s0, s3))
    # print(distance_format.format(str(a.distance(s1, s2)), s1, s2))
    # print(distance_format.format(str(a.distance(s1, s3)), s1, s3))
    print(distance_format.format(str(a.distance(s2, s3)), s2, s3))

    # print(similarity_format.format(str(a.similarity(s0, s1)), s0, s1))
    # print(similarity_format.format(str(a.similarity(s0, s2)), s0, s2))
    # print(similarity_format.format(str(a.similarity(s0, s3)), s0, s3))
    # print(similarity_format.format(str(a.similarity(s1, s2)), s1, s2))
    # print(similarity_format.format(str(a.similarity(s1, s3)), s1, s3))
    print(similarity_format.format(str(a.similarity(s2, s3)), s2, s3))



main()