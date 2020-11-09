import typer

def getQuotes(s):
    return []

def main(inputFileName: str = 'input.txt',outputFileName: str = 'output.txt'):
    typer.echo(f"Hello {inputFileName}")
    # 1) read file
    f = open(inputFileName, "r")
    inputdata = []
    for x in f:
        sentances = x.split('.')
        inputdata.append(sentances)
    f.close
    # 3) get quotes
    alldata = [] # [line][sentance] {'inputdata':str,'quotes':[{'quote':str,'pct':float}]}
    for line in inputdata:
        newLine = []
        for sentance in line:
            newSentance = {'inputdata':sentance,'quotes':getQuotes(sentance)}
            newLine.append(newSentance)
        alldata.append(newLine)
    # 4) pick quotes
    outputdata = [] # [line][sentance] {'inputdata':str,'quote':str/None}
    for line in alldata:
        newLine = []
        for sentance in line:
            newSentance = {'inputdata':sentance,'quote':None}
            if len(sentance['quotes']) > 0:
                maxQuotePct = 0
                maxQuote = None
                for q in sentance['quotes']:
                    if q['pct'] > maxQuotePct:
                        maxQuote = q['quote']
                        maxQuotePct = q['pct']
                newSentance['quote'] = maxQuote
            newLine.append(newSentance)
        outputdata.append(newLine)


    # 2) write file
    f = open(outputFileName, 'w+')
    for line in outputdata:
        newLine = '.'.join(line['inputdata'])
        f.write(newLine)
    f.close()


if __name__ == "__main__":
    typer.run(main)