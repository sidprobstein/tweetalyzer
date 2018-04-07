#############################################
# datify-tweetalyzer

# reads multiple tweetalyzer output files and creates a date-aligned set of term counts
# it uses the date of each file automatically

import sys
import operator
import argparse
import csv
import glob
import os.path
import time

#############################################

def main(argv):
   
    # set up CLI parsing
    parser = argparse.ArgumentParser(description='Reads two or more tweetalyzer CSV files and produces a time-series report for all terms.')
    parser.add_argument('filespec', help="path to the input csv files")
    args = parser.parse_args()
      
    # initialize
    lstFiles = []
    lstDates = []
    
    if args.filespec:
        lstFiles = glob.glob(args.filespec)
    else:
        sys.exit()
            
    dictMerge = {}

    for sFile in lstFiles:
        
        # verify that input file claims to be a .csv
        if not sFile.endswith(".csv"):
            print "datify-tweetalyzer: error: inputfile must be in csv format..."
            sys.exit()
               
        # open the file
        try:
            f = open(sFile, 'r')
        except Exception, e:
            print "datify-tweetalyzer: error:", e
            sys.exit()

        print "datify-tweetalyzer: processing:", sFile,
        
        # get the file date/time
        sFileDate = time.ctime(os.path.getmtime(sFile))
        lstDates.append(sFileDate)

        csvReader = csv.reader(f)   
    
        # skip the header which is always in the form "TERM", "TF"
        lstRow = csvReader.next()

        # for each row:
            # if the row is not in the dict, then add a key "term" with value "{ $filedate$ : $tf$ }"
            # if the row is in the dict, then add a key to the value dict in the same form as above 

        for lstRow in csvReader:
            if dictMerge.has_key(lstRow[0]):
                dictTmp = dictMerge[lstRow[0]]
                dictTmp[sFileDate] = lstRow[1]
                dictMerge[lstRow[0]] = dictTmp
            else:
                dictTmp = { sFileDate : lstRow[1] }
                dictMerge[lstRow[0]] = dictTmp
            
        f.close()
        print "ok"
    
    lstDates.sort()
    sHeader = '"TERM",'
    for date in lstDates:
        sHeader = sHeader + '"' + date + '",'
    sHeader = sHeader[:-1]
    print sHeader
    for term in dictMerge:
        sRow = '"' + term + '",'
        for date in lstDates:
            if dictMerge[term].has_key(date):
                sRow = sRow + dictMerge[term][date] + ','
            else:
                sRow = sRow + '0,'
        sRow = sRow[:-1]
        print sRow
    
# end main

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end datify-tweetalyzer module