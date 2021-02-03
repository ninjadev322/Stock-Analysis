#-----------------------------------------------------------------------
# values.py
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
#lxml package

def fundamentalInfoFVZ(soup) -> float:
    #We inspect the webpage to finde the html tags of the pbjects that we want
    #Transforms the html to a pandas dataframe
    fundamentals = pd.read_html(str(soup), attrs={'class': 'snapshot-table2'}) #Can only do this if class type is a table 

    PE = fundamentals[0][3][0] #Price to earnings ratio
    PEG = fundamentals[0][3][2] #Price to earnings growth ratio
    PS = fundamentals[0][3][3] #Price to sales ratio
    PB = fundamentals[0][3][4] # Price to book value ratio

    MarketCap = fundamentals[0][1][1] #Number of shares times the the current price of each share
    MarketCap = float(MarketCap[0:-1]) #When scraped comes with a B or M at the end we tranform it into number 
    MarketCap = MarketCap * 1000000000 #The value is given to use in billions so we transform it

    return PE, PEG, PS, PB, MarketCap

def IncomeStatementMW(soup) -> float:
    #We inspect the webpage to finde the html tags of the objects that we want
    #Transform the html to a pandas dataframe
    IncomeStatement = pd.read_html(str(soup), attrs={'class': 'table table--overflow align--right'}) #Can only do this if class type is a table 
    IncomeStatement = IncomeStatement[0] #Only getting the table since there are more objects with the same class
    IncomeStatement.columns = pd.RangeIndex(0, 7) #Indexing the columns as numbers so that the differences in the name of columns wont matter

    RevenuePast5 = [IncomeStatement[1][0], IncomeStatement[2][0], IncomeStatement[3][0], IncomeStatement[4][0], IncomeStatement[5][0]]
    #We must change the values from billions and millions to full numbers
    for i in range(len(RevenuePast5)):
        if RevenuePast5[i][-1] == 'B':
            RevenuePast5[i] = float(RevenuePast5[i][0:-1]) * 1000000000
        elif RevenuePast5[i][-1] == 'M':
            RevenuePast5[i] = float(RevenuePast5[i][0:-1]) * 1000000     
    
    #We take the growth year to year and average it. We must take off the percentage symbol from each one to be able to do the calculations
    RevenueGrowthPast5 = (float(IncomeStatement[2][1][0:-1]) + float(IncomeStatement[3][1][0:-1]) + float(IncomeStatement[4][1][0:-1]) + float(IncomeStatement[5][1][0:-1])) / 4
    
    #We check if the EBITDA exists in the income statement, and then we isolate it and convert the number from millions
    EBITDA = 0
    if len(IncomeStatement.loc[IncomeStatement[0] == 'EBITDA EBITDA']) == 1:
        EBITDA = IncomeStatement.loc[IncomeStatement[0] == 'EBITDA EBITDA'][5]
        EBITDA = EBITDA[int(EBITDA.index.values)] #We dont know what position it is in so we find out and take only that specific value
        if EBITDA[-1] == 'B':
            EBITDA[i] = float(EBITDA[0:-1]) * 1000000000
        elif EBITDA[-1] == 'M':
            EBITDA = float(EBITDA[0:-1]) * 1000000 
    

    #We check if the Depreciation and Amortization exists in the income statement, and then we isolate it and convert the number from millions
    DepreciationAmortization = 0
    if len(IncomeStatement.loc[IncomeStatement[0] == 'Depreciation & Amortization Expense Depreciation & Amortization Expense']) == 1:
        DepreciationAmortization = IncomeStatement.loc[IncomeStatement[0] == 'Depreciation & Amortization Expense Depreciation & Amortization Expense'][5]
        DepreciationAmortization = DepreciationAmortization[int(DepreciationAmortization.index.values)] #We dont know what position it is in so we find out and take only that specific value
        if DepreciationAmortization[-1] == 'B':
            DepreciationAmortization[i] = float(DepreciationAmortization[0:-1]) * 1000000000
        elif DepreciationAmortization[-1] == 'M':
            DepreciationAmortization = float(DepreciationAmortization[0:-1]) * 1000000

    #We check if the EPS of the past 5 years exists in the income statement, and then we isolate it and convert the number from millions
    EPSpast5 = []
    if len(IncomeStatement.loc[IncomeStatement[0] == 'EPS (Basic) EPS (Basic)']) == 1:
        #We want the last 5 years EPS so we isolate each case and add it to the list
        for i in range(1,6):
            EPS = IncomeStatement.loc[IncomeStatement[0] == 'EPS (Basic) EPS (Basic)'][i]
            EPSpast5 += [float(EPS[int(EPS.index.values)])]
    
    EPSgrowthPast5 = 0
    if len(IncomeStatement.loc[IncomeStatement[0] == 'EPS (Basic) Growth EPS (Basic) Growth']) == 1:       
        for i in range(2,6):
            EPS = IncomeStatement.loc[IncomeStatement[0] == 'EPS (Basic) Growth EPS (Basic) Growth'][i]
            EPSgrowthPast5 += float(EPS[int(EPS.index.values)][0:-1])
        EPSgrowthPast5 = EPSgrowthPast5 / 4    

    #Since the statement doesnt give us EBIT, we calculate it by using other metrics, first making sure we have these    
    EBIT = 0    
    if EBITDA != 0 or DepreciationAmortization != 0:
        EBIT = EBITDA - DepreciationAmortization

    return RevenuePast5, RevenueGrowthPast5, EBITDA, EBIT, DepreciationAmortization, EPSpast5, EPSgrowthPast5

def BalanceSheet(soup) -> None:
    #We inspect the webpage to finde the html tags of the objects that we want
    #Transform the html to a pandas dataframe
    #Balance sheet is broken up into these two categories
    BalanceSheet = pd.read_html(str(soup3), attrs={'class': 'table table--overflow align--right'}) 
    Assets = BalanceSheet[0]
    Liabilities = BalanceSheet[1]

def CashFlow(soup) -> None:
    #We inspect the webpage to finde the html tags of the objects that we want
    #Transform the html to a pandas dataframe
    #Cash flow is broken up into these three categories
    CashFlow = pd.read_html(str(soup4), attrs={'class': 'table table--overflow align--right'})  
    OperatingActivities = CashFlow[0]
    FinancialActivities = CashFlow[1]
    InvestingActiviteies = CashFlow[2]



def main ():

    url1 = 'http://finviz.com/quote.ashx?t=gff'
    req1 = Request(url1, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
    webpage_coded1 = urlopen(req1, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

    soup1 = BeautifulSoup(webpage_coded1, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

    url2 = 'https://www.marketwatch.com/investing/stock/gff/financials'
    req2 = Request(url2, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
    webpage_coded2 = urlopen(req2, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded2 = webpage_coded2.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

    soup2 = BeautifulSoup(webpage_coded2, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

    url3 = 'https://www.marketwatch.com/investing/stock/gff/financials/balance-sheet'
    req3 = Request(url3, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
    webpage_coded3 = urlopen(req3, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

    soup3 = BeautifulSoup(webpage_coded3, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

    url4 = 'https://www.marketwatch.com/investing/stock/gff/financials/cash-flow'
    req4 = Request(url4, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
    webpage_coded4 = urlopen(req4, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

    soup4 = BeautifulSoup(webpage_coded4, 'html.parser') #Parsing(breaking the code down into relevant info) the html code


    PE, PEG, PS, PB, MarketCap = fundamentalInfoFVZ(soup1)
    RevenuePast5, RevenueGrowthPast5, EBITDA, EBIT, DepreciationAmortization, EPSpast5, EPSgrowthPast5 = IncomeStatementMW(soup2)



    #insider = pd.read_html(str(soup), attrs={'class': 'body-table'})
    #print(insider[0])

    #ratings = pd.read_html(str(soup), attrs={'class': 'fullview-ratings-outer'})
    #print(ratings[0])




if __name__ == '__main__': main()