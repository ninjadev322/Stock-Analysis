#-----------------------------------------------------------------------
# dataScraping.py
# Description:
# Author: André Luiz Queiroz Costa
# Date: 03/02/2020
# Version: 1.0
#-----------------------------------------------------------------------

#The objective of this code is to retrieve all the necessary information that we need by scraping different
# webpages, so that we can later commence a full stock analysis with this info.

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
from typing import List
from urllib.request import urlopen, Request
import re
#import lxml

def fundamentalInfoFVZ(soup) -> float:
    #We inspect the webpage to finde the html tags of the pbjects that we want
    #Transforms the html to a pandas dataframe
    fundamentals = pd.read_html(str(soup), attrs={'class': 'snapshot-table2'}) #Can only do this if class type is a table 
    PE = fundamentals[0][3][0] # Price to earnings ratio
    if PE == '-':
        PE = 0
    PEG = fundamentals[0][3][2] # Price to earnings growth ratio
    if PEG == '-':
        PEG = 0
    PS = fundamentals[0][3][3] # Price to sales ratio
    if PS == '-':
        PS = 0
    PB = fundamentals[0][3][4] # Price to book value ratio
    if PB == '-':
        PB = 0
    DebtEquity = fundamentals[0][3][9] # Debt to equity ratio
    if DebtEquity == '-':
        DebtEquity = 0
    Recom = fundamentals[0][1][11] # Analysts recomendations
    if Recom == '-':
        Recom = 0
    MarketCap = fundamentals[0][1][1] #Number of shares times the the current price of each share
    if MarketCap == '-':
        MarketCap = 0
    else:    
        MarketCap = float(MarketCap[0:-1]) #When scraped comes with a B or M at the end we tranform it into number 
        MarketCap = MarketCap * 1000000000 #The value is given to use in billions so we transform it
    InsiderTrans = fundamentals[0][7][1] #The percentage of recent movements by insiders in the company
    if InsiderTrans == '-':
        InsiderTrans = 0
    else:    
        InsiderTrans = InsiderTrans[0:-1]    
    InstitutionTrans = fundamentals[0][7][3] #The percentage of recent mvoements made my hedgefunds and institutions
    if InstitutionTrans == '-':
        InstitutionTrans = 0
    else:    
        InstitutionTrans = InstitutionTrans[0:-1]
    ROA = fundamentals[0][7][4] #Return on assets
    if ROA == '-':
        ROA = 0
    else:    
        ROA = ROA[0:-1]   
    ROE = fundamentals[0][7][5] #Return on equity
    if ROE == '-':
        ROE = 0
    else:    
        ROE = ROE[0:-1]       
    AvgVolume = fundamentals[0][9][10] #The amount of shares bought and sold in a single trading period
    if AvgVolume == '-':
        AvgVolume = 0
    else:
        if AvgVolume[-1] == 'B':
            AvgVolume = float(AvgVolume[0:-1]) * 1000000000
        elif AvgVolume[-1] == 'M':
            AvgVolume = float(AvgVolume[0:-1]) * 1000000
        elif AvgVolume[-1] == 'K':
                AvgVolume = float(AvgVolume[0:-1]) * 1000
    Price = fundamentals[0][11][10] #price per share
    if Price == '-':
        Price = 0  
    LastChange = fundamentals[0][11][11] #The price percentage change in the last trading day
    if LastChange == '-':
        LastChange = 0
    else:
        LastChange = LastChange[0:-1]    
    PerfWeek = fundamentals[0][11][0] #The price percentage change in the last week
    if PerfWeek == '-':
        PerfWeek = 0
    else:
        PerfWeek = PerfWeek[0:-1]    
    PerfMonth = fundamentals[0][11][1] #The price percentage change in the last month
    if PerfMonth == '-':
        PerfMonth = 0
    else:
        PerfMonth = PerfMonth[0:-1]    
    PerfYear = fundamentals[0][11][4] #The price percentage change in the last year
    if PerfYear == '-':
        PerfYear = 0
    else:
        PerfYear = PerfYear[0:-1]    
    YearHighPercent = fundamentals[0][9][6] #The percent difference from its 52 week high
    if YearHighPercent == '-':
        YearHighPercent = 0
    else:
        YearHighPercent = YearHighPercent[0:-1]   
    EPSNextY = fundamentals[0][5][4] #Earnings per share growth for next year 
    if EPSNextY == '-':
        EPSNextY = 0
    else:    
        EPSNextY = EPSNextY[0:-1]  
    EPSNext5Y = fundamentals[0][5][5] #Earnings per share growth for next 5 years 
    if EPSNext5Y == '-':
        EPSNext5Y = 0
    else:    
        EPSNext5Y = EPSNext5Y[0:-1]                 


    return PE, PEG, PS, PB, MarketCap, DebtEquity, Recom, InsiderTrans, InstitutionTrans, ROA, ROE, AvgVolume, Price, LastChange, PerfWeek, PerfMonth, PerfYear, YearHighPercent, EPSNextY, EPSNext5Y

def IncomeStatementMW(soup) -> float:
    #We inspect the webpage to finde the html tags of the objects that we want
    #Transform the html to a pandas dataframe
    IncomeStatement = pd.read_html(str(soup), attrs={'class': 'table table--overflow align--right'}) #Can only do this if class type is a table 
    IncomeStatement = IncomeStatement[0] #Only getting the table since there are more objects with the same class
    IncomeStatement.columns = pd.RangeIndex(0, len(IncomeStatement.columns)) #Indexing the columns as numbers so that the differences in the name of columns wont matter
                                                                              #There is no defined nuber of columns so we set it to len
    
    #We add all the columns except the first which is the title and the last which is Nan
    RevenuePast5 = []
    for i in range(1, len(IncomeStatement.columns) - 1):
        RevenuePast5 += [IncomeStatement[i][0]]    
    #We must change the values from billions and millions to full numbers
    for i in range(len(RevenuePast5)):
        if RevenuePast5[i][-1] == 'B':
            RevenuePast5[i] = float(RevenuePast5[i][0:-1]) * 1000000000
        elif RevenuePast5[i][-1] == 'M':
            RevenuePast5[i] = float(RevenuePast5[i][0:-1]) * 1000000 
        elif RevenuePast5[-1] == 'K':
                RevenuePast5 = float(RevenuePast5[0:-1]) * 1000    
        elif RevenuePast5[i] == '-':
            RevenuePast5.remove(RevenuePast5[i])             

    #We take the growth year to year and average it. We must take off the percentage symbol from each one to be able to do the calculations
    RevenueGrowthPast5 = 0
    for i in range(2, len(IncomeStatement.columns) - 1):
        RevenueGrowthPast5 += float(IncomeStatement[i][1][0:-1])
    RevenueGrowthPast5 = RevenueGrowthPast5 / (len(IncomeStatement.columns) - 3)   
    
    #We check if the EBITDA exists in the income statement, and then we isolate it and convert the number from millions
    EBITDA = 0
    if len(IncomeStatement.loc[IncomeStatement[0] == 'EBITDA EBITDA']) == 1:
        EBITDA = IncomeStatement.loc[IncomeStatement[0] == 'EBITDA EBITDA'][len(IncomeStatement.columns) - 2]
        EBITDA = EBITDA[int(EBITDA.index.values)] #We dont know what position it is in so we find out and take only that specific value
        if EBITDA[-1] == 'B':
            EBITDA = float(EBITDA[0:-1]) * 1000000000
        elif EBITDA[-1] == 'M':
            EBITDA = float(EBITDA[0:-1]) * 1000000 
        elif EBITDA[-1] == 'K':
                EBITDA = float(EBITDA[0:-1]) * 1000    
        elif EBITDA == '-':
            EBITDA = 0    

    #We check if the Depreciation and Amortization exists in the income statement, and then we isolate it and convert the number from millions
    DepreciationAmortization = 0
    if len(IncomeStatement.loc[IncomeStatement[0] == 'Depreciation & Amortization Expense Depreciation & Amortization Expense']) == 1:
        DepreciationAmortization = IncomeStatement.loc[IncomeStatement[0] == 'Depreciation & Amortization Expense Depreciation & Amortization Expense'][len(IncomeStatement.columns) - 2]
        DepreciationAmortization = DepreciationAmortization[int(DepreciationAmortization.index.values)] #We dont know what position it is in so we find out and take only that specific value
        if DepreciationAmortization[-1] == 'B':
            DepreciationAmortization = float(DepreciationAmortization[0:-1]) * 1000000000
        elif DepreciationAmortization[-1] == 'M':
            DepreciationAmortization = float(DepreciationAmortization[0:-1]) * 1000000
        elif DepreciationAmortization[-1] == 'K':
                DepreciationAmortization = float(DepreciationAmortization[0:-1]) * 1000    
        elif DepreciationAmortization == '-':
            DepreciationAmortization = 0     
       
    #We check if the EPS of the past 5 years exists in the income statement, and then we isolate it and convert the number from millions
    EPSpast5 = []
    if len(IncomeStatement.loc[IncomeStatement[0] == 'EPS (Basic) EPS (Basic)']) == 1:
        #We want the last 5 years EPS so we isolate each case and add it to the list
        for i in range(1, len(IncomeStatement.columns) - 1):
            EPS = IncomeStatement.loc[IncomeStatement[0] == 'EPS (Basic) EPS (Basic)'][i]
            if EPS[int(EPS.index.values)] != '-':
                #The negative values for this in the website appear with a parentesis before it, so we must correct that
                if EPS[int(EPS.index.values)][0] == '(':
                    EPSpast5 += [-1 * (float(EPS[int(EPS.index.values)][1:-1]))]
                else:       
                    EPSpast5 += [float(EPS[int(EPS.index.values)])]        
    
    EPSgrowthPast5 = 0
    count = 0
    if len(IncomeStatement.loc[IncomeStatement[0] == 'EPS (Basic) Growth EPS (Basic) Growth']) == 1:       
        for i in range(2, len(IncomeStatement.columns) - 1):
            EPS = IncomeStatement.loc[IncomeStatement[0] == 'EPS (Basic) Growth EPS (Basic) Growth'][i]
            if EPS[int(EPS.index.values)] != '-':
                #We search to see if there are any commas and we remove them so that it can be converted to float
                for character in EPS[int(EPS.index.values)]:
                    if character == ',':
                        EPS = EPS.replace([EPS[int(EPS.index.values)]], EPS[int(EPS.index.values)].replace(character, ''))
                EPSgrowthPast5 += float(EPS[int(EPS.index.values)][0:-1])
                count += 1
        EPSgrowthPast5 = EPSgrowthPast5 / count 

    #Since the statement doesnt give us EBIT, we calculate it by using other metrics, first making sure we have these    
    EBIT = 0    
    if EBITDA != 0:
        EBIT = EBITDA - DepreciationAmortization

    return RevenuePast5, RevenueGrowthPast5, EBITDA, EBIT, DepreciationAmortization, EPSpast5, EPSgrowthPast5

def BalanceSheet(soup) -> float:
    #We inspect the webpage to finde the html tags of the objects that we want
    #Transform the html to a pandas dataframe
    #Balance sheet is broken up into these two categories
    BalanceSheet = pd.read_html(str(soup), attrs={'class': 'table table--overflow align--right'}) 

    Assets = BalanceSheet[0]
    Assets.columns = pd.RangeIndex(0, len(Assets.columns)) #Indexing the columns as numbers so that the differences in the name of columns wont matter
    
    #We check if the Total Assets exists in the income statement, and then we isolate it and convert the number from millions or billions
    TotalAssets = 0
    if len(Assets.loc[Assets[0] == 'Total Assets Total Assets']) == 1:
        TotalAssets = Assets.loc[Assets[0] == 'Total Assets Total Assets'][len(Assets.columns) - 2]
        TotalAssets = TotalAssets[int(TotalAssets.index.values)] #We dont know what position it is in so we find out and take only that specific value
        if TotalAssets[-1] == 'B':
            TotalAssets = float(TotalAssets[0:-1]) * 1000000000
        elif TotalAssets[-1] == 'M':
            TotalAssets = float(TotalAssets[0:-1]) * 1000000 
        elif TotalAssets[-1] == 'K':
                TotalAssets = float(TotalAssets[0:-1]) * 1000       
        elif TotalAssets == '-':
            TotalAssets = 0    

    #We check if the Total Current Assets exists in the income statement, and then we isolate it and convert the number from millions or billions
    TotalCurrentAssets = 0
    if len(Assets.loc[Assets[0] == 'Total Current Assets Total Current Assets']) == 1:
        TotalCurrentAssets = Assets.loc[Assets[0] == 'Total Current Assets Total Current Assets'][len(Assets.columns) - 2]
        TotalCurrentAssets = TotalCurrentAssets[int(TotalCurrentAssets.index.values)] #We dont know what position it is in so we find out and take only that specific value
        if TotalCurrentAssets[-1] == 'B':
            TotalCurrentAssets = float(TotalCurrentAssets[0:-1]) * 1000000000
        elif TotalCurrentAssets[-1] == 'M':
            TotalCurrentAssets = float(TotalCurrentAssets[0:-1]) * 1000000  
        elif TotalCurrentAssets[-1] == 'K':
                TotalCurrentAssets = float(TotalCurrentAssets[0:-1]) * 1000    
        elif TotalCurrentAssets == '-':
            TotalCurrentAssets = 0                       

    ###################################################################################################################################

    Liabilities = BalanceSheet[1]
    Liabilities.columns = pd.RangeIndex(0, len(Liabilities.columns)) #Indexing the columns as numbers so that the differences in the name of columns wont matter

    #We check if the Total Current Liabilities exists in the income statement, and then we isolate it and convert the number from millions or billions
    TotalCurrentLiabilities = 0
    if len(Liabilities.loc[Liabilities[0] == 'Total Current Liabilities Total Current Liabilities']) == 1:
        TotalCurrentLiabilities = Liabilities.loc[Liabilities[0] == 'Total Current Liabilities Total Current Liabilities'][len(Liabilities.columns) - 2]
        TotalCurrentLiabilities = TotalCurrentLiabilities[int(TotalCurrentLiabilities.index.values)] #We dont know what position it is in so we find out and take only that specific value
        if TotalCurrentLiabilities[-1] == 'B':
            TotalCurrentLiabilities = float(TotalCurrentLiabilities[0:-1]) * 1000000000
        elif TotalCurrentLiabilities[-1] == 'M':
            TotalCurrentLiabilities = float(TotalCurrentLiabilities[0:-1]) * 1000000   
        elif TotalCurrentLiabilities[-1] == 'K':
                TotalCurrentLiabilities = float(TotalCurrentLiabilities[0:-1]) * 1000    
        elif TotalCurrentLiabilities == '-':
            TotalCurrentLiabilities = 0    

    #We check if the Total Liabilities exists in the income statement, and then we isolate it and convert the number from millions or billions        
    TotalLiabilities = 0
    if len(Liabilities.loc[Liabilities[0] == 'Total Liabilities Total Liabilities']) == 1:
        TotalLiabilities = Liabilities.loc[Liabilities[0] == 'Total Liabilities Total Liabilities'][len(Liabilities.columns) - 2]
        TotalLiabilities = TotalLiabilities[int(TotalLiabilities.index.values)] #We dont know what position it is in so we find out and take only that specific value
        if TotalLiabilities[-1] == 'B':
            TotalLiabilities = float(TotalLiabilities[0:-1]) * 1000000000
        elif TotalLiabilities[-1] == 'M':
            TotalLiabilities = float(TotalLiabilities[0:-1]) * 1000000   
        elif TotalLiabilities[-1] == 'K':
                TotalLiabilities = float(TotalLiabilities[0:-1]) * 1000    
        elif TotalLiabilities == '-':
            TotalLiabilities = 0    
   
    #First we retrieve the liabilities to assets ratio of the past 5 years 
    RatioLA = []
    count = 0
    if len(Liabilities.loc[Liabilities[0] == 'Total Liabilities / Total Assets Total Liabilities / Total Assets']) == 1:       
        for i in range(1,len(Liabilities.columns) - 1):
            LA = Liabilities.loc[Liabilities[0] == 'Total Liabilities / Total Assets Total Liabilities / Total Assets'][i]
            if LA[int(LA.index.values)] != '-':
                RatioLA += [float(LA[int(LA.index.values)][0:-1])]
    #Now we calculate the growth of this ratio year over year            
    GrowthLA = 0            
    for i in range(1, len(RatioLA)):
        GrowthLA += (RatioLA[i] - RatioLA[i-1])
        count += 1
    if count != 0:   
        GrowthLA = GrowthLA / count

    #We check if the Total Equity exists in the income statement, and then we isolate it and convert the number from millions or billions        
    TotalEquity = 0
    if len(Liabilities.loc[Liabilities[0] == 'Total Equity Total Equity']) == 1:
        TotalEquity = Liabilities.loc[Liabilities[0] == 'Total Equity Total Equity'][len(Liabilities.columns) - 2]
        TotalEquity = TotalEquity[int(TotalEquity.index.values)] #We dont know what position it is in so we find out and take only that specific value
        if TotalEquity[-1] == 'B':
            TotalEquity = float(TotalEquity[0:-1]) * 1000000000
        elif TotalEquity[-1] == 'M':
            TotalEquity = float(TotalEquity[0:-1]) * 1000000   
        elif TotalEquity[-1] == 'K':
                TotalEquity = float(TotalEquity[0:-1]) * 1000    
        elif TotalEquity == '-':
            TotalEquity = 0

    #We calculate the long term assets and liabilities with the difference of other two metrics but first we must make sure that these exist        
    LongTermAssets = 0
    if TotalAssets != 0:        
        LongTermAssets = TotalAssets - TotalCurrentAssets

    LongTermLiabilities = 0    
    if LongTermLiabilities != 0:
        LongTermLiabilities = TotalLiabilities - TotalCurrentLiabilities        

    return TotalEquity, GrowthLA, TotalLiabilities, TotalCurrentLiabilities, LongTermLiabilities, TotalAssets, TotalCurrentAssets, LongTermAssets             
            
def CashFlow(soup) -> float:
    #We inspect the webpage to finde the html tags of the objects that we want
    #Transform the html to a pandas dataframe
    #Cash flow is broken up into these three categories
    CashFlow = pd.read_html(str(soup), attrs={'class': 'table table--overflow align--right'})  
    
    OperatingActivities = CashFlow[0]
    OperatingActivities.columns = pd.RangeIndex(0, len(OperatingActivities.columns)) #Indexing the columns as numbers so that the differences in the name of columns wont matter

    #We check if the Net Operating Cash Flow exists in the income statement, and then we isolate it and convert the number from millions or billions     
    NetOperatingCashFlow = 0
    if len(OperatingActivities.loc[OperatingActivities[0] == 'Net Operating Cash Flow Net Operating Cash Flow']) == 1:
        NetOperatingCashFlow = OperatingActivities.loc[OperatingActivities[0] == 'Net Operating Cash Flow Net Operating Cash Flow'][len(OperatingActivities.columns) - 2]
        NetOperatingCashFlow = NetOperatingCashFlow[int(NetOperatingCashFlow.index.values)]
        #Since negative values come with parentesis , we check for those and then remove them
        if NetOperatingCashFlow[0] == '(':
            NetOperatingCashFlow = NetOperatingCashFlow[1:-1] #We dont know what position it is in so we find out and take only that specific value
            if NetOperatingCashFlow[-1] == 'B':
                NetOperatingCashFlow = float(NetOperatingCashFlow[0:-1]) * -1000000000
            elif NetOperatingCashFlow[-1] == 'M':
                NetOperatingCashFlow = float(NetOperatingCashFlow[0:-1]) * -1000000   
            elif NetOperatingCashFlow[-1] == 'K':
                NetOperatingCashFlow = float(NetOperatingCashFlow[0:-1]) * -1000    
        elif NetOperatingCashFlow[-1] == 'B':
            NetOperatingCashFlow = float(NetOperatingCashFlow[0:-1]) * 1000000000
        elif NetOperatingCashFlow[-1] == 'M':
            NetOperatingCashFlow = float(NetOperatingCashFlow[0:-1]) * 1000000   
        elif NetOperatingCashFlow[-1] == 'K':
                NetOperatingCashFlow = float(NetOperatingCashFlow[0:-1]) * 1000           
        elif NetOperatingCashFlow == '-':
            NetOperatingCashFlow = 0             

    InvestingActivities = CashFlow[1]
    InvestingActivities.columns = pd.RangeIndex(0, len(InvestingActivities.columns)) #Indexing the columns as numbers so that the differences in the name of columns wont matter

    FinancingActivities = CashFlow[2]
    FinancingActivities.columns = pd.RangeIndex(0, len(FinancingActivities.columns)) #Indexing the columns as numbers so that the differences in the name of columns wont matter
    
    #We check if the Debt reduction exists in the income statement, and then we isolate it and convert the number from millions or billions     
    DebtReduction = 0
    TotalDebtReduction = 0
    if len(FinancingActivities.loc[FinancingActivities[0] == 'Issuance/Reduction of Debt, Net Issuance/Reduction of Debt, Net']) == 1:
        #We want to see how much debt was reduced total in the past five years so we add each one
        for i in range(1, len(FinancingActivities.columns) - 1):
            DebtReduction = FinancingActivities.loc[FinancingActivities[0] == 'Issuance/Reduction of Debt, Net Issuance/Reduction of Debt, Net'][i]
            DebtReduction = DebtReduction[int(DebtReduction.index.values)]
            #Since negative values come with parentesis , we check for those and then remove them
            if DebtReduction[0] == '(':
                DebtReduction = DebtReduction[1:-1] #We dont know what position it is in so we find out and take only that specific value
                if DebtReduction[-1] == 'B':
                    DebtReduction = float(DebtReduction[0:-1]) * -1000000000
                elif DebtReduction[-1] == 'M':
                    DebtReduction = float(DebtReduction[0:-1]) * -1000000 
                elif DebtReduction[-1] == 'K':
                    DebtReduction = float(DebtReduction[0:-1]) * -1000        
            elif DebtReduction[-1] == 'B':
                DebtReduction = float(DebtReduction[0:-1]) * 1000000000
            elif DebtReduction[-1] == 'M':
                DebtReduction = float(DebtReduction[0:-1]) * 1000000 
            elif DebtReduction[-1] == 'K':
                DebtReduction = float(DebtReduction[0:-1]) * 1000             
            elif DebtReduction == '-':
                DebtReduction = 0 
            TotalDebtReduction += DebtReduction          

    #We check if the Free Cash Flow exists in the income statement, and then we isolate it and convert the number from millions or billions     
    FreeCashFlow = 0
    if len(FinancingActivities.loc[FinancingActivities[0] == 'Free Cash Flow Free Cash Flow']) == 1:
        FreeCashFlow = FinancingActivities.loc[FinancingActivities[0] == 'Free Cash Flow Free Cash Flow'][len(FinancingActivities.columns) - 2]
        FreeCashFlow = FreeCashFlow[int(FreeCashFlow.index.values)]
        #Since negative values come with parentesis , we check for those and then remove them
        if FreeCashFlow[0] == '(':
            FreeCashFlow = FreeCashFlow[1:-1] #We dont know what position it is in so we find out and take only that specific value
            if FreeCashFlow[-1] == 'B':
                FreeCashFlow = float(FreeCashFlow[0:-1]) * -1000000000
            elif FreeCashFlow[-1] == 'M':
                FreeCashFlow = float(FreeCashFlow[0:-1]) * -1000000 
            elif FreeCashFlow[-1] == 'K':
                FreeCashFlow = float(FreeCashFlow[0:-1]) * -1000       
        elif FreeCashFlow[-1] == 'B':
            FreeCashFlow = float(FreeCashFlow[0:-1]) * 1000000000
        elif FreeCashFlow[-1] == 'M':
            FreeCashFlow = float(FreeCashFlow[0:-1]) * 1000000 
        elif FreeCashFlow[-1] == 'K':
                FreeCashFlow = float(FreeCashFlow[0:-1]) * 1000             
        elif FreeCashFlow == '-':
            FreeCashFlow = 0

    return FreeCashFlow, TotalDebtReduction, NetOperatingCashFlow                 

def EPSRevisions(soup) -> float:
    #We inspect the webpage to finde the html tags of the objects that we want
    #Transform the html to a pandas dataframe
    #estimates is broken down in four different parts and we want the last two
    estimates = pd.read_html(str(soup), attrs={'class' : 'table value-pairs no-heading font--lato'})

    firstYear = estimates[2] #EPS estimate for next year revisions from 3 months ago 1 month ago and current 
    estimateRevision1 = 0
    for i in range(2, 0, -1):
        #We calculate the percentage change from one year to another and then average them out
        estimateRevision1 += (float(firstYear[1][i - 1][1:]) * 100) / float(firstYear[1][i][1:]) - 100
        
    secondYear = estimates[3] #EPS estimate for the year after next year revisions from 3 months ago 1 month ago and current 
    estimateRevision2 = 0
    for i in range(2, 0, -1):
        #We calculate the percentage change of the revisions 
        estimateRevision2 += (float(secondYear[1][i - 1][1:]) * 100) / float(secondYear[1][i][1:]) - 100

    return estimateRevision1, estimateRevision2

def PriceTargets(soup) -> float:
    #We inspect the webpage to finde the html tags of the objects that we want
    #Transform the html to a pandas dataframe
    #estimates is broken down in four different parts and we want the second one
    estimates = pd.read_html(str(soup), attrs={'class' : 'table value-pairs no-heading font--lato'})

    priceTargets = estimates[1]
    HighTarget = float(priceTargets[1][0][1:])
    LowTarget = float(priceTargets[1][2][1:])
    AverageTarget = float(priceTargets[1][3][1:])

    Summary = estimates[0]
    NumberOfRatings = int(Summary[1][2])

    return HighTarget, LowTarget, AverageTarget, NumberOfRatings

def EPSEstimates(soup):
    #We inspect the webpage to finde the html tags of the objects that we want
    #Transform the html to a pandas dataframe
    EPSestimates = pd.read_html(str(soup), attrs={'class' : 'table table--primary'})[0]
    #We save the chart to be able to graph the estimates later 

    return EPSestimates

def Recomendations(soup) -> int:
    #We inspect the webpage to finde the html tags of the objects that we want
    #Transform the html to a pandas dataframe
    recom = pd.read_html(str(soup), attrs={'class' : 'table table-primary align--left border--dotted'})    
    #retieve info to create a bar chart, timeframes: current 1M ago 3M ago, Ratings: buy overweight hold underweight sell
    print(recom)


def main ():
    
    Ticker = 'dss'
    url1 = 'http://finviz.com/quote.ashx?t=' + Ticker
    req1 = Request(url1, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
    webpage_coded1 = urlopen(req1, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

    soup1 = BeautifulSoup(webpage_coded1, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

    url2 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/financials'
    req2 = Request(url2, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
    webpage_coded2 = urlopen(req2, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded2 = webpage_coded2.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

    soup2 = BeautifulSoup(webpage_coded2, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

    url3 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/financials/balance-sheet'
    req3 = Request(url3, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
    webpage_coded3 = urlopen(req3, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

    soup3 = BeautifulSoup(webpage_coded3, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

    url4 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/financials/cash-flow'
    req4 = Request(url4, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
    webpage_coded4 = urlopen(req4, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

    soup4 = BeautifulSoup(webpage_coded4, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ###################################################################################################################################################

    url5 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/analystestimates?mod=mw_quote_tab'
    req5 = Request(url5, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
    webpage_coded5 = urlopen(req5, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

    soup5 = BeautifulSoup(webpage_coded5, 'html.parser') #Parsing(breaking the code down into relevant info) the html code


    PE, PEG, PS, PB, MarketCap, DebtEquity, Recom, InsiderTrans, InstitutionTrans, ROA, ROE, AvgVolume, Price, LastChange, PerfWeek, PerfMonth, PerfYear, YearHighPercent, EPSNextY, EPSNext5Y = fundamentalInfoFVZ(soup1)

    RevenuePast5, RevenueGrowthPast5, EBITDA, EBIT, DepreciationAmortization, EPSpast5, EPSgrowthPast5 = IncomeStatementMW(soup2)
    TotalEquity, GrowthLA, TotalLiabilities, TotalCurrentLiabilities, LongTermLiabilities, TotalAssets, TotalCurrentAssets, LongTermAssets = BalanceSheet(soup3)
    FreeCashFlow, TotalDebtReduction, NetOperatingCashFlow = CashFlow(soup4)

    estimateRevision1, estimateRevision2 = EPSRevisions(soup5)
    HighTarget, LowTarget, AverageTarget, NumberOfRatings = PriceTargets(soup5)

    EPSestimates = EPSEstimates(soup5)

    Recomendations(soup5)



if __name__ == '__main__': main()