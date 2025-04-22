from queue import PriorityQueue
from BinaryNode import *
class HuffmanTableGenerator:
    '''This is a backend class for generating HuffmanTable'''

    def __init__(self):
        '''Constructor that initializes dictionary'''
        self.characterAndFrequencyDictionary = dict()

    def createDictionary(self, textInput):
        '''Method to create dectionary from the text box that was provided by user
        It generates a list of characters, then it checks if a character is in the dictionary.
        If it is, the number of it increases by one, if not then it is added to the dictionary with value 1'''
        
        textInputList = list(textInput)
        if len(textInput) == 0:
            print("No text was provided") #TODO: Remove
        for character in textInputList:
            if character in self.characterAndFrequencyDictionary:
                self.characterAndFrequencyDictionary[character] = int(self.characterAndFrequencyDictionary.get(character)) + 1
            else:
                self.characterAndFrequencyDictionary.update({character : 1})
        print(self.characterAndFrequencyDictionary) #TODO: Remove
        return self.characterAndFrequencyDictionary
    
    def getCharacterAndFrequencyDictionary(self):
        return self.characterAndFrequencyDictionary
    
    
    def getListOfCharacters(self):
        '''Returns Characters from dictionary in list form'''
        return list(dict.keys(self.getCharacterAndFrequencyDictionary()))
    
    def getListOfFrequencies(self):
        '''Returns list of frequencies for every character'''
        return list(dict.values(self.getCharacterAndFrequencyDictionary()))
    
    def createPriorityQueue(self, characterAndFrequencyDictionary: dict):
        '''This method is to create original priority queue having dictionary as input parameter'''
        priorityQueue = PriorityQueue(0) #0 means infinete length 
        for character, frequency in characterAndFrequencyDictionary.items():
            #priorityQueue.put((frequency, character))
            priorityQueue.put((frequency, BinaryNode(character)))
        return priorityQueue

    def updatePriorityQueue(self, priorityQueue: PriorityQueue) -> BinaryNode:
        '''This method is using recursion to update priority queue.
        It removes two elements with lowest frequencies from the queue and
        Creates a node of them. Then, the node gets addded back to the priority queue.
        The proccess repeats until queue has one element which will be the root node
        of a tree'''
        if priorityQueue.qsize() == 1:
            frequency, root = priorityQueue.get()
            return root
        else:
            #Get two characters with smallest frequencies
            #frequencyOne, characterOne = priorityQueue.get()
            #frequencyTwo, characterTwo = priorityQueue.get()

            frequencyOne, nodeOne = priorityQueue.get()
            frequencyTwo, nodeTwo = priorityQueue.get()


            #Create new node with frequency sum of two smallest and string called "Node"
            #node = BinaryNode((int(frequencyOne) + int(frequencyTwo), "Node"))
            #Set children of the node to be rarest characters from priority queue
            #node.setRight((frequencyOne, characterOne))
            #node.setLeft((frequencyTwo, characterTwo))

            #Create combined node
            combined = BinaryNode("Node")
            combined.frequency = frequencyOne + frequencyTwo
            combined.setLeft(nodeOne)
            combined.setRight(nodeTwo)

            #update priority queue by adding new element with sum of two frequencies and node
            #priorityQueue.put((int(frequencyOne) + int(frequencyTwo), "Node"))
            priorityQueue.put((combined.frequency, combined))
            
            print("------------------------------------------------------")
            print(priorityQueue.queue)
            print()
            print(f"nodeOne: {nodeOne}")
            print(f"NodeTwo: {nodeTwo}")
            print(f"node: {combined}")
            print("------------------------------------------------------")

            #Call recursion
            return self.updatePriorityQueue(priorityQueue)

def main():
    myHTG = HuffmanTableGenerator()
    myDictionary = myHTG.createDictionary("Hello World")
    myPriorityQueue = myHTG.createPriorityQueue(myDictionary)
    finalQueue = myHTG.updatePriorityQueue(myPriorityQueue)
    

if __name__ == "__main__":
    main()