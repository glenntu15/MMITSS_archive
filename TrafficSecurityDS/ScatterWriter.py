import math

class ScatterWriter(object):
    """Writes data for scatter plots   """
    def WriteScatter(name, cycledata, cycledata2):
        print(" in write scatter")
        outfilename = outfilename = name+"_ScatterCycle_Data.csv"
        print(" Opening file: ",outfilename)
        try:
            outfile = open(outfilename, 'w')
        except IOError:
            print(" could not open file")
            exit()
        outfile.write("DSN"+","+name+","+"DST,standardpairs\n")
        lmaj = len(cycledata)
        lmin = len(cycledata2)
    # # *** if data for major and minor have been written
        if (lmaj > 5 and lmin > 5): 
            outfile.write("Red_Maj,Major,Red_Min,Minor\n")
        else:
            outfile.write("Red_Maj,Major\n")
        
        lim = lmaj;
        if (lmin > 5):
            if (lmin < lim):
                lim = lmin
        lim = 40 #-------------------------LIMIT 40 cycles for debugging 
        for i in range(0,lim):
            point = cycledata[i]
            string = "{:.4f}".format(point[2]) + "," + "{:.4f}".format(point[3]) + ","
            if (point[3] < 17.):
                print("r: ", point[2]," g: ",point[3]," M: ",point[5])
            if (lmin > 5):
                point = cycledata2[i]
                string = string + "{:.4f}".format(point[2]) + "," + "{:.4f}".format(point[3]) + "\n"
            else:
                string = string + "\n"
            outfile.write(string)

       

        outfile.close()
#-----------------------------------------------------------------------------------------
# THIS CODE FOR NORMALIZED DATA CYCLES
    def WriteNormalScatter(name,cycledata, cycledata2):
        print(" in write Normal scatter")
        outfilename = name+"_ScatterCycleNormal_Mut4_ShortGreenMinor_Data.csv"
        print(" Opening file: ",outfilename)
        try:
            outfile = open(outfilename, 'w')
        except IOError:
            print(" could not open file")
            exit()
#
# OPEN DEBUG FILES
#
        #debug1name = name +"_NormalDebug_Data.csv"
        #print(" Opening file: ",debug1name)
        #try:
        #    debug1 = open(debug1name, 'w')
        #except IOError:
        #    print(" could not open file")
        #    exit()
#
# End Debug File open

        lmaj = len(cycledata)
        lmin = len(cycledata2)
        outfile.write("DSN"+","+name+" Limit 4 s,"+"DST,standardpairs,metadata,2\n")
    # # *** if data for major and minor have been written
        if (lmaj > 5 and lmin > 5): 
            outfile.write("Red_Maj,Major,Red_Min,Minor\n")
        else:
            outfile.write("Red_Maj,Major\n")
        
        lim = lmaj;
        if (lmin > 5):
            if (lmin < lim):
                lim = lmin

        maxfr = 0.
        minfg = 999.
        ##lim = 40 #-------------------------LIMIT 40 cycles for debugging 
        for i in range(0,lim):
            point = cycledata[i]
            total = point[2] + point[3] + point[4]
            if (math.isnan(total) or math.isnan(point[2]) or math.isnan(point[3])):
                string = "??,??,"
            else:
                r = point[2]
                fr = r / total
                g = point[3]
                
                fg = g / total
                
                string = "{:.4f}".format(fr) + "," + "{:.4f}".format(fg) + "," 
                metadata = point[5]
                
                #dbstring = "{:.2f}".format(point[2]) + "," + "{:.2f}".format(point[3]) + "," 
                #dbstring = dbstring + "{:.2f}".format(point[4]) + "," + point[5] + "\n";
                #print(" DEBUG STRING: ",dbstring)
                #debug1.write(dbstring)
                #if (r < 4.):
                #    print(" this is mutated: ",point[5]," point is: (",fr,",",fg,") metadata: ",point[5])
                #    #debug1.write(dbstring)
                #    string = string + "\n"
                #    outfile.write(string)

                #Minor Road data
                if (lmin > 5):
                    
                    point = cycledata2[i]
                    total = point[2] + point[3] + point[4]
                    if (math.isnan(total) or math.isnan(point[2]) or math.isnan(point[3])):
                        string = string + "??,??," + metadata + ",??,\n"
                    else:
                        r = point[2]
                        #if (r > 380.):
                        #    print(" point metadata ",metadata)
                        fr = r / total
                        #if (fr > .97):
                        #    print(" other point fr ",fr," metadata ",metadata)
                        
                        g = point[3]
                        fg = g / total
                        #if (fr < .40 and fg > .55):
                        #    print(" ***point: fr, ", fr, " fg, ",fg," metadata",point[5])
                        #    print(" Red ", r, " Green: ", g, "total = ",total)
                        string = string + "{:.4f}".format(fr) + "," + "{:.4f}".format(fg)
                        ##   --- leave out metadata
                        string = string + "," + metadata + "," + point[5] + "\n"
                        # string = string + "\n"
                        if (fr > maxfr):
                            maxfr = fr
                        if (fg < minfg):
                            minfg = fg
                else:
                    string = string + "\n"
                outfile.write(string)
        #debug1.close()
        outfile.close()


