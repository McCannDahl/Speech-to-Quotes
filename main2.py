#see https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/


import typer
import json
from tabulate import tabulate

app = typer.Typer()

# Program to measure the similarity between 
# two sentences using cosine similarity. 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
# sw contains the list of stopwords 
sw = stopwords.words('english') 

bom = None
with open('scriptures-json/book-of-mormon.json') as f:
  bom = json.load(f)
totalNumSentances = 0
for book in bom['books']:
    for chapter in book['chapters']:
        for verse in chapter['verses']:
            for sentence in verse['text'].split('.'):
                totalNumSentances += 1

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
        for book in bom['books']:
            for chapter in book['chapters']:
                for verse in chapter['verses']:
                    for sentence in verse['text'].split('.'): 
                        r = getSimilarity(s, sentence)
                        if r > threshold and s != '' and sentence != '':
                            #print(f"s = {s}, r = {r}, s = {sentence}")
                            returnData.append({
                                'quote': sentence,
                                'pct': r,
                                'reference': f"({verse['reference']})"
                            })
                        progress.update(1)
    typer.echo(f" I found {len(returnData)} quote(s) related to '{s}'")
    return returnData

@app.command()
def auto(inputFileName: str = 'input.txt', reviewFileName: str = 'review.txt',outputFileName: str = 'output.txt', threshold: float = 0.3):
    typer.echo(f"Hello! Lets turn your talk into quotes....")

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
            newSentance = {'inputdata':sentance,'quotes':[]}
            if sentance != '\n' and sentance != '':
                newSentance = {'inputdata':sentance,'quotes':getQuotes(sentance,threshold)}
            newLine.append(newSentance)
        alldata.append(newLine)

    # 3) write file
    f = open(reviewFileName, 'w+')
    for line in alldata:
        json.dump(line, f)
        f.write('\n')
    f.close()

    # 4) pick quotes
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

    # 5) write file
    f = open(outputFileName, 'w+')
    for line in outputdata:
        newLine = '.'.join(line)
        f.write(newLine)
    f.close()


@app.command()
def review(reviewFileName: str = 'review.txt',outputFileName: str = 'output.txt'):
    typer.echo(f"Hello! Lets review your quotes....")

    # 1) read file
    f = open(reviewFileName, "r")
    alldata = [] 
    for x in f:
        alldata.append(json.loads(x))
    f.close

    # 2) pick quotes
    outputdata = [] # [line][sentance] str
    for line in alldata:
        newLine = []
        for sentance in line:
            newSentance = sentance['inputdata']
            if len(sentance['quotes']) > 0:
                i = 0
                tableData = []
                for q in sentance['quotes']:
                    tableData.append([i,q['reference'],round(q['pct']*100),q['quote']])
                    i += 1
                print(tabulate(tableData, headers=['Index', 'Reference', 'Match', 'Quote'], tablefmt='orgtbl'))
                selectedIndex = typer.prompt(typer.style("Which index (or -1)?", fg=typer.colors.GREEN, bold=True))
                if selectedIndex is not None and selectedIndex != '':
                    sI = int(selectedIndex)
                    if sI < len(sentance['quotes']) and sI >= 0:
                        q = sentance['quotes'][sI]
                        newSentance = q['quote'] + ' ' + q['reference']
            newLine.append(newSentance)
        outputdata.append(newLine)

    # 3) write file
    f = open(outputFileName, 'w+')
    for line in outputdata:
        newLine = '.'.join(line)
        f.write(newLine)
    f.close()

if __name__ == "__main__":
    app()

