import os

class MutateData(object):
    """description of class"""

    def ShortenRed(datalist):
        outdatalist = []
        startepoc = datalist[0][0]
        cyclecount = 0
        wasred = 0
        recordcount = 0
        nmutated = 0
        inmutation = False
        deltatime = 0.0;
        for record in datalist:
            newrecord = record.copy()
            if (record[1] == 1):
                wasred = wasred + 1  #wasred is to flag cycles for counting
                if (( (cyclecount % 3) == 1) and (nmutated < 46)):
                # every third cycle...after red time > x, start setting red to green
                    redtime= record[2]
                    if (redtime > 4.):
                        if (not inmutation):  # start of mutation
                            inmutation = True
                            nmutated = nmutated + 1
                            startredtime = prevredtime;
                        inmutation = True
                        newrecord[1] = 3  # mutate on this red, make it green
                        deltatime = redtime - startredtime; #redtime is last red time, add to green time
                        newrecord[2] = deltatime;
                        recordcount = recordcount + 1
                    else:
                        prevredtime = record[2]
            elif (record[1] == 3):  # green 
                
                if (wasred > 0):
                    cyclecount = cyclecount+1; # cycles start on Red, when off read increment cycle count
                    wasred = 0;   
                    #if (inmutation):
                    #    newrecord[2] = record[2] + deltatime;
                if (inmutation):
                     newrecord[2] = record[2] + deltatime;
            else:
                inmutation = False # turn off mutation on yellow

            outdatalist.append(newrecord)
        
        print("++++++++++>>> records changed ",recordcount," mutations: ",nmutated," cycles : ",cyclecount)
        return outdatalist

#--------------------------------------------------------------------------------------
    def ShortenGreen(datalist,shortestredgreen):
        outdatalist = []
        thisdata = []
        cyclecount = 0
        redtime = 0.
        maxred = shortestredgreen - 1.
        wasred = False
        nmutated = 0
        nrecords = 0
        inmutation = False
        for record in datalist:
            newrecord = record.copy()
            #print(" debug processing record: ",record)
            if (record[1] == 1):  #red
                
                if (wasred == False):  #new cycle
                    cyclecount = cyclecount + 1
                    greentime = 0.
                    if (( (cyclecount % 3) == 1) and (nmutated < 46)):
                        inmutation = True # start the mutation
                        nmutated = nmutated + 1

                redtime = record[2]
                #inmutation = False
                wasred = True
            if (record[1] == 3):  # green 
                greentime = record[2]
                wasred = False
                if (inmutation):
                    thisdata.append(record)

            if (inmutation):
                if (record[1] == 4):   ## yellow => end of cycle
                    wasred = False
                    inmutation = False
                    ###PROCESS HERE***
                    redgreentime = redtime + greentime
                    print("debug process here beforedata...")
                    
                    if (greentime > 3.9):
                        #for r in thisdata:
                        #    print("debug ",r)
                        outdatalist = MutateData.modthiscycle(thisdata,outdatalist,redgreentime)
                    else:
                        for r in thisdata:
                            outdatalist.append(r)
                    thisdata.clear()
                else:
                    thisdata.append(record)
            else:  # not inmutation
                outdatalist.append(record)

        return outdatalist

    def modthiscycle(thisdata,outdatalist,redgreentime):
        lasttime = 0
        ismutate = False
        wasred = False
        wasgreen = False
        lastgreentime = 0.
        maxred = redgreentime - 4.0

        for record in thisdata:
            newrecord = record.copy()
            if (record[1] == 1):  #red
                lasttime = record[2]
                ismutate = False
                wasred = True
                wasgreen = False
            if (record[1] == 3):  # green 
                greentime = record[2]
                ismutate = True

                if ((record[2] + lasttime) >= maxred):
                    ismutate = False
                    # no longer mutating
                    newrecord[2] = record[2] - lastgreentime

                if (ismutate):
                    newrecord[1] = 1 # continue red
                    newrecord[2] = record[2] + lasttime
                    lastgreentime = greentime
                outdatalist.append(newrecord)
                print("appending: ",newrecord)
        return outdatalist
        
