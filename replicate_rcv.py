"""
Maine Congressional District 2 (2018) Ranked Choice Voting Replication by Nathan Tefft, Ph.D.

To run this replication script, include the Excel files containing the counted ballots in the same directory
    as the script, and set the working directory there.

This python script improves on and generalizes the notebook I created on 11/29/2018. Improvements include:
    1) The ability to run ranked-choice voting runoffs automatically for future votes 
    2) Although irrelevant to the final results, I changed the ballot labels to "exhausted" instead of
        "invalidated" after two consecutive skipped rankings, or when all remaining choices are reported as
        "undervote".
"""

import numpy
import pandas

ballots = pandas.DataFrame()
for datafilename in ['Nov18CVRExportFINAL1.xlsx','Nov18CVRExportFINAL2.xlsx','Nov18CVRExportFINAL3.xlsx','RepCD2-8final.xlsx']:
    ballots = ballots.append(pandas.read_excel(datafilename).rename(index=str, columns={"Rep. to Congress 1st Choice District 2": "choice1", "Rep. to Congress 2nd Choice District 2": "choice2", "Rep. to Congress 3rd Choice District 2": "choice3", "Rep. to Congress 4th Choice District 2": "choice4", "Rep. to Congress 5th Choice District 2": "choice5"}), sort=True)
for datafilename in ['UOCAVA-FINALRepCD2.xlsx','UOCAVA-AUX-CVRRepCD2.xlsx','UOCAVA2CVRRepCD2.xlsx','AUXCVRProofedCVR95RepCD2.xlsx']:
    ballots = ballots.append(pandas.read_excel(datafilename).rename(index=str, columns={"Rep. to Congress District 2 1st Choice": "choice1", "Rep. to Congress District 2 2nd Choice": "choice2", "Rep. to Congress District 2 3rd Choice": "choice3", "Rep. to Congress District 2 4th Choice": "choice4", "Rep. to Congress District 2 5th Choice": "choice5"}), sort=True)

choices = pandas.DataFrame()
for i in range(0,5):
    choices[i] = ballots['choice' + str(i+1)].str.replace("\(5931\)","").str.replace("\(5471\)","").str.strip()

# work backwards from last choices to 2nd choice and mark as exhausted until finding an identified choice or a double undervote
for i in range(len(choices.columns)-1,0,-1):
    if (i==(len(choices.columns)-1)):
        choices[i] = numpy.where(choices[i].str.contains('undervote'),'exhausted',choices[i])
    else:
        choices[i] = numpy.where(choices[i+1].str.contains('exhausted') & choices[i].str.contains('undervote'),'exhausted', choices[i])        

#If you skip two levels of rankings, your votes in the subsequent levels of rankings will not count.    
for i in range(2,len(choices.columns)):
    choices[i] = numpy.where(choices.iloc[:,i-2].str.contains('undervote') & choices[i-1].str.contains('undervote'),'exhausted',choices[i])

#Invalidate all choices that follow an overvote or an invalidation
for i in range(1,len(choices.columns)):
    choices[i] = numpy.where(choices[i-1].str.contains('overvote|invalidated'),'invalidated',choices[i])

runoffs = pandas.DataFrame()
n=0
eliminated=['INITIALIZE_ELIMINATED_CANDIDATE_LIST']
finished = False
while not finished:
    print('\n********\nBEGINNING RUNOFF ' + str(n))
    
    if n==0:    
        runoffs[0] = choices[0]
    else:
        runoffs[n] = runoffs[n-1]
    
    for i in range(0,len(choices.columns)-1):
        runoffs[n] = numpy.where(runoffs[n].str.contains('|'.join(eliminated)) | runoffs[n].str.contains('undervote'),choices[i+1],runoffs[n])
    runoffs[n] = numpy.where(runoffs[n].str.contains('|'.join(eliminated)),'exhausted',runoffs[n])    
            
    print('\n***Tabulation of ballot statuses')
    tally = runoffs[n].value_counts()
    print(tally)
    print('\n***Percents of votes among continuing candidates')
    percents = 100*tally[~tally.index.str.contains('exhausted|overvote|undervote|invalidated')]/tally[~tally.index.str.contains('exhausted|overvote|undervote|invalidated')].sum()
    print(percents)

#In the final round, when only 2 continuing candidates remain, the candidate with the most votes in that round is the winning candidate.    
    finished = percents.count() == 2
    
    if not finished:    
        eliminated.append(''.join(tally[~tally.index.str.contains('exhausted|overvote|undervote|invalidated')][[-1]].index.format()))
        n+=1
    else:
        print('\n********\n' + tally.index[0].format() + ' is the winner.')


