#!/usr/bin/env python

import time, os, sys
from optparse import OptionParser

version = "0.1.2"  

# Simple colors class for pretty CLI output
# ===============================================================
class clrs:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    RESET = '\033[0m'

    def disable(self):
        self.PURPLE = ''
        self.BLUE = ''
        self.GREEN = ''
        self.WARNING = ''
        self.ERROR = ''
        self.RESET = ''


# Flash log tracking class
# ===============================================================
class Flog:

    # Main class constructor
    # ===============================================================

    def __init__( self, argv):  
        # reset filters/params
        self.levels = [ "ALL", "DEBUG", "INFO", "WARNING", "ERROR", "FATAL" ]
        self.filterWord = ''    
        self.filterLevel = 0;

        # set CLI arguments options
        usage = "usage: %prog [options] arg" + "\n"
        usage += "This program reads the Flash log file (flashlog.txt) from its default location" + "\n"
        usage += "and shows its content on screen, using fancy colors for different log levels." + "\n"
        usage += "It also allows filtering by log level (will show all logs with level equal or greater than the one supplied)" + "\n"
        usage += "and/or keyword (non case-sensitive)."
        parser = OptionParser(usage)
        parser.add_option("-f", "--filter", dest="filter", help="Filter by category")
        parser.add_option("-l", "--level", dest="level", help="Filter by log level (valid values are: " + (", ").join(self.levels) + ")")
        (options, args) = parser.parse_args()

        # print welcome message, clearing screen out first, and saving filter keyword if provided
        print "%c[2J" % (27)
        print "\nFLOG " + version + " (Flash log viewer)"
        if options.filter:
            print "    - filtering by keyword: \"" + options.filter + "\""
            self.filterWord= options.filter.lower()
        if options.level:
            levelIndex = self.levels.index( options.level.upper() )
            if levelIndex == -1:
                print "Error. Level option must be one of these: " + str(self.levels)
                sys.exit(2)
            print "    - filtering by level: \"" + options.level.upper() + "\""
            self.filterLevel = levelIndex
        print "Program ready. You can now run your Flash movie, matching logs will be shown here."
        # start tracking logs
        self.trackFlashLog()


    # Infinite loop to watch log file
    # ===============================================================
    def trackFlashLog( self ):
        # Open the log file (assuming default path for Mac OS)
        homeDir =  os.environ['HOME']
        logfile = open( homeDir + "/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt" )

        # get the log file contents, and iterate over lines
        loglines = self.follow(logfile)
        for line in loglines:
            # Assign different colors depending on the log level
            color = ''
            if line.find("Logger.DEBUG") == 0:
                color = clrs.RESET
            elif line.find("Logger.INFO") == 0:
                color = clrs.BLUE
            elif line.find("Logger.WARNING") == 0:
                color = clrs.WARNING
            elif line.find("Logger.ERROR") == 0:
                color = clrs.ERROR
            elif line.find("Logger.FATAL") == 0:
                color = clrs.ERROR

            # Only allow valid lines (containing "Logger.*" and passing filters).
            # Also clean out strings and print with the right color
            out = ""
            if self.lineCanBePrinted( line ):
                start = line.find( "." )+1
                print color + line[start:-1] + clrs.RESET




    # Infinite loop to watch log file
    # ===============================================================
    def follow(self, thefile):
        thefile.seek(0,2)
        while True:
             line = thefile.readline()
             if not line:
                 time.sleep(0.1)
                 continue
             yield line


    



    # ################### AUX FUNCTION BELOW HERE ###################
    # ===============================================================

    # Performs checks to decide if a line should be printd or not
    # ===============================================================
    def lineCanBePrinted( self, line ):
    	pass1 = self.isLoggerLine( line )
    	pass2 = self.passesWordFilter( line )
    	pass3 = self.passesLevelFilter( line )

        return pass1 and pass2 and pass3

    def isLoggerLine( self, line ):
        if line.find("Logger") == 0:
            return True
        return False

    def passesWordFilter( self, line ):
        if self.filterWord == '' or ( self.filterWord != '' and line.lower().find( self.filterWord ) >= 0 ):
            return True
        return False

    def passesLevelFilter( self, line ):
        level = self.getLevel( line )
        if level >= self.filterLevel:
            return True
        return False
    


    # Gets the log level of a line
    # ===============================================================
    def getLevel( self, line ):
        start = line.find( "." )+1
        clean = line[start:]
        #print "clean: " + clean
        end = clean.find(" (")
        #print str(start) + "---"+str(end)
        level = clean[:end]
        if level in self.levels:
            index = self.levels.index(level)
        else:
            index = 0
        return index


    



# Script entry point
if __name__ == "__main__":
    Flog(sys.argv[1:])
