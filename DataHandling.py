# Author: George Adler Buras

import numpy as np
import csv
import os

# TODO Better error handling (especially for files)

# saves data to csv files
def saveData(electionID: str, dataProfile):
    # TODO encrypt saved data

    votesCounted = dataProfile[0]
    marginOfVictoryVotes = dataProfile[1]
    data =  dataProfile[2]

    # Index:
    # 0: Risk ID
    # 1: Risk Name
    # 2: Type of Vote Manipulation (Adding, Subtracting, or Changing)
    # 3: Probability of Manipulation Over 1 Election Cycle
    # 4: Lower Bound of Impact (95% Chance Value Is Higher)
    # 5: Upper Bound of Impact (95% Chance Value Is Lower)
    # 6: Total Cost of Controls
    # 7: Control Effectiveness
    dataHeader = ["Risk ID", "Risk Name", "Type of Vote Manipulation (Adding, Subtracting, or Changing)", "Probability of Manipulation Over 1 Election Cycle", "Lower Bound of Impact (95% Chance Value Is Higher)", "Upper Bound of Impact (95% Chance Value Is Lower)", "Total Cost of Controls", "Control Effectiveness"]
    with open(f"./data/{electionID}Data.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(dataHeader)
        writer.writerows(data)

    metaHeader = ["Election ID", "Number of Votes Counted", "Margin of Victory"]
    metaData = [electionID, votesCounted, marginOfVictoryVotes]
    with open(f"./data/{electionID}Meta.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(metaHeader)
        writer.writerow(metaData)

    # TODO there is probably a better way to do this?
    with open(f"./data/savedElectionIDs.csv", "r+", newline='') as csvfile:
        savedElectionIDs = csv.reader(csvfile)
        alreadyExists = False
        for row in savedElectionIDs:
            if electionID in row:
                alreadyExists = True
        
        # print(alreadyExists)
        
        if not alreadyExists:
            writer = csv.writer(csvfile)
            writer.writerow([electionID])


# Loads saved data from csv files, returns dataProfile
def loadData(electionID: str):
    # TODO decrypt saved data
    with open(f"./data/{electionID}Data.csv", 'r') as csvfile:
        contents = list(csv.reader(csvfile))
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

    with open(f"./data/{electionID}Meta.csv", 'r') as csvfile:
        contents = list(csv.reader(csvfile))
        # metaHeader = contents[0] 
        # print(metaHeader)
        metaData = contents[1]
        # print(metaData)
        # electionID = metaData[0] 
        # print(electionID)
        votesCounted = int(metaData[1])
        # print(votesCounted)
        marginOfVictoryVotes = int(metaData[2])
        # print(marginOfVictoryVotes)
    
    return [votesCounted, marginOfVictoryVotes, data]

# Deletes electionID from savedElectionIDs.csv and deletes the corresponding data and meta csv files
def deleteData(electionID: str):
    # remove electionID from savedElectionIDs
    updatedList = []
    with open(f"./data/savedElectionIDs.csv", "r", newline='') as csvfile:
        savedElectionIDs = csv.reader(csvfile)
        for row in savedElectionIDs:
            if electionID not in row:
                updatedList.append(row)

    with open(f"./data/savedElectionIDs.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(updatedList)
        
    # delete electionID + Data.csv
    if os.path.exists(f"./data/{electionID}Data.csv"):
        os.remove(f"./data/{electionID}Data.csv")
    else:
        print(f"{electionID}Data.csv does not exist")
    
    # delete electionID + Meta.csv
    if os.path.exists(f"./data/{electionID}Meta.csv"):
        os.remove(f"./data/{electionID}Meta.csv")
    else:
        print(f"{electionID}Meta.csv does not exist")


# dataProfile is [votesCounted, marginOfVictoryVotes, data], same as returned by loadData(...)
def analyzeData(dataProfile):

    votesCounted = dataProfile[0]
    marginOfVictoryVotes = dataProfile[1]
    data =  dataProfile[2]

    # TODO do I want to seed random numbers?
    # tie seed to simulation number?
    rng = np.random.default_rng()

    # List of total impact for each simulation
    simulatedImpacts = []

    # List of total impact for each risk
    riskImpacts = [0] * len(data)

    # Iterate through 10k simulations, as recomended by book. Increasing gives more consistent results
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

                # TODO Track the impact of each risk
                riskImpacts[i] += riskImpact

        # print("Total Impact: " + str(totalImpact))

        # Track total impact for each simulation
        simulatedImpacts.append(totalImpact)

    # print(simulatedImpacts)
    # print(riskImpacts)


    # Calculate loss exceedance curve

    marginOfVictoryPercentage = marginOfVictoryVotes / votesCounted
    xValues = np.linspace(0, marginOfVictoryPercentage * 1.5, 151)
    # print(xValues)

    yValues = []

    for x in xValues:
        yValue = 0
        for t in simulatedImpacts:
            if t > (x * votesCounted): 
                yValue += 1
        yValues.append(yValue/numberOfSimulations)

    # print(yValues)

    marginOfVictoryY = 0
    for t in simulatedImpacts:
        if t > marginOfVictoryVotes:
            marginOfVictoryY += 1
    marginOfVictoryY = marginOfVictoryY/numberOfSimulations

    # Calculate Control Ranking
    avgRiskImpacts = []
    for riskImpact in riskImpacts:
        avgRiskImpacts.append(riskImpact/numberOfSimulations)

    # print(avgRiskImpacts)

    # Average number of manipulated votes from a particular risk mitigated per dollar spent on implementing all controls for that risk
    mitigatedManipulatedVotePerControlDollar = []
    for risk in range(len(avgRiskImpacts)):
        # (avgRiskImpact * controlEffectiveness) / totalControlCost
        mitigatedManipulatedVotePerControlDollar.append((avgRiskImpacts[risk] * data[risk][7]) / data[risk][6])

    # print(mitigatedManipulatedVotePerControlDollar)

    # Average control cost of mitigating a single manipulated vote
    controlCostPerMitigatedManipulatedVote = []
    for risk in range(len(avgRiskImpacts)):
        # totalControlCost / (avgRiskImpact * controlEffectiveness)
        controlCostPerMitigatedManipulatedVote.append(data[risk][6] / (avgRiskImpacts[risk] * data[risk][7]))

    # print(controlCostPerMitigatedManipulatedVote)

    # Control Ranking to be displayed
    controlRanking = []
    for risk in range(len(data)):
        # [Risk ID, Risk Name, Total Cost of Controls, Control Effectiveness, votes/dollar, dollars/vote]
        controlRanking.append([data[risk][0], data[risk][1], data[risk][6], data[risk][7], mitigatedManipulatedVotePerControlDollar[risk], controlCostPerMitigatedManipulatedVote[risk]])

    controlRanking = sorted(controlRanking, key=lambda x: x[5])

    # print(controlRanking)

    return [xValues, yValues, marginOfVictoryPercentage, marginOfVictoryY, controlRanking]

    # TODO Test with sample data from book

# TODO Doublecheck everything for spelling

if __name__ == '__main__':
    # analyzeData(loadData("sample"))

    # saveData("sample", votesCounted, marginOfVictoryVotes, data)

    # deleteData("sample2")

    pass