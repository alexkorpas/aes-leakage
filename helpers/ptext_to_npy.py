import sys
import numpy as np

if __name__ == '__main__':
    f = open(sys.argv[1], "r")
    outfile = sys.argv[2]
    print(outfile)

    res = []
    for x in f:
        temp = []
        for c in x:
            temp.append(ord(c))
        res.append(temp)
    f.close()

    A = np.array([np.array(x) for x in res])
    np.save(outfile, A)
