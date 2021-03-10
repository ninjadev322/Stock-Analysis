#-----------------------------------------------------------------------
# main.py
# Description:
# Author: André Luiz Queiroz Costa
# Date: 06/03/2020
# Version: 1.0
#-----------------------------------------------------------------------

#The objective of the code is to to execute all the codes and show all the graphs for one ticker

from typing import List
from dataScraping import *
from pointSystem import *
from revenueEarningsChart import *
from priceTargetChart import *
from recomBarChart import *
import colorama
from colorama import Fore, Style 

colorama.init()

def accessWeb(Ticker:str):

	url1 = 'http://finviz.com/quote.ashx?t=' + Ticker
	req1 = Request(url1, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded1 = urlopen(req1, timeout = 1).read() #We open the page and read all the raw info
   	#webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup1 = BeautifulSoup(webpage_coded1, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

	url2 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/financials'
	req2 = Request(url2, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded2 = urlopen(req2, timeout = 1).read() #We open the page and read all the raw info
    #webpage_decoded2 = webpage_coded2.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup2 = BeautifulSoup(webpage_coded2, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

	url3 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/financials/balance-sheet'
	req3 = Request(url3, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded3 = urlopen(req3, timeout = 1).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup3 = BeautifulSoup(webpage_coded3, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

	url4 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/financials/cash-flow'
	req4 = Request(url4, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded4 = urlopen(req4, timeout = 1).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup4 = BeautifulSoup(webpage_coded4, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ###################################################################################################################################################

	url5 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/analystestimates?mod=mw_quote_tab'
	req5 = Request(url5, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded5 = urlopen(req5, timeout = 1).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup5 = BeautifulSoup(webpage_coded5, 'html.parser') #Parsing(breaking the code down into relevant info) the html code
	
	#####################################################################################################################################################

	url6 = 'https://finance.yahoo.com/quote/' + Ticker + '/analysis?p=' + Ticker
	req6 = Request(url6, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded6 = urlopen(req6, timeout = 1).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup6 = BeautifulSoup(webpage_coded6, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

	return soup1, soup2, soup3, soup4, soup5, soup6

def main ():
	#obtain the ticker wanted by the user
	Ticker = str(input('Ticker: '))

	#get all the websites necessary to scrape info
	wrong = False
	try:
		print(f'Webscraping info for {Ticker.upper()}...')
		soup1, soup2, soup3, soup4, soup5, soup6 = accessWeb(Ticker)
	except:
		wrong = True

	#############################################################################################################################

	if wrong:
		print(f'{Ticker.upper()} not available')
	
	else:
		#if it is available, we webscrape and evaluate each individual stock
		print(f'Analyzing and Assesing Data...')
		print()
		PE, PEG, PS, PB, MarketCap, DebtEquity, Recom, InsiderTrans, InstitutionTrans, ROA, ROE, AvgVolume, Price, LastChange, PerfWeek, PerfMonth, PerfYear, YearHighPercent, EPSNextY, EPSNext5Y = fundamentalInfoFVZ(soup1)

		RevenuePast5, RevenueGrowthPast5, EBITDA, EBIT, DepreciationAmortization, EPSpast5, EPSgrowthPast5, InterestExpense, NetIncomePast5 = IncomeStatementMW(soup2)
		TotalEquity, GrowthLA, GrowthDA, TotalLiabilities, TotalCurrentLiabilities, LongTermLiabilities, TotalAssets, TotalCurrentAssets, LongTermAssets, ShortTermDebt, LongTermDebt = BalanceSheet(soup3)
		FreeCashFlow, TotalDebtReduction, NetOperatingCashFlow = CashFlow(soup4)

		estimateRevision1, estimateRevision2 = EPSRevisions(soup5)
		HighTarget, LowTarget, AverageTarget, NumberOfRatings = PriceTargets(soup5)

		EPSestimates = EPSEstimates(soup5)
		RevenueGrowthNextY = RevenuesEstimates(soup6)

		columnNames, xValues, Buy, Overweight, Hold, Underweight, Sell = Recomendations(soup5)

		###############################################################################################################################

		pointsEarnedHealth, TotalpointsHealth, RatioLE, RatioFD, RatioLA, RatioLA2, RatioLA3 = health(DebtEquity, LongTermLiabilities, NetOperatingCashFlow, EBIT, InterestExpense, TotalCurrentAssets, TotalCurrentLiabilities, TotalLiabilities, GrowthLA, TotalEquity, ShortTermDebt, LongTermDebt, TotalDebtReduction, GrowthDA, TotalAssets)
		pointsEarnedFuture, TotalpointsFuture = future(EPSNextY, EPSNext5Y, estimateRevision1, estimateRevision2, AverageTarget, LowTarget, Buy, Overweight, Hold, Underweight, Sell, RevenueGrowthNextY, Price)
		pointsEarnedPast, TotalpointsPast = past(ROA, ROE, RevenuePast5, RevenueGrowthPast5, EPSpast5, EPSgrowthPast5, NetIncomePast5)
		pointsEarnedInsiders, TotalpointsInsiders = insiders(InsiderTrans, InstitutionTrans)
		pointsEarnedValue, TotalpointsValue, GoldenRatio = value(PE, PEG, PS, PB, YearHighPercent, EBITDA, LongTermDebt, ShortTermDebt, FreeCashFlow, MarketCap, NetIncomePast5)

		################################################################################################################################	

		print(f'Value: {round(pointsEarnedValue * 10 / TotalpointsValue, 2)} ({pointsEarnedValue}/{TotalpointsValue})' + 3*'\t' + f'Health: {pointsEarnedHealth * 10 / TotalpointsHealth} ({pointsEarnedHealth}/{TotalpointsHealth})')
		print(Fore.GREEN + Style.BRIGHT + f'PE: {PE} (<23 is a Good PE)' + Style.RESET_ALL if float(PE) <= 23 else Fore.RED + Style.BRIGHT + f'PE: {PE} (<23 is a Good PE)' + Style.RESET_ALL , end = '')
		print(2*'\t' + f'Debt/Equity: {round(float(DebtEquity), 2)} (<0.4 is a Good DE Ratio)')
		print(f'PEG: {PEG} (<1.3 is a Good PEG)' + 2*'\t' + f'InterestExpense/EBIT: {round(RatioLE, 2)} (<0.33 is a Good IEE Ratio)')
		print(f'PS: {PS} (<1.8 is a Good PS)' + 2*'\t' + f'NetOperatingCashFlow/Debt: {round(RatioFD, 2)} (>0.5 is a Good NOCFD Ratio)')
		print(f'PB: {PB} (<3 is a Good PB)' + 2*'\t' + f'CurrentLiabilities/CurrentAssets: {round(RatioLA, 2)} (<1 is a Good CLCA Ratio)')
		print(f'Golden Ratio: {round(GoldenRatio, 2)}' + 3*'\t' + f'LongTermLiabilities/CurrentAssets: {round(RatioLA2, 2)} (<1.25 is a Good LTLCA Ratio)')
		print(f'Year High Percent: {YearHighPercent}' + 2*'\t' + f'Liabilities&Equity/Assets: {round(RatioLA3, 2)} (<1 is a Good LEA Ratio)')
		print(5*'\t' + f'Growth Liabilities/Assets: {GrowthLA} (<0 is a Good LA Growth)')
		print(5*'\t' + f'Growth Debt/Assets: {GrowthDA} (<0 is a Good DA Growth)')
		print(5*'\t' + f'Debt Reduction: {TotalDebtReduction} (<0 is a Good Debt Reduction)')

		#we define different figures for each chart and then place them in different parts of the screen
		#plt.figure(1)
		#RBchart(Ticker, columnNames, Buy, Overweight, Hold, Underweight, Sell)
		#plt.figure(2)
		#REchart(Ticker, RevenuePast5, NetIncomePast5, soup2, soup1)
		#plt.figure(3)
		#PTchart(Ticker, Price, HighTarget, LowTarget, AverageTarget, NumberOfRatings)

		#plt.show()


if __name__ == '__main__': main() 