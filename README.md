# tweetalyzer

Python script to read the twitter analytics export, in CSV format, and identify the top concepts associated with particular outcomes like retweets or follows.

---

# tweetalyzer.py

Reads the twitter analytic output, in CSV format, and finds the top words and phrases associated with specific outcomes

## Usage
```
python tweetalyzer.py [-m OBS] [-g GRAMS] [-sw] file targets
```	

## Arguments
```
-m  minimum number of observations to report
-g  maximum number of n-grams to analyze
-s  strip special characters before analyzing
-w  remove stopwords before analyzing
file    the full path to the twitter analytic export file in CSV format
targets list of row names that designate an outcome of interest when > 0
```

---

# datify-tweetalyzer.py

This python script reads one or more outputs from the tweetalyzer, in CSV format, and transforms them into a unified time series for trend analysis.

## Usage
```
python datify-tweetalyzer.py filespec
```	

## Arguments
```
filespec: path to one or more tweetalyzer output files in csv format
```