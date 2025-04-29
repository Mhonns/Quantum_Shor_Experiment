# Quantum_Shor_Experiment Abstract
Just an experiment for getting the runtimes of prime factorization using brent-pollard factor on Classical Computer and Shor's Algorithm on Quantum and Classical computer (Hybrid solution). The result indicates that classical still beats the quantum computer for a small number in term of runtimes. 

# Procedure
0. Select the number to be factorized (15 and 21)
   0.1 Prepare the Classical compute machine: Mac M2
   0.2 Prepare the Quantum compute instance: IBMQ Sherbrooke
2. Run brent-pollard factor multiple times [Classical]
3. Run Shor's algorithm [Hybrid]
   2.1. Randomly select a in {a, N - 2} [Classical]
   2.2. Check Coprime of a, N [Classical]
   2.3. Define unitary U_N,a and get the period r [Quantum]
   2.4. Check if r is an odd [Classical]
   2.5. Find non trivial square root x = a^(r/2) mod N [Classcal]
   
5. Collect both result
6. Analyze the result
Please note for step 2.1 to remove the luck factor we instead looping x from a to N - 2

# Results
## Classical
#TODO Add result images
## Quantum
#TODO Add result images
