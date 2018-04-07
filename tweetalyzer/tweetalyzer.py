    #############################################
# tweetalyzer

# reads the twitter analytic CSV file and finds the top terms associated with good outcomes

import sys
import operator
import argparse
import csv

#############################################

def removeStopChars(sString):
    
    # list of stop characters
    # tbd: move these to a file...
    lstStopChars = [ '.', ',', '!', '?', ';', ':', '@', '#', '(', ')', "''s", "\'", '\"' ,'&', '|' ]    
    
    sCleaned = ""
    for token in sString:
        # strip tokens
        for target in lstStopChars:
            # remove any targets found
            token = token.replace(target, '')
        sCleaned = sCleaned + token
        
    return sCleaned # omit the extra space at the end

# end removeStopChars

def removeStopWords(sString):

    # list of stop words
    # tbd: move these to a file...
    lstStopWords = [ "-", "a", "as", "an", "and", "amp", "at", "are", "be", "by", "can", "dont", "for", "gt", "how", "have", "i", "if", "it", "its", "is", "in", "into", "lt", "me", "mt", "of", "on", "rt", "to", "the", "that", "this", "us", "you", "your", "youre", "with" ]

    sCleaned = ""
    for token in sString.split():
        bFound = False
        # strip tokens
        for target in lstStopWords:
            # remove short tokens
            if len(token) < 3:
                # also stopword
                bFound = True
            # remove any targets found
            if token.lower() == target:
                # stopword
                bFound = True
        if not bFound:
            sCleaned = sCleaned + token + " "
    
    return sCleaned[:-1] # omit the extra space at the end

# end removeStopWords

#############################################

def main(argv):
   
    # set up CLI parsing
    parser = argparse.ArgumentParser(description='Reads the twitter analytic output, in CSV format, and finds the top words and phrases associated with specific outcomes')
    parser.add_argument('-m', '--min', type=int, default=3, help="minimum number of observations to report")
    parser.add_argument('-g', '--grams', type=int, default=3, help="maximum number of n-grams to analyze")
    parser.add_argument('-s', '--strip', action='store_true', default=False)
    parser.add_argument('-w', '--stopwords', action='store_true', default=False)
    parser.add_argument('file', help="path to the input csv file")
    parser.add_argument('targets', nargs=argparse.REMAINDER, help="list of row names that designate an outcome of interest when > 0")
    args = parser.parse_args()

    # for convenience
    nMaxGrams = args.grams
    nMin = args.min
       
    # check for an input file  
    if args.file:
        sFilename = args.file
    else:
        # no file - exit - parser will take care of usage/error reporting
        sys.exit(1)
        
    # verify that input file claims to be a .csv
    if not sFilename.endswith(".csv"):
        print "tweetalyzer: error: inputfile must be in csv format..."
        sys.exit()
           
    # open the file
    try:
        f = open(sFilename, 'r')
    except Exception, e:
        print "tweetalyzer: error:", e
        sys.exit()
        
    csvReader = csv.reader(f)   

    # initialize
    lstTargets = []
    
    # process the csv file   
    
    # process the header, populate lstTargets with the column numbers based on target names provided on the CLI

    nCol = 0
    lstRow = csvReader.next()
    for col in lstRow:
        for target in args.targets:
            if col.lower() == target.lower():
                # hit
                lstTargets.append(nCol)
                break
        nCol = nCol + 1
    
    if len(lstTargets) == 0:
        # no targets found
        print "tweetalyzer: no targets matched the header row..."
        sys.exit()

    # now process the rest of the file
    
    lstGrams = []  # list to store window of grams
    dictGrams = {}
    nRow = 0  # row number
    xTWEETTEXT = 2  # tweet text column
         
    for lstRow in csvReader:
        nRow = nRow + 1
        # sum positive outcomes in target columns
        nPositive = 0
        for target in lstTargets:
            nPositive += int(lstRow[target])
        if nPositive > 0:
            # this tweet resulted in a target outcome
            # process the tweet text
            
            # remove stop chars, if requested
            if args.strip:
                sTweetRaw = removeStopChars(lstRow[xTWEETTEXT].lower())
            else:
                sTweetRaw = lstRow[xTWEETTEXT].lower()
            
            # remove stopwords, if requested
            if args.stopwords:
                sTweetRaw = removeStopWords(sTweetRaw)
                
            # gram analysis...
            for token in sTweetRaw.split():
                # add to the gram list
                lstGrams.append(token)
                # if the gram list is full, delete the left-most
                if len(lstGrams) > nMaxGrams:
                    lstGrams = lstGrams[1:len(lstGrams)]
                # now process all grams
                sLast = ""
                for n in range(1, nMaxGrams + 1):
                    sGram = '_'.join(lstGrams[-1*n:])
                    if sGram != sLast:
                        if sGram != "":
                            if dictGrams.has_key(sGram):
                                dictGrams[sGram] += 1
                            else:
                                dictGrams[sGram] = 1
                    sLast = sGram
            
    # sort the dictionary by TF
    dictSorted = sorted(dictGrams.iteritems(), key=operator.itemgetter(1), reverse=True)
        
    # output results...
    print '"TERM","TF"'
    for (term, count) in dictSorted:
        if int(count) > int(nMin):
            tmpTerm = '"' + term + '",' + str(count)
            print tmpTerm
            
    f.close()
    
# end main

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end tweetalyzer module