import time

class StatisticObject:
    def __init__(self,maxCallCnt=100000, statisticsFile='statistics.txt',version='unknown'):
        self.relCallCnt=0
        self.revolutions=0
        self.maxCallCnt=maxCallCnt
        self.startTime=time.time()
        self.stackLevel=0
        self.actionToDo=False
        self.statisticsFile=statisticsFile
        self.version=version

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

    def write_statistics(self):
        self.write_statistics_1()

    def save_statistics(self,*args):
        self.save_statistics_1()

    def print_statistics(self,*args):
        self.print_statistics_1()
        
    def write_statistics_1(self,*args):
           runtime=self.runtime()
           self.save_statistics_2(runtime,*args)
           self.print_statistics_2(runtime,*args)

    def save_statistics_1(self,*args):
           runtime=self.runtime()
           self.save_statistics_2(runtime,*args)

    def print_statistics_1(self,*args):
           runtime=self.runtime()
           self.print_statistics_2(runtime,*args)

    def save_statistics_2(self,runtime,*args):
        target = open(self.statisticsFile, 'a')
        target.write("Version: {0:s}\n".format(self.version))
        for ll in args:
            s=(ll[0]+': {0:'+ll[1]+'}\n')
            target.write((ll[0]+' {0:'+ll[1]+'}\n').format(ll[2]))
        target.write("Iterations: {0:d}\n".format(self.calls()))
        target.write("Seconds: {0:f}\n".format(runtime))
        target.write("\n")
        target.close()
    
    def print_statistics_2(self,runtime,*args):
        print("Version: {0:s}".format(self.version))
        for ll in args:
            print((ll[0]+': {0:'+ll[1]+'}').format(ll[2]))
        print("Iterations: {0:d}".format(self.calls()))
        print("Seconds: {0:f}".format(runtime))
        print("")
    


class GearStatisticObject(StatisticObject):
    def __init__(self,maxCallCnt=100000, resultFile='result.txt', statisticsFile='statistics.txt',version='unknown'):
        super().__init__(maxCallCnt=100000, statisticsFile='statistics.txt',version='unknown')
        self.resultFile=resultFile

    def formattedListPair(self,ll1,ll2,maxll):
        s1=ll1[:]
        s2=ll2[:]
        s1.extend((maxll-len(s1))*[0])
        s2.extend((maxll-len(s2))*[0])
        return('['+','.join('{0:2d}'.format(i) for i in s1)+'],['+','.join('{0:2d}'.format(i) for i in s2)+']')


    def formattedZippedListPair(self,ll1,ll2,maxll):
        s1=ll1[:]
        s2=ll2[:]
        s1.extend((maxll-len(s1))*[0])
        s2.extend((maxll-len(s2))*[0])
        return(' '.join('{0:2d} {1:2d}'.format(i,j) for i,j in zip(s1,s2)))


        
    def print_sprockets(self,sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,calledBy):
        if calledBy==1:
            s1=sprocket1
            s2=sprocket2
        elif calledBy==2:
            s1=sprocket2
            s2=sprocket1
        else:
            assert(False)        
        print(self.formattedListPair(s1,s2,maxs)+' '+self.formattedZippedListPair(s1,s2,maxs)+'{0:8.2f}'.format(self.runtime()))

    def print_solution(self,sprocket1,sprocket2,unused1,unused2,transformation,next1,next2,maxn,maxs,calledBy):
        runtime=round(self.runtime())
        if calledBy==1:
            s1=sprocket1
            s2=sprocket2
        elif calledBy==2:
            s1=sprocket2
            s2=sprocket1
        else:
            assert(False)        
        print("solution:")
        print(self.formattedListPair(s1,s2,maxs))
        print("Target Number:", maxn)
        print("Iterations:",self.calls())
        print("Seconds:",runtime)
        target = open(self.resultFile, 'a')
        target.write("Target Number: {0:d}\n".format(maxn))
        target.write("solution:\n")
        target.write(self.formattedListPair(s1,s2,maxs)+'\n')
        target.write("Iterations: {0:d}\n".format(self.calls()))
        target.write("Seconds: {0:d}\n".format(runtime))
        target.write("Version: {0:s}\n".format(self.version))
        target.write("\n")
        target.close()

    def write_statistics(self,maxn,maxs):
           self.write_statistics_1(["Target Number","d",maxn],["List Length","d",maxs])

    def save_statistics(self,maxn,maxs):
           self.save_statistics_1(["Target Number","d",maxn],["List Length","d",maxs])

    def print_statistics(self,maxn,maxs):
           self.print_statistics_1(["Target Number","d",maxn],["List Length","d",maxs])


