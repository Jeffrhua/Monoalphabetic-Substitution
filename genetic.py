import math
import random
import hillclimb
import time

'''
A rewrite of Rishabh Bector's monoalphabetic decrypter implementation
https://github.com/rishabh-bector/enigma - Original repo source
'''

'''
Genetic algorithm parameters
'''
MAX_ITERATIONS = 500
MAX_POPULATION = 100
PURGE_PERCENTAGE = .33
MAX_IMPROVES = 20
MUTATION_PROBABILITY = 10

'''
MAX_ITERATIONS = How many times do we want to try to refine our answer? (Usually ~200 is enough to get to the pt where we refine with hillclimb, set to 500 on the off chance we get unlucky)
MAX_POPULATION = How large should each population we test be?
PURGE_PERCENTAGE = How much of that population do we want to terminate?
MAX_IMPROVES = How times do we create and try a new population before we start trying to hillclimb instead?
MUTATION_PROBABILITY = How likely is the newly created population likely to have simulated mutations? (Represented in %)

Default parameters = 500, 100, .33, 20, 10 respectively, I haven't tested different parameters too much however, so there's likely a better combination
'''

#Parse the english_quadgrams.txt file into a dictionary of normalized quadgram values     
def quadgram_parse():
    file = open("english_quadgrams.txt")

    quadgrams = {}
    #Parse txt file into a dictionary
    for line in file.read().split("\n"):
        split = line.split(" ")
        if split: #Don't wanna add a blank line
            quadgrams[split[0]] = int(split[1])
    
    #Now we want to convert each quadgram to a relative score (Log probability = log10(value / total_sum))
    total_sum = sum(quadgrams.values())
    for key in quadgrams.keys():
        quadgrams[key] = math.log10(quadgrams[key] / total_sum)
    
    return quadgrams

#Create n random different keys to test
def population_creation(n):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" #Used as a base to create a random key

    population = []
    for i in range(n):
        temp = list(alphabet)
        random.shuffle(temp)
        population.append(temp) #Append the randomized key
    
    return population

#Purge the bottom "PURGE_PERCENTAGE" of key values
def purge(population, cipher, quadgrams):
    final_population = []
    temp = []

    #Test out each key, and get the score of it
    for key in population:
        substituted_string = hillclimb.decrypt(cipher, key)
        score = hillclimb.quadgram_score(substituted_string, quadgrams)
        temp.append((key, score))
    
    temp.sort(key = lambda x: x[1]) #Sort based on the score value
    terminate = max(1, math.floor(len(population) * PURGE_PERCENTAGE)) #Terminate the bottom MAX_POPULATION_PERCENTAGE of values, default to 1 if 0

    for p in temp[terminate:]:
        final_population.append(p[0])
    
    #Return the final trimmed population, and the best score of that trimmed population
    return final_population, temp[-1][1]

#Replace missing values from the population -> Introduce possible mutations
def repopulate(population):
    final_population = []

    #Repopulate the purged population
    for i in range(MAX_POPULATION - len(population)):
        final = crossover(population[i], population[len(population) - i - 1])
        final_population.append(final)
    
    #Mutate the repopulated population and return
    mutation = mutate(final_population)
    mutation += population

    return mutation

#Combines two populations randomly, to (potentially) create a stronger candidate
def crossover(p1, p2):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" #Standard alphabet list to compare values
    crossover_pt = random.randint(0, 25) #Pick a index to combine at
    combined_population = p1[:crossover_pt] + p2[crossover_pt:]

    #We now need to refined this combined population by removing duplicates, adding missing values, etc...
    missing_letters = list(set(letters) - set(combined_population)) #Find the missing letters
    duplicates = list(set(x for x in combined_population if combined_population.count(x) > 1)) #Get a count of each letter, if > 1, we have duplicates

    #Replace the first instance of duplicate letters with missing letters
    for i, dup in enumerate(duplicates):
        combined_population[combined_population.index(dup)] = missing_letters[i]
    
    return combined_population

#Mutate a population randomly by swapping two elements based on MUTATION_PROBABILITY
def mutate(population):
    temp = population[:]

    for i in range(len(temp)):
        mutate = random.randint(0, 100) #Roll a die to check if a given key mutates
        if mutate <= MUTATION_PROBABILITY: #IF it does, we simply swap two random elements of a key
            x, y = random.randint(0, 25), random.randint(0, 25) 
            temp[i][x], temp[i][y] = temp[i][y], temp[i][x]
    
    return temp

#Start of our genetic algorithim -> Creates a list of potential key candidates we can further refine with hill climbing
def genetic_algorithm(cipher, quadgrams):
    best_score = -math.inf
    population = population_creation(MAX_POPULATION) #Create MAX_POPULATION random keys as our intial pool of key candidates
    iterations = 0 #Track when we want to stop refining
    stop = 0 #If we haven't found a better answer in MAX_IMPROVES, we start hillclimbing with our refined population

    #Currently, we continue iterating until we hit the max_iterations, or when we need to start refining with hillclimbing
    while iterations < MAX_ITERATIONS:
        purged, score = purge(population, cipher, quadgrams) #Returns the population that survived, and the best candidate score of that population

        if score > best_score:
            best_score = score
            stop = 0
            print(f"Current best score = {best_score} from key = {purged[-1]}")
        else:
            stop += 1

        population = repopulate(purged)
        iterations += 1

        #Once we stop improving, we hillclimb
        if stop > MAX_IMPROVES:
            best_key = max(population, key = lambda k: hillclimb.quadgram_score(hillclimb.decrypt(cipher, k), quadgrams))
            return hillclimb.hillclimb(hillclimb.decrypt(cipher, best_key), best_key, quadgrams) #We use the partically decrypted string as its a better restart point for the hillclimbing => Leads to more consistent answers
    
    #If we ever hit max iterations before finding the best possible candidate key refine with what we have
    if iterations > MAX_ITERATIONS:
        return hillclimb.hillclimb(hillclimb.decrypt(cipher, best_key), best_key, quadgrams)

def main():
    user = input("Enter cipher to solve: ")

    #Cleaning up input -> stripping whitespace & punctuation
    cipher = ""
    for char in user:
        if char.isalpha():
            cipher += char.upper()

    start = time.time()

    quadgrams = quadgram_parse() #Grab our quadgram values
    best_time = genetic_algorithm(cipher, quadgrams)
    end = time.time()

    print(f"Best answer found in {best_time - start}s")
    print(f"Program terminated in {end - start}s for {hillclimb.MAX_ITERATIONS} iterations")

main()