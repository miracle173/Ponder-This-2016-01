Version='gears03 02.1'
'''
gears03 02:
bug in tracing block. wrong value was displayed
another bug in tracing block. wrong value was displayed
'''


import tracing
import copy

# [2, 5, 8, 9, 13, 7], [1, 6, 3, 9, 4, 7]

TRACE_ON=False
ASSERT_ON=__debug__

def precalc(maxn):
    #products
    products=[[]]
    for n in range(1,maxn+1):
        ll=[]
        for i in range(1,n+1):
            if n%i==0:
                ll.append((i,n//i))
        products.append(ll)
    #gears
    gears=[]
    for n in range(0,maxn+1):
        ss=set(products[n])
        if n>1:
            ss=ss.union(set(products[n-1]))
        if n<maxn:
            ss=ss.union(set(products[n+1]))
        ll=list(ss)
        ll.sort()
        gears.append(ll)
    
    transformation=[i==0 for i in range(0,maxn+3)]
    return([gears,transformation])

        
def check_next_free_1(next_free,sprocket1,sprocket2,gears,
                    transformation,rejected, used, maxn,maxs,solutions,statistics):

        

    next_free_found=False
    for i in range(next_free+1,maxn+1):
        if not transformation[i]:
            next_free=i
            next_free_found=True
            break
    if not next_free_found:
        # solution found
        solutions.append(sorted([sorted(sprocket1[:]),sorted(sprocket2[:])]))
        print("Solution {0:d}: ".format(len(solutions)),solutions[-1])
        return(solutions)

    if ASSERT_ON:   
        #print("rejected start: ",rejected)
        mySprocket1=sprocket1[:]
        mySprocket2=sprocket2[:]
        myUsed=used[:]
        myRejected=rejected[:]

    
    rejectCount=0
    pairlist=gears[next_free][:]
    while pairlist:
        statistics.count()
        if ASSERT_ON:
            assert(mySprocket1==sprocket1)
            assert(mySprocket2==sprocket2)
            assert(myUsed==used)
            
        if TRACE_ON:
            print("while loop:")
            print("transformations",[i for i in range(1,maxn+1) if not transformation[i]])
            print("gears for",next_free,":",pairlist)
            print("rejected",rejected)
            print("used",used)
            print("gears",gears)
            print("sprockets",sprocket1,sprocket2)

        (g1,g2)=pairlist.pop()

        if statistics.doAction():
            print(statistics.formattedListPair(sprocket1,sprocket2,maxs)+' {0:10d} {1:15.2f}'.format(statistics.calls(),statistics.runtime()))
        if TRACE_ON:
            print("try ",(g1,g2))
            print("remaining gears for this number",pairlist)
            print("")
        new_g1=g1 not in sprocket1
        new_g2=g2 not in sprocket2
        
        if new_g1:
            if len(sprocket1)>=maxs:
                rejected.append((g1,g2))
                rejectCount+=1
                if TRACE_ON:
                    print("reject")
                continue
            for g in sprocket2:
                if (g1,g) in rejected:
                    rejected.append((g1,g2))
                    rejectCount+=1
                    if TRACE_ON:
                        print("reject")

                    continue
        if new_g2:
            if len(sprocket2)>=maxs:
                rejected.append((g1,g2))
                rejectCount+=1
                if TRACE_ON:
                    print("reject")
                continue
            for g in sprocket1:
                if (g,g2) in rejected:
                    rejected.append((g1,g2))
                    rejectCount+=1
                    if TRACE_ON:
                        print("reject")
                    continue
                
        if TRACE_ON:
            print("accepted")
        used.append((g1,g2))
        myTransformation=transformation[:]
        if new_g1:
            for g in sprocket2:
                if g1*g-1<=maxn:
                    myTransformation[g1*g-1:g1*g+2]=[True,True,True]
        if new_g2:
            for g in sprocket1:                
                if g*g2-1<=maxn:
                    myTransformation[g*g2-1:g*g2+2]=[True,True,True]
        if new_g1:
            sprocket1.append(g1)
        if new_g2:
            sprocket2.append(g2)
            
        if g1*g2<=maxn:
            myTransformation[g1*g2]=True
        if g1*g2+1<=maxn:
            myTransformation[g1*g2+1]=True
        if g1*g2-1<=maxn:
            myTransformation[g1*g2-1]=True
            
        if TRACE_ON:
            print("after accepting:")
            print("sprockets",sprocket1,sprocket2)
            print("used",used)
            print("rejected",rejected)
            print("transformations",[i for i in range(1,maxn+1) if not myTransformation[i]])
            print("")

        if TRACE_ON:
            print("goto level",statistics.stackLevel+1)
            
        statistics.incStack()
        ll=check_next_free_1(next_free,sprocket1,sprocket2,
                gears,myTransformation,rejected,used,
                maxn, maxs,solutions,statistics)
        statistics.decStack()
        
        if TRACE_ON:
            print("back from level",statistics.stackLevel+1)

    
        rejected.append((g1,g2))
        rejectCount+=1
        used.pop()
        if new_g1:
            sprocket1.pop()
        if new_g2:
            sprocket2.pop()
            
        if TRACE_ON:
            print("reject", (g1,g2))
            
    for i in range(0,rejectCount):
        rejected.pop()

    if ASSERT_ON:
        #print("rejected end: ",rejected)
        assert(myRejected==rejected)
    
    return(solutions)


def check_next_free(maxn, maxs,statistics):
    ll=precalc(maxn)
    return(sorted(check_next_free_1(1,[],[],ll[0],ll[1],[],[],
                                    maxn, maxs,[],statistics)))

MAXN=40
MAXS=5

MAXN=19
MAXS=3

MAXN=58
MAXS=6

MAXN=21
MAXS=3

MAXN=57
MAXS=6

MAXN=31
MAXS=4

MAXN=10
MAXS=2


stat=tracing.GearStatisticObject(resultFile='test2_result.txt', statisticsFile='test2_statistics.txt',version=Version)

        
            
ss=check_next_free(MAXN,MAXS,stat)        

print(ss)

stat.write_statistics(MAXN,MAXS)
