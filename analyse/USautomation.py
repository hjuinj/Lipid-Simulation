import re
import sys
import os
from subprocess import call


def simple_check(dir = "./"):
    output = [i.split(".")[-1] for i in os.listdir(dir)]
    print "number of .mdp files: %d\nnumber of .ndx files: %d\nnumber of .top files: %d" %(output.count("mdp"), output.count("ndx"), output.count("top"))

#simple_check()

def select_frames( end, frames, start = 0):
    step = (start + end) / float(frames - 1)
    result = []
    for i in range(frames):
        result.append(start)
        start += step
    return [int(i) for i in result]

def order_frames(frames):
    """
    Order by prioritising frames that are most distant from frames that have been selected in the past
    """
    #result = [frames.pop(0), frames.pop(-1)]
    result = [frames.pop(0)]
    while len(frames) > 0:
        which = -1
        if len(result) %2 == 0:
            min_sum = 10 ** 10
            for i in frames:
                tmp = abs(sum(np.array(result) - i))
        #        print tmp
                if tmp < min_sum:
        #            print "if"
                    min_sum = tmp
                    which = i
        else:
            max_dis = -1
            for i in frames:
                tmp = sum(abs(np.array(result) - i))
                print tmp
                if tmp > max_dis:
                    max_dis = tmp
                    which = i
        print "asdfas"
        frames.remove(which)
        result.append(which)
    return result

order_frames(select_frames(end = 100, frames = 17))
x = abs(np.array([1,2,3]) - 9)
sum(x)
x.remove(2)
a.pop(0)
a = [1,2,3]
a.remove(2)
a



#call("gmx grompp -p topol.top -c npt.gro -f npt.mdp -o npt.tpr ", shell = True)
# call(["gmx", "grompp", "-p", "topol.top", "-c", "npt.gro", "-f", "npt.mdp", "-o", "npt.tpr"], shell = True)
#make_tpr("./npt.gro")
os.system("mkdir tmp")
os.system("cp ~/Sandbox/build/insert/* ./tmp")
os.system("rm -rf tmp")
