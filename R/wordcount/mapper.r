#! /usr/bin/env Rscript

# documentation and commenting will be quite verbose I apologize in advance

input <- file("stdin", "r") # create our input stream object with parameters "stdin" for standard in and "r" for reading

# we now want to start reading from this input stream moreover we  want to keep reading as long as we have input

while(length(currentLine <- readLines(input, n = -1, warn = FALSE)) > 0){

    # next we want to split according the whitespace, moroever create a vector of this split
    # we will use the strsplit to split the current line according to our param split
    # when then take this and use unlist to take this character list and create a vector of it in words
    words <- unlist(strsplit(currentLine, split = " "))

    # now that we have this we want map each element of the vecotr to a <value , key> format for the reduce stage
    for (word in words){
        cat(word, 1, "\n")
    }

}

## TODO: just add regex expressions to the split parameter to accept other delims or use other functions

