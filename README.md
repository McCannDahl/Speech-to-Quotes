# Speech-to-Quotes
Input a speech and this converts sections of the speech to quotes

## 1) Get the code on your computer
```
git clone https://github.com/McCannDahl/Speech-to-Quotes.git
git submodule init
git submodule update
```

## 2) Get the python modules
```
pip install typer
pip install nltk
```

## 3) Fill in input.txt with our speech

## 4) Run the program
```
python main.py auto
```

## 5) Try more options
To see a list of options
```
python main.py --help
```

### Flow
Input text document ->  
Parce into sentances ->  
Compare each sentance to each verse ->  
save quote options ->  
pick top options with threashold ->  
save new text document with quotes and references