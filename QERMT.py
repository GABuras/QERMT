# Author: George Adler Buras

# from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib.ticker as mtick


# use tkinter for gui data collection?
# import tkinter

# If I want to scrape excel doc:
# import pandas as pd
# df = pd.read_excel('Response 1.xlsx', sheet_name='Submission')
# print(df.loc[0])


# TODO Create GUI for data collection





# Index:
    # 0: Risk ID
    # 1: Risk Name
    # 2: Type of Vote Manipulation (Adding, Subtracting, or Changing)
    # 3: Probability of Manipulation Over 1 Election Cycle
    # 4: Lower Bound of Impact (95% Chance Value Is Higher)
    # 5: Upper Bound of Impact (95% Chance Value Is Lower)
    # 6: Total Cost of Controls
    # 7: Control Effectiveness
header = ["Risk ID", "Risk Name", "Type of Vote Manipulation (Adding, Subtracting, or Changing)", "Probability of Manipulation Over 1 Election Cycle", "Lower Bound of Impact (95% Chance Value Is Higher)", "Upper Bound of Impact (95% Chance Value Is Lower)", "Total Cost of Controls", "Control Effectiveness"]


# Saving or loading data?
loadingData = True

if not loadingData:
    # Saving data
    # TODO encrypt saved data
    # TODO fill data from GUI
    electionID = "sample"
    data = []
    # print(tabulate(data, headers=header, tablefmt="grid"))
    votesCast = 0
    marginOfVictoryVotes = 0

    with open(electionID + "Data.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)

    metaHeader = ["Election ID", "Number of Votes Cast", "Margin of Victory"]
    metaData = [electionID, votesCast, marginOfVictoryVotes]
    with open(electionID + "Meta.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(metaHeader)
        writer.writerow(metaData)

if loadingData:
    # Loading saved data
    # TODO decrypt saved data
    with open("sampleData.csv", 'r') as csvfile:
        contents = csv.reader(csvfile)
        contents = list(contents)
        # header = contents[0] # unnecessary/redundant
        # print(header) 
        data = contents[1:]
        # print(data)
        # correct data formatting
        for risk in data:
            risk[0] = int(risk[0])
            risk[3] = float(risk[3])
            risk[4] = int(risk[4])
            risk[5] = int(risk[5])
            risk[6] = int(risk[6])
            risk[7] = float(risk[7])
        # print(data)

    with open("sampleMeta.csv", 'r') as csvfile:
        contents = csv.reader(csvfile)
        contents = list(contents)
        metaHeader = contents[0]
        # print(metaHeader)
        metaData = contents[1]
        # print(metaData)
        electionID = metaData[0]
        # print(electionID)
        votesCast = int(metaData[1])
        # print(votesCast)
        marginOfVictoryVotes = int(metaData[2])
        # print(marginOfVictoryVotes)


# Doing the math

# TODO do I want to seed random numbers?
# tie seed to simulation number?
rng = np.random.default_rng()

totalImpacts = []

# Iterate through 10k simulations
numberOfSimulations = 10000
for s in range(numberOfSimulations):

    totalImpact = 0

    # For each risk
    for i in range(len(data)):
        # print(data[i][3])
        # Did the risk occur in this simulation?
        if rng.random() < data[i][3]:
            # The risk occured. What is its impact?

            # mean = ((ln(UB)+ln(LB))/2)
            mean = ((np.log(data[i][5]) + np.log(data[i][4])) / 2)
            # print(mean)

            # standardDeviataion = (ln(UB)‐ ln(LB))/3.29)
            standardDeviataion = ((np.log(data[i][5]) - np.log(data[i][4])) / 3.29)
            # print(standardDeviataion)

            riskImpact = rng.lognormal(mean, standardDeviataion)
            # print("Impact: " + str(riskImpact))

            # Add impact to total for this simulation
            totalImpact += riskImpact

    # print("Total Impact: " + str(totalImpact))

    # Track total impact for each simulation
    totalImpacts.append(totalImpact)

# print(totalImpacts)




# Draw loss exceedance curve
# TODO make x axis exponential

marginOfVictoryPercentage = marginOfVictoryVotes / votesCast
xValues = np.linspace(0, marginOfVictoryPercentage + 0.01, 151)
# print(xValues)

yValues = []

for x in xValues:
    yValue = 0
    for t in totalImpacts:
        if t > (x * votesCast): 
            yValue += 1
    yValues.append(yValue/numberOfSimulations)

# print(yValues)

marginOfVictoryY = 0
for t in totalImpacts:
    if t > marginOfVictoryVotes:
        marginOfVictoryY += 1
marginOfVictoryY = marginOfVictoryY/numberOfSimulations



plt.title("Loss Exceedance Curve")
plt.xlabel("Margin of Manipulation (Manipulated Votes / Counted Votes)")
plt.ylabel("Chance of Margin of Manipulation or Greator")
plt.plot(xValues, yValues)

ax = plt.gca()
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

plt.grid(True, which='both', linestyle='--', color='gray', linewidth=0.5)
plt.tight_layout()
plt.ylim(0, max(yValues) + 0.01)
plt.xlim(min(xValues), max(xValues))

# Label Margin of Victory Percentage
ax.annotate("Margin of Victory\n(%.4f%%, %.4f%%)"%(marginOfVictoryPercentage*100, marginOfVictoryY*100), xy=(marginOfVictoryPercentage, marginOfVictoryY), xytext=(marginOfVictoryPercentage-0.005, marginOfVictoryY+0.15), arrowprops=dict(facecolor = 'red', shrink = 0.05),)

plt.show()



# TODO Test with sample data from book






# mean = ((ln(UB)+ln(LB))/2)
# mean = ((np.log(data[0][5]) + np.log(data[0][4])) / 2)
# print(mean)

# # standardDeviataion = (ln(UB)‐ ln(LB))/3.29)
# standardDeviataion = ((np.log(data[0][5]) - np.log(data[0][4])) / 3.29)
# print(standardDeviataion)

# points = rng.lognormal(mean, standardDeviataion, 10000)
# # print(points)

# lower = 0
# higher = 0

# for p in points:
#     if p < data[0][4]:
#         lower+=1
#     if p > data[0][5]:
#         higher +=1

# print(lower/1000)
# print(higher/1000)


# import matplotlib.pyplot as plt
# count, bins, _ = plt.hist(points, 10000, density=True, align='mid')

# x = np.linspace(min(bins), max(bins), 10000)
# # probability density function of lognormal distribution
# pdf = (np.exp(-(np.log(x) - mean)**2 / (2 * standardDeviataion**2))
#        / (x * standardDeviataion * np.sqrt(2 * np.pi)))

# plt.plot(x, pdf, linewidth=0.5, color='r')
# plt.axis('tight')
# plt.show()