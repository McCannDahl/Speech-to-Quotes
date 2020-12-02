#see https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/


import typer
import json
from os import path

app = typer.Typer()

# Program to measure the similarity between 
# two sentences using cosine similarity. 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
# sw contains the list of stopwords 
sw = stopwords.words('english') 

############input data###################
sources = [] # [{'name':name, 'references':[{'reference':reference},'quotes':[quote]]}]
totalNumSentances = 0

###BOM###
bom = None
with open('scriptures-json/flat/book-of-mormon-flat.json') as f:
  bom = json.load(f)
references = []
for verse in bom['verses']:
    quotes = []
    for sentence in verse['text'].split('.'):
        quotes.append(sentence)
        totalNumSentances += 1
    references.append({'reference':verse['reference'],'quotes':quotes})
sources.append({'name':'bom','references':references})
###DNC###
dnc = None
with open('scriptures-json/doctrine-and-covenants.json') as f:
  dnc = json.load(f)
references = []
for chapter in dnc['sections']:
    for verse in chapter['verses']:
        quotes = []
        for sentence in verse['text'].split('.'):
            quotes.append(sentence)
            totalNumSentances += 1
        references.append({'reference':verse['reference'],'quotes':quotes})
sources.append({'name':'dnc','references':references})
###pgp###
pgp = None
with open('scriptures-json/flat/pearl-of-great-price-flat.json') as f:
  pgp = json.load(f)
references = []
for verse in pgp['verses']:
    quotes = []
    for sentence in verse['text'].split('.'):
        quotes.append(sentence)
        totalNumSentances += 1
    references.append({'reference':verse['reference'],'quotes':quotes})
sources.append({'name':'pgp','references':references})
###bibleNT###
bibleNT = None
with open('scriptures-json/flat/new-testament-flat.json') as f:
    bibleNT = json.load(f)
references = []
for verse in bibleNT['verses']:
    quotes = []
    for sentence in verse['text'].split('.'):
        quotes.append(sentence)
        totalNumSentances += 1
    references.append({'reference':verse['reference'],'quotes':quotes})
sources.append({'name':'bibleNT','references':references})
###bibleOT###
bibleOT = None
with open('scriptures-json/flat/old-testament-flat.json') as f:
    bibleOT = json.load(f)
for verse in bibleOT['verses']:
    quotes = []
    for sentence in verse['text'].split('.'):
        quotes.append(sentence)
        totalNumSentances += 1
    references.append({'reference':verse['reference'],'quotes':quotes})
sources.append({'name':'bibleOT','references':references})

def getSimilarity(X,Y):
    # tokenization 
    X_list = word_tokenize(X) 
    Y_list = word_tokenize(Y) 
    l1 =[];l2 =[] 

    # remove stop words from the string 
    X_set = {w for w in X_list if not w in sw} 
    Y_set = {w for w in Y_list if not w in sw} 

    # form a set containing keywords of both strings 
    rvector = X_set.union(Y_set) 
    for w in rvector: 
        if w in X_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0

    # cosine formula 
    for i in range(len(rvector)): 
            c+= l1[i]*l2[i] 
    cosine = 0
    if float((sum(l1)*sum(l2))**0.5) != 0:
        cosine = c / float((sum(l1)*sum(l2))**0.5) 
    #print("similarity: ", cosine) 
    return cosine

def getQuotes(s, threshold): # return [{'quote':str,'pct':float,'reference':str}]
    returnData = []
    with typer.progressbar(length=totalNumSentances) as progress:
        for source in sources:
            for reference in source['references']:
                for sentence in reference['quotes']:
                    r = getSimilarity(s, sentence)
                    if r > threshold and s != '' and sentence != '':
                        #print(f"s = {s}, r = {r}, s = {sentence}")
                        returnData.append({
                            'quote': sentence,
                            'pct': r,
                            'reference': f"({reference['reference']})"
                        })
                    progress.update(1)
    typer.echo(f" I found {len(returnData)} quote(s) related to '{s}'")
    return returnData

def getInputFileContents(inputFileName):
    f = open(inputFileName, "r")
    inputdata = [] # [line][sentance] str
    for x in f:
        sentances = x.split('.')
        inputdata.append(sentances)
    f.close
    return inputdata

def getAllQuotes(inputdata,threshold):
    alldata = [] # [line][sentance] {'inputdata':str,'quotes':[{'quote':str,'pct':float,'reference':str}]}
    totalNumberOfSentancesToAnylize = 0
    numberOfSentancesToAnylized = 0
    for line in inputdata:
        for sentance in line:
            if sentance != '\n' and sentance != '':
                totalNumberOfSentancesToAnylize += 1
    for line in inputdata:
        newLine = []
        for sentance in line:
            newSentance = {'inputdata':sentance,'quotes':[]}
            if sentance != '\n' and sentance != '':
                numberOfSentancesToAnylized += 1
                typer.secho(f"Processing {numberOfSentancesToAnylized}/{totalNumberOfSentancesToAnylize}", fg=typer.colors.BRIGHT_GREEN)
                newSentance = {'inputdata':sentance,'quotes':getQuotes(sentance,threshold)}
            newLine.append(newSentance)
        alldata.append(newLine)
    return alldata


def saveReviewFile(reviewFileName,contents):
    f = open(reviewFileName, 'w+')
    for line in contents:
        json.dump(line, f)
        f.write('\n')
    f.close()

def saveOutputFile(outputFileName,contents):
    f = open(outputFileName, 'w+')
    for line in outputdata:
        newLine = '.'.join(line)
        f.write(newLine)
    f.close()

def getReviewFileContents(reviewFileName):
    f = open(reviewFileName, "r")
    alldata = [] 
    for x in f:
        alldata.append(json.loads(x))
    f.close
    return alldata


def sortQuotes(q):
    return q['pct']

def autoGetQutoes(inputFileName,reviewFileName,threshold):
    typer.echo(f"Hello! Lets turn your talk into quotes....")
    getQuotes = True
    if path.exists(reviewFileName):
        typer.echo(f"It looks like that review file already exists...")
        getQuotes = typer.confirm("Do you want to get the quotes again?")

    alldata = []

    if getQuotes:
        # 1) read file
        inputdata = getInputFileContents(inputFileName)

        # 2) get quotes
        alldata = getAllQuotes(inputdata,threshold)

        # 3) write review file
        saveReviewFile(reviewFileName,alldata)
    
    else:
        alldata = getReviewFileContents(reviewFileName)

    return alldata

@app.command()
def auto(inputFileName: str = 'input.txt', reviewFileName: str = 'review.txt',outputFileName: str = 'output.txt', threshold: float = 0.3):

    alldata = autoGetQutoes(inputFileName,reviewFileName,threshold)

    # auto pick quotes
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
                        maxNewSentance = q['quote'] + ' ' + q['reference']
                        maxQuotePct = q['pct']
                if maxNewSentance is not None:
                    newSentance = maxNewSentance
            newLine.append(newSentance)
        outputdata.append(newLine)

    # write file
    saveReviewFile(outputFileName,outputdata)


@app.command()
def manual(inputFileName: str = 'input.txt', reviewFileName: str = 'review.txt',outputFileName: str = 'output.txt', threshold: float = 0.3):

    alldata = autoGetQutoes(inputFileName,reviewFileName,threshold)

    # manual pick quotes
    outputdata = [] # [line][sentance] str
    for line in alldata:
        newLine = []
        for sentance in line:
            newSentance = sentance['inputdata']
            if len(sentance['quotes']) > 0:
                i = 0
                sentance['quotes'].sort(reverse=True, key=sortQuotes)
                for q in sentance['quotes']:
                    typer.echo(typer.style(str(i)+") ", fg=typer.colors.RED)+typer.style(str(round(q['pct']*100))+"% ", fg=typer.colors.GREEN)+typer.style(q['reference']+" ", fg=typer.colors.CYAN)+typer.style(q['quote'], fg=typer.colors.BRIGHT_BLACK))
                    i += 1
                selectedIndex = typer.prompt(typer.style("Which index (or -1)?", fg=typer.colors.WHITE, bold=True))
                if selectedIndex is not None and selectedIndex != '':
                    sI = int(selectedIndex)
                    if sI < len(sentance['quotes']) and sI >= 0:
                        q = sentance['quotes'][sI]
                        newSentance = q['quote'] + ' ' + q['reference']
            newLine.append(newSentance)
        outputdata.append(newLine)

    # write file
    saveReviewFile(outputFileName,outputdata)

if __name__ == "__main__":
    app()

