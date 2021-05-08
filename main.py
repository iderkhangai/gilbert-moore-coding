import math

#input file name
ifname = "input.txt"
#output file name
ofname = "output.txt"

p = []  #Probablities
y = []  #Code letters
code = []  #Codes of The Probablities


def get_p_input_from_console():
    print("Enter The Probablities(-1 to stop): ")
    p = []
    while True:
        input_p = float(input("P" + str(len(p)) + " : "))
        if (input_p == -1):
            if len(p) == 0:
                p = [
                    0.08, 0.12, 0.27, 0.1, 0.12, 0.1, 0.06, 0.05, 0.04, 0.02,
                    0.03, 0.01
                ]
            print()
            print("Probilities:")
            print(p)
            print()
            return p
        if (input_p > 0 and input_p < 1):
            p.append(input_p)
        else:
            print("Invalid probablity!")


def get_code_letters_input_from_console():
    print("Enter The Number of Code Letters: ")
    n = int(input())
    print()
    print("Code Letters:")
    y = [*range(n)]
    print(y)
    print()
    return y


def get_p_input_from_file(filename):
    print("Reading from file " + ifname)
    print()
    p = []
    file1 = open(filename, "r+")
    lines = file1.readlines()
    file1.close()
    temp = str(lines[0]).replace(" ", "").split("=")
    strp = str(temp[1]).split(',')
    for sp in strp:
        p.append(float(sp))
    print("Probilities:")
    print(p)
    print()
    return p


def get_code_letters_input_from_file(filename):
    file1 = open(filename, "r+")
    lines = file1.readlines()
    file1.close()
    temp = str(lines[1]).replace(" ", "").split("=")
    sn = str(temp[1])
    n = int(sn)
    print("Code Letters:")
    y = [*range(n)]
    print(y)
    print()
    return y


def calc_x(p):
    print("Calculating x:")
    x = []
    for i in range(len(p)):
        sum = 0
        for j in range(i):
            sum += p[j]
        x.append(sum + p[i] / 2)
    print("x =", x)
    print()
    return x


def split_n(r, n):
    beg = r[0]
    end = r[1]
    print("for range [", beg, ",", end, "]")
    print("splitting by ", n)
    result = []
    width = end - beg
    step = width / n
    for i in range(n):
        a = beg + i * step
        b = beg + (i + 1) * step
        result.append([a, b])
    print("rl =\n" + '\n'.join(map(lambda x: str(x), result)))
    print()
    return result


def match_xlist_range(xl, r):
    ml = []
    beg = r[0]
    end = r[1]
    for i, x in enumerate(xl):
        print("for x [", i, "] in range ", r)
        if (x >= beg and x <= end):
            ml.append(x)
    print("ml = ", ml)
    print()
    return ml


def code(x, rl):
    print("for x =", x)
    print()
    for index, r in enumerate(rl):
        beg = r[0]
        end = r[1]
        if (x >= beg and x <= end):
            c = str(index)
            print("found x in rl[", index, "] =", r)
            print("xcode =", c)
            print()
            return c


def recrusivefun(subxl, beg, end, n, cl, xl, node):
    node += 1
    print("recrusive-ness starting node =", node)
    print()

    ml = [1, 1]
    rlist = split_n([beg, end], n)
    for ri, r in enumerate(rlist):
        print("node:", node, "checking", subxl, " for range =", r)
        print()
        ml = match_xlist_range(subxl, r)
        if len(ml) == 1:
            xi = xl.index(ml[0])
            print("adding code ", ri, " for x =", ml[0], "of index", xi)
            cl[xi] += str(ri)
            print("cl =", cl)
            print()
        elif len(ml) > 1:
            beg = r[0]
            end = r[1]
            for m in ml:
                xi = xl.index(m)
                print("adding code ", ri, " for x =", m, "of index", xi)
                cl[xi] += str(ri)
                print("cl =", cl)
                print()
            recrusivefun(ml, beg, end, n, cl, xl, node)
        else:
            print("ml =", ml)
            print()
    return cl


def gilbert_moore(p, y):

    n = len(y)
    #x calc...
    xl = calc_x(p)
    #code list result
    cl = ["" for x in xl]
    print("cl =", cl)
    print()
    cl = recrusivefun(xl, 0, 1, n, cl, xl, 0)
    print("result ")
    print('\n'.join(
        map(lambda x: "for p[" + str(cl.index(x)) + "] code = " + str(x), cl)))
    return cl


def write_result_to_output_file(p, y, code, ofname):
    file2 = open(ofname, "w")
    file2.writelines("------------- Here is Result -----------" + '\n\n')
    file2.writelines("p = "+str(p)+"\n\n")
    file2.writelines("y = "+str(y)+"\n\n")
    file2.writelines("Gilbert Moore Coding: \n\n")
    file2.writelines('\n'.join(
        map(lambda x: "p[" + str(cl.index(x)) + "] code = " + str(x), cl)))
    
    file2.writelines("\n\n")
    sumE = 0
    sumH = 0
    for i in range(len(p)):
        sumE += -1 * p[i] * math.log(p[i], len(y))
        sumH += p[i] * len(code[i])

    print(code)
    entroupy = sumE
    hSum = sumH
    #  a random variable is the average level of "information"
    print("Entropy value : ", entroupy)
    file2.writelines("Entropy value : " + str(entroupy) + "\n")
    # average code lenght
    print("h value : ", hSum)
    file2.writelines("H-(average code length) value : " + str(hSum) + "\n")
    effc = entroupy / hSum
    print("Efficiency = ", effc * 100, "%")
    file2.writelines("Entropy value : " + str(entroupy) + "\n")
    # closing the file after writing the result
    file2.close()


#probablity input...
#p = get_p_input_from_console()
p = get_p_input_from_file(ifname)
#get code letters
#y = get_code_letters_input_from_console()
y = get_code_letters_input_from_file(ifname)
#Done...
print("Done taking input...")
print()
cl = gilbert_moore(p, y)
write_result_to_output_file(p, y, cl, ofname)
