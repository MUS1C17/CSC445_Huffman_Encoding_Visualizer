class HuffmanTableGenerator:
    '''This is a backend class for generating HuffmanTable'''

    def __init__(self):
        '''Constructor that initializes dictionary'''
        self.characterAndAmountDictionary = dict()

    def createDictionary(self, textInput):
        '''Method to create dectionary from the text box that was provided by user
        It generates a list of characters, then it checks if a character is in the dictionary.
        If it is, the number of it increases by one, if not then it is added to the dictionary with value 1'''
        
        textInputList = list(textInput)
        if len(textInput) == 0:
            print("No text was provided") #TODO: MAKE RETURN
        for character in textInputList:
            if character in self.characterAndAmountDictionary:
                self.characterAndAmountDictionary[character] = int(self.characterAndAmountDictionary.get(character)) + 1
            else:
                self.characterAndAmountDictionary.update({character : 1})
        print(self.characterAndAmountDictionary) #TODO: MAKE RETURN
        return self.characterAndAmountDictionary
    
    def getCharacterAndAmountDictionary(self):
        return self.characterAndAmountDictionary
    
    def getListOfCharacters(self):
        '''Returns Characters from dictionary in list form'''
        return list(dict.keys(self.getCharacterAndAmountDictionary()))
    
    def getListOfFrequencies(self):
        '''Returns list of frequencies for every character'''
        return list(dict.values(self.getCharacterAndAmountDictionary()))
    