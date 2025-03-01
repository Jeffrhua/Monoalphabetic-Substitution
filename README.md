# Monoalphabetic-Substitution
A monoalphabetic substitution decrypter that utilizes genetic algorithims

This code follows the original implementation from Rishabh Bector's "Enigma" decrypter found here:  
https://github.com/rishabh-bector/enigma  
with the main purpose of revamping portions of the code and allowing for different parameters to be easily tested.

**Genetic Algorithm Parameters:**  
MAX_ITERATIONS = How many times do we want to try to refine our answer? (Usually ~200 is enough to get to the pt where we refine with hillclimb)
MAX_POPULATION = How large should each population we test be?
MAX_POPULATION_PERCENTAGE = How much of that population do we want to terminate?
MAX_IMPROVES = How times do we create and try a new population before we start trying to hillclimb instead?
MUTATION_PROBABILITY = How likely is the newly created population likely to have simulated mutations? (Represented in %)

**Hillclimbing Algorithm Parameters:**  
MAX_ITERATIONS = How many times do we want to keep trying to refine our key?
MAX_INVALID_COUNT = Prevents a key from getting stuck in hill climbing
QUADGRAM_VALUE = Just tracks what the total sum of quadgram in the original dict was - I couldn't be bothered to carry this around normally so I hardcoded it as a const

I haven't messed around with these parameters too much, so there's likely a better combination that what I have as the default.

To run:
- Boot up "genetic.py" and input any string (Which will be stripped of all punctuation and non alpha characters)
- Default iterations for hillclimb are 100k iterations, which will be roughly ~2mins to run
