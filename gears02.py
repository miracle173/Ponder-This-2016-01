
import time


# try to find all solutions otherwise finish after a solution was found
ALL_SOLUTIONS=True

#import pdb; pdb.set_trace()

TAS_continue=1
TAS_no_solution=2
TAS_skip_remaining=3
TAS_solved=4

version='02.01'
statistic_file='statistics.txt'
resultfile='results.txt'

class StatisticObject:
    def __init__(self,maxCallCnt=100000):
        self.relCallCnt=0
        self.revolutions=0
        self.maxCallCnt=maxCallCnt
        self.startTime=time.time()
        self.stackLevel=0
        self.actionToDo=False

    def count(self):
        self.relCallCnt+=1
        if self.relCallCnt==self.maxCallCnt:
            self.relCallCnt=0
            self.revolutions+=1
            self.actionToDo=True
            
    def incStack(self):
        self.stackLevel+=1

    def decStack(self):
        self.stackLevel-=1

    def doAction(self):
        if self.actionToDo:
            self.actionToDo=False
            return(True)
        else:
            return(False)

    def runtime(self):
        return(time.time()-self.startTime)
        
    def calls(self):
        return(self.relCallCnt+self.revolutions*self.maxCallCnt)


def formattedListPair(ll1,ll2,maxll):
    s1=ll1[:]
    s2=ll2[:]
    s1.extend((maxll-len(s1))*[0])
    s2.extend((maxll-len(s2))*[0])
    return('['+','.join('{0:2d}'.format(i) for i in s1)+'],['+','.join('{0:2d}'.format(i) for i in s2)+']')


def formattedZippedListPair(ll1,ll2,maxll):
    s1=ll1[:]
    s2=ll2[:]
    s1.extend((maxll-len(s1))*[0])
    s2.extend((maxll-len(s2))*[0])
    return(' '.join('{0:2d} {1:2d}'.format(i,j) for i,j in zip(s1,s2)))


    
def print_sprockets(sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,calledBy,statisticObject):
    if calledBy==1:
        s1=sprocket1
        s2=sprocket2
    elif calledBy==2:
        s1=sprocket2
        s2=sprocket1
    else:
        assert(False)        
    print(formattedListPair(s1,s2,maxs)+' '+formattedZippedListPair(s1,s2,maxs)+'{0:8.2f}'.format(statisticObject.runtime()))

def print_solution(sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,calledBy,statisticObject):
    runtime=round(statisticObject.runtime())
    if calledBy==1:
        s1=sprocket1
        s2=sprocket2
    elif calledBy==2:
        s1=sprocket2
        s2=sprocket1
    else:
        assert(False)        
    print("solution:")
    print(formattedListPair(s1,s2,maxs))
    print("Target Number:", maxn)
    print("Iterations:",statisticObject.calls())
    print("Seconds:",runtime)
    target = open(resultfile, 'a')
    target.write("Target Number: {0:d}\n".format(maxn))
    target.write("solution:\n")
    target.write(formattedListPair(s1,s2,maxs)+'\n')
    target.write("Iterations: {0:d}\n".format(statisticObject.calls()))
    target.write("Seconds: {0:d}\n".format(runtime))
    target.write("Version: {0:s}\n".format(version))
    target.write("\n")
    target.close()

def init_all(maxn,maxs):
    return([[],[],[],[],[i==0 for i in range(0,maxn+1)],1,1,maxn,maxs,StatisticObject()])

def tryAddSprockets(sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,calledBy,statisticObject):
    assert(len(sprocket1)==len(unused1))
    assert(len(sprocket2)==len(unused2))
    assert(len(sprocket1)<=maxs)
    assert(len(sprocket2)<=maxs)


    statisticObject.count()

    sprocket1.append(next1)
    unused1.append(True)

    
    if len(sprocket1)>maxs:
        return(TAS_skip_remaining)

    if statisticObject.doAction():
        print_sprockets(sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,calledBy,statisticObject)

    if not sprocket2 :
        return(TAS_continue)
    
    for t in range(1,min(sprocket1[0]*sprocket2[-1]-1,sprocket2[0]*next1-1)):
        if not transformation[t]:
            return(TAS_skip_remaining)
        
    for j in range(len(sprocket2)):
        s=sprocket2[j]
        p=s*next1
        for t in [p-1,p,p+1]:
            if (t>0) and (t<=maxn):
                if not transformation[t]:
                    unused2[j]=False
                    unused1[-1]=False
                    transformation[t]=True
    for i,value in enumerate(unused1):
        if unused1[i]:
            never_needed=True
            for t in range(sprocket1[i],maxn+1,sprocket1[i]):
                if not transformation[t]:
                    never_needed=False
                    break
            if never_needed:
                return(TAS_no_solution)

    for i,value in enumerate(unused2):
        if unused2[i]:
            never_needed=True
            for t in range(sprocket2[i],maxn+1,sprocket2[i]):
                if not transformation[t]:
                    never_needed=False
                    break
            if never_needed:
                return(TAS_no_solution)
                
    for t in range(1,maxn+1):
        if not transformation[t]:
            return(TAS_continue)
    print_solution(sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,calledBy,statisticObject)
    return(TAS_solved)
    
    

def augmentSprocket1(sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,solutions,statisticObject):
    assert(len(sprocket1)==len(unused1))
    assert(len(sprocket2)==len(unused2))
    assert(len(sprocket1)<=maxs)
    assert(len(sprocket2)<=maxs)
    statisticObject.incStack()    
    for n in range(next1,maxn+1):
        mySprocket1=sprocket1[:]
        mySprocket2=sprocket2[:]
        myUnused1=unused1[:]
        myUnused2=unused2[:]
        mytransformation=transformation[:]      
        t=tryAddSprockets(mySprocket1,mySprocket2,myUnused1,myUnused2,mytransformation,n,next2,maxn,maxs,1,statisticObject)
        if t==TAS_continue:
            solutions=augmentSprocket2(mySprocket1,mySprocket2,myUnused1,myUnused2,mytransformation,n+1,next2,maxn,maxs,solutions,statisticObject)
            statisticObject.decStack()
        elif t==TAS_skip_remaining:
            statisticObject.decStack()
            return([])
        elif t==TAS_no_solution:
            pass
        elif t==TAS_solved:
            statisticObject.decStack()
            solutions.append([[mySprocket1[:],mySprocket2[:]]])
            if not ALL_SOLUTIONS:
                return(solutions)
        else:
            assert(False)
    return(solutions)

def augmentSprocket2(sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,solutions,statisticObject):
    assert(len(sprocket1)==len(unused1))
    assert(len(sprocket2)==len(unused2))
    assert(len(sprocket1)<=maxs)
    assert(len(sprocket2)<=maxs)
    
    statisticObject.incStack()    

    if sprocket1[0:-1]==sprocket2:
        next2=max(next2,sprocket1[-1])
    
    for n in range(next2,maxn+1):
        mySprocket1=sprocket1[:]
        mySprocket2=sprocket2[:]
        myUnused1=unused1[:]
        myUnused2=unused2[:]
        mytransformation=transformation[:]
        
        t=tryAddSprockets(mySprocket2,mySprocket1,myUnused2,myUnused1,mytransformation,n,next1,maxn,maxs,2,statisticObject)
        if t==TAS_continue:
            solutions=augmentSprocket1(mySprocket1,mySprocket2,myUnused1,myUnused2,mytransformation,next1,n+1,maxn,maxs,solutions,statisticObject)
            statisticObject.decStack()
        elif t==TAS_skip_remaining:
            statisticObject.decStack()
            return([])
        elif t==TAS_no_solution:
            pass
        elif t==TAS_solved:
            statisticObject.decStack()
            solutions.append([[mySprocket1[:],mySprocket2[:]]])
            if not ALL_SOLUTIONS:
                return(solutions)
        else:
            assert(False)
    return(solutions)

def write_statistics(statfile,maxn,maxs,statisticObject):
    target = open(statfile, 'a')
    target.write("Target Number: {0:d}\n".format(maxn))
    target.write("List Length: {0:d}\n".format(maxs))
    target.write("Iterations: {0:d}\n".format(statisticObject.calls()))
    target.write("Seconds: {0:f}\n".format(statisticObject.runtime()))
    target.write("Version: {0:s}\n".format(version))
    target.write("\n")
    target.close()


[sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,statisticObject]=init_all(56,6)
[sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,statisticObject]=init_all(40,5)
[sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,statisticObject]=init_all(21,3)
[sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,statisticObject]=init_all(31,4)
[sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,statisticObject]=init_all(41,5)
[sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,statisticObject]=init_all(40,5)
[sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,statisticObject]=init_all(56,6)
[sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,statisticObject]=init_all(31,4)

[sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,statisticObject]=init_all(10,2)

ll=augmentSprocket1(sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,[],statisticObject)

write_statistics(statistic_file,maxn,maxs,statisticObject)

# [ 1, 2,12,13,40,47],[ 1, 3, 8, 9,15,19]  1  1  2  3 12  8 13  9 40 15 47 1922648.66
