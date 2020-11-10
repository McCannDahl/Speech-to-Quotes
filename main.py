import typer
import json
from fuzzywuzzy import fuzz 

bom = None
with open('scriptures-json/book-of-mormon.json') as f:
  bom = json.load(f)
totalNumSentances = 0
for book in bom['books']:
    for chapter in book['chapters']:
        for verse in chapter['verses']:
            for sentence in verse['text'].split('.'):
                totalNumSentances += 1


def getQuotes(s, threshold): # return [{'quote':str,'pct':float,'reference':str}]
    returnData = []
    with typer.progressbar(length=totalNumSentances) as progress:
        for book in bom['books']:
            for chapter in book['chapters']:
                for verse in chapter['verses']:
                    for sentence in verse['text'].split('.'):
                        # r = fuzz.token_set_ratio(s, sentence) 
                        r = fuzz.WRatio(s, sentence)
                        if r > threshold*100 and s != '' and sentence != '':
                            #print(f"s = {s}, r = {r}, s = {sentence}")
                            returnData.append({
                                'quote': sentence,
                                'pct': r,
                                'reference': f"({verse['reference']})"
                            })
                        progress.update(1)
    return returnData

def main(inputFileName: str = 'input.txt',outputFileName: str = 'output.txt', threshold: float = 0.8):
    typer.echo(f"Hello {inputFileName}")

    # 1) read file
    f = open(inputFileName, "r")
    inputdata = [] # [line][sentance] str
    for x in f:
        sentances = x.split('.')
        inputdata.append(sentances)
    f.close

    # 2) get quotes
    alldata = [] # [line][sentance] {'inputdata':str,'quotes':[{'quote':str,'pct':float,'reference':str}]}
    for line in inputdata:
        newLine = []
        for sentance in line:
            newSentance = {'inputdata':sentance,'quotes':getQuotes(sentance,threshold)}
            newLine.append(newSentance)
        alldata.append(newLine)

    # 3) pick quotes
    outputdata = [] # [line][sentance] str
    for line in alldata:
        newLine = []
        for sentance in line:
            newSentance = sentance['inputdata']
            if len(sentance['quotes']) > 0:
                maxQuotePct = 0
                maxNewSentance = None
                for q in sentance['quotes']:
                    if q['pct'] > maxQuotePct:
                        maxNewSentance = q['quote'] + q['reference']
                        maxQuotePct = q['pct']
                if maxNewSentance is not None:
                    newSentance = maxNewSentance
            newLine.append(newSentance)
        outputdata.append(newLine)

    # 4) write file
    f = open(outputFileName, 'w+')
    for line in outputdata:
        newLine = '.'.join(line)
        f.write(newLine)
    f.close()


if __name__ == "__main__":
    typer.run(main)