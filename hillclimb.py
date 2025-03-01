import math
import random
import time

#HillClimb Parameters
MAX_ITERATIONS = 100000
MAX_INVALID_COUNT = 1000
QUADGRAM_VALUE = 4224127912

'''
MAX_ITERATIONS = How many times do we want to keep trying to refine our key?
MAX_INVALID_COUNT = Prevents a key from getting stuck in hill climbing
QUADGRAM_VALUE = Just tracks what the total sum of quadgram in the original dict was - I couldn't be bothered to carry this around normally

100k iterations takes roughly ~2 minutes to run? Varies a lot however
'''

#Used to score each of the possible bruteforces by frequenc of quadgram appearence (Values are from a dict, so we pass that in as well)
def quadgram_score(txt, quadgrams):
    score = 0

    #We're getting each possible quadgram in a string
    for i in range(len(txt) - 3):
        substring = txt[i:i+4]
        if substring in quadgrams.keys():
            score += quadgrams[substring]
        else:
            score += math.log10(.01 / QUADGRAM_VALUE) #On the chance a quadgram is not in dict, we add this value (negative) to indicate a less likely candidate

    return score

#Applies a key to our current cipher
def decrypt(cipher, key):
    #Key is an alphabet of values
    substituted_string = ""

    #Assuming our cipher is uppercase here...
    for letter in cipher:
        substituted_string += key[ord(letter) - ord("A")] #Grab the unicode value -> Get the position in alphabet -> Find index in key
    
    return substituted_string

def hillclimb(cipher, start_key, quadgrams):
    best_key = None
    best_text = None
    best_score = -math.inf

    iterations = 0
    #Continue interating until we hit max, or we can't find a better key
    while iterations < MAX_ITERATIONS:
        key = start_key[:]
        invalid_count = 0
        #Prevents us from getting caught in a loop, where we can't improve our current key
        while invalid_count < MAX_INVALID_COUNT:
            original_score = quadgram_score(decrypt(cipher, key), quadgrams) #Grab the current score of our cipher

            #Swap two random keys
            x, y = random.randint(0, 25), random.randint(0, 25)
            key[x], key[y] = key[y], key[x]

            new_text = decrypt(cipher, key) #To prevent unescessary repeat calls
            new_score = quadgram_score(new_text, quadgrams)

            #If the new score beats the original, that's the new key we continue refining
            if new_score > original_score:
                #Save the best key overall and print it out
                if new_score > best_score:
                    best_score, best_text, best_key = new_score, new_text, key
                    print(f"Current Best (Iteration = {iterations})")
                    print(best_text)
                    print(best_key)
                    print(f"With a value of {best_score}")
                    best_time = time.time() 
                iterations += 1
            #If the new score isn't better, we can revert and try again
            else:
                key[x], key[y] = key[y], key[x]
                invalid_count += 1
    
    return best_time