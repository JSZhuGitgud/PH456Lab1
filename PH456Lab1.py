"""
PH456 Lab 1
"""
#Importing modules
import numpy as np
import random
import matplotlib.pyplot as plt

###############
#Task1
###############

#Declaring and seeding pseudo-random generators
rngPC1 = np.random.Generator(np.random.PCG64(10))
rngPC2 = np.random.Generator(np.random.PCG64(100))


rngMT1 = np.random.Generator(np.random.MT19937(10))
rngMT2 = np.random.Generator(np.random.MT19937(100))


#Declaring arrays of pseudo-random numbers of N points
N= 10000
numsPC1 = rngPC1.random(N)
numsPC2 = rngPC2.random(N)


numsMT1 = rngMT1.random(N)
numsMT2 = rngMT2.random(N)


#Setting up a figure of 4 histograms for the generated numbers
plt.figure(1)
fig, ((ax1, ax2),(ax3, ax4)) = plt.subplots(2, 2, sharex=True)
fig.suptitle('Histogram to test uniformity of generated numbers')

m = 100 #Declaring number of bins in the histogram

#Plotting and labelling histograms
ax1.set_ylabel("PCG64")
counts1, bins, bars = ax1.hist(numsPC1, bins = m)
counts2, bins, bars = ax2.hist(numsPC2, bins = m)

ax3.set_ylabel("MT19937")
counts3, bins, bars = ax3.hist(numsMT1, bins = m)
counts4, bins, bars = ax4.hist(numsMT2, bins = m)

ax3.set_xlabel("seed=10")
ax4.set_xlabel("seed=100")

plt.show()

E = N/m #Calculating the expectation value

# Setting up a for loop for a Chi-Squared test
counts = [counts1, counts2, counts3, counts4] #Declaring a counter array to later display the Chi-squared value of all 4 plots at once
Chi = [0,] * 4 #Declaring an array of four 0s

for i in range(4) :
    for x in counts[i]:
            Chi[i] += ((x-E)**2)/E #Assigning each Chi-squared value to the array 'Chi'
            
#Defining a function for testing correlation between the original set of values and a rotated set of values of the histograms 
def shift(x, shf):
    for i in range(0, shf):
        first = x[0];
        for j in range(0, len(x)-1):
            x[j] = x[j+1]
        x[len(x)-1]=first
    return x

#Declaring the new shifted arrays of the pseudo-random numbers, shifting them by 500 points, and maintaining a copy of the original array
numsPC1_ori = numsPC1.copy()
numsPC1_shf = shift(numsPC1, 500)
numsPC2_ori = numsPC2.copy()
numsPC2_shf = shift(numsPC2, 500)
numsMT1_ori = numsMT1.copy()
numsMT1_shf = shift(numsMT1, 500)
numsMT2_ori = numsMT2.copy()
numsMT2_shf = shift(numsMT2, 500)

#Plotting and labelling the shifted arrays of pseudo-random numbers against the corresponding original arrays
plt.figure(2)
plt.xlabel('PCG64 Generated values')
plt.ylabel('PCG64 Generated values (shifted by 500 points)')
plt.scatter(numsPC1_ori, numsPC1_shf, marker= 'x')
plt.show()

plt.figure(3)
plt.xlabel('PCG64 Generated values')
plt.ylabel('PCG64 Generated values (shifted by 500 points)')
plt.scatter(numsPC2_ori, numsPC2_shf, marker= 'x')
plt.show()


plt.figure(4)
plt.scatter(numsMT1_ori, numsMT1_shf, marker= 'x')
plt.show()

plt.figure(5)
plt.scatter(numsMT2_ori, numsMT2_shf, marker= 'x')
plt.show()


# Setting up a for loop for a correlation test
shift_number = np.linspace(0,10000, 1000, dtype=int) #Array used to set 1k shifts between value 0 and and value 10k of the pseudo-random numbers array
correlation = np.zeros(len(shift_number)) #Array of 0s of length 1k

for i in range (len(shift_number)):
    shift = shift_number[i]
    numsPC1_shf = np.append(numsPC1_ori[-shift:], numsPC1_ori[:-shift]) 
    correlation[i] = np.correlate(numsPC1_ori, numsPC1_shf)[0] #Calculating the correlation between the orginal array and the shifted ones

correlation /= max(correlation) #Normalising correlation values

#Plotting and labelling the correlation between the arrays against the number of positions shifted
plt.figure(6)
plt.xlabel('Number of positions shifted')
plt.ylabel('Correlation between original values and shifted ones')
plt.plot(shift_number, correlation)
plt.show()



###############
#Task2
###############

#Declaring number of particles in the box
total = 1000
left = total

#Declaring empty arrays and setting up a for loop to simulate partitioned box problem
left_arr = []
right_arr = []
for i in range(10000):
     l_ratio = (left/total) #Calculates the fraction of particles on the left half of the box
     ran_num = random.random() #Generates a random number according to the current system time
     #Setting up an if statement, increasing or decreasing the number of particles on the left depending on the value of the generated number
     if ran_num < l_ratio: 
         left = left - 1
     else:
         left = left + 1
     #Appending mirrored values to two arrays, of the number of particles on the left and the right respectively, after each particle moving
     left_arr = np.append(left_arr, left)
     right_arr = np.append(right_arr, total-left)

#Plotting and labelling the number of particles in each side of the box against the timestep of the particles moving
plt.figure(7)
plt.xlabel('Timestep')
plt.ylabel('Number of particles')
plt.axhline(y=500, color='r', linestyle='-') #Adding a horizontal line to display the point of equilibrium for the system
plt.plot(left_arr)
plt.plot(right_arr)
plt.legend(['Equilibrium at 500','Particles on the left', 'Particles on the right']) #Adding a legend to identify each line
plt.show()



###############
#Task3
###############

#Reseting the number of particles to 1000 in the left
total = 1000
left = total

#Simulating partitioned box problem again but using the PCG64 pseudo-random generator this time
left_arrPC = []
right_arrPC = []
for i in range(len(numsPC1)):
      l_ratio = (left/total) 
      if numsPC1[i] < l_ratio:
          left = left - 1
      else:
          left = left + 1
      left_arrPC = np.append(left_arrPC, left)
      right_arrPC = np.append(right_arrPC, total-left)

#Plotting the number of particles against the timestep
plt.figure(8)
plt.xlabel('Timestep')
plt.ylabel('Number of particles')
plt.axhline(y=500, color='r', linestyle='-')
plt.plot(left_arrPC)
plt.plot(right_arrPC)
plt.legend(['Equilibrium at 500','Particles on the left', 'Particles on the right'])
plt.show()

#Reseting the number of particles
total = 1000
left = total

#Simulating partitioned box problem using the MT19937 pseudo-random generator this time
left_arrMT = []
right_arrMT = []
for i in range(len(numsMT1)):
      l_ratio = (left/total) 
      if numsMT1[i] < l_ratio:
          left = left - 1
      else:
          left = left + 1
      left_arrMT = np.append(left_arrMT, left)
      right_arrMT = np.append(right_arrMT, total-left)

#Plotting the number of particles against the timestep
plt.figure(9)
plt.xlabel('Timestep')
plt.ylabel('Number of particles')
plt.axhline(y=500, color='r', linestyle='-')
plt.plot(left_arrMT)
plt.plot(right_arrMT)
plt.legend(['Equilibrium at 500','Particles on the left', 'Particles on the right'])
plt.show()



###############
#Task4
###############

#Reseting the number of particles
total = 1000
left = total

#Simulating partitioned box problem using the same two pseudo-random generators, 
#but this time the probability for particles to move from left to right is 75% and from right to left is 25%
left_arrPC75 = []
right_arrPC25 = []
for i in range(len(numsPC1)):
      l_ratio = (left/total) 
      if numsPC1[i] < l_ratio * 2: #Multiplying the fraction 'left/total' by 2 changes the probability
          left = left - 1
      else:
          left = left + 1
      left_arrPC75 = np.append(left_arrPC75, left)
      right_arrPC25 = np.append(right_arrPC25, total-left)

plt.figure(10)
plt.xlabel('Timestep')
plt.ylabel('Number of particles')
plt.axhline(y=750, color='green', linestyle='-')
plt.axhline(y=250, color='r', linestyle='-')
plt.plot(left_arrPC75)
plt.plot(right_arrPC25)
plt.legend(['Equilibrium at 750 for right-hand side','Equilibrium at 750 for left-hand side','Particles on the left', 'Particles on the right'])
plt.show()

total = 1000
left = total

left_arrMT75 = []
right_arrMT25 = []
for i in range(len(numsMT1)):
      l_ratio = (left/total) 
      if numsMT1[i] < l_ratio * 2:
          left = left - 1
      else:
          left = left + 1
      left_arrMT75 = np.append(left_arrMT75, left)
      right_arrMT25 = np.append(right_arrMT25, total-left)

plt.figure(11)
plt.xlabel('Timestep')
plt.ylabel('Number of particles')
plt.axhline(y=750, color='green', linestyle='-')
plt.axhline(y=250, color='r', linestyle='-')
plt.plot(left_arrMT75)
plt.plot(right_arrMT25)
plt.legend(['Equilibrium at 750 for right-hand side','Equilibrium at 750 for left-hand side','Particles on the left', 'Particles on the right'])
plt.show()



