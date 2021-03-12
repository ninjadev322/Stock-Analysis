#-----------------------------------------------------------------------
# main.py
# Description:
# Author: André Luiz Queiroz Costa
# Date: 06/03/2020
# Version: 1.0
#-----------------------------------------------------------------------

#The objective of the code is to to execute all the codes and show all the graphs for one ticker as well as visualizing the parameters for each category with
#colors to identify which have met the prerequisites and which have not 

from typing import List
from dataScraping import *
from pointSystem import *
from revenueEarningsChart import *
from priceTargetChart import *
from recomBarChart import *
import colorama
from colorama import Fore, Style 

#we initiate the colorama module
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
		print(f'{Ticker.upper()} not available (Check WIFI)')
	
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
		pointsEarnedFuture, TotalpointsFuture, numBuy, numOverweight, numHold, numUnderweight, numSell = future(EPSNextY, EPSNext5Y, estimateRevision1, estimateRevision2, AverageTarget, LowTarget, Buy, Overweight, Hold, Underweight, Sell, RevenueGrowthNextY, Price)
		pointsEarnedPast, TotalpointsPast, ProfitMarginsGrowth = past(ROA, ROE, RevenuePast5, RevenueGrowthPast5, EPSpast5, EPSgrowthPast5, NetIncomePast5)
		pointsEarnedInsiders, TotalpointsInsiders = insiders(InsiderTrans, InstitutionTrans)
		pointsEarnedValue, TotalpointsValue, GoldenRatio = value(PE, PEG, PS, PB, YearHighPercent, EBITDA, LongTermDebt, ShortTermDebt, FreeCashFlow, MarketCap, NetIncomePast5)

		################################################################################################################################	

		#printing general data
		print(f'Avg Volume: {AvgVolume}')
		print(f'Market Cap: {MarketCap}')
		print(f'Price: {Price}')

		print()
		print()

		#we print the 5 categories with the each individual parameters that we have evaluated
		#if in each parameter, the prerequisite was met, then it prints in green. else, it prints in red
		print(f'Value: {round(pointsEarnedValue * 10 / TotalpointsValue, 2)} ({pointsEarnedValue}/{TotalpointsValue})' + 4*'\t' + f'Health: {pointsEarnedHealth * 10 / TotalpointsHealth} ({pointsEarnedHealth}/{TotalpointsHealth})')

		print(Fore.GREEN + Style.BRIGHT + f'PE: {PE} (<23, <15)' + Style.RESET_ALL if float(PE) <= 23 and float(PE) != -1 else Fore.RED + Style.BRIGHT + f'PE: {PE} (<23, <15)' + Style.RESET_ALL , end = '')
		print(4*'\t' + Fore.GREEN + Style.BRIGHT + f'Debt/Equity: {round(float(DebtEquity), 2)} (<0.8, <0.4)' + Style.RESET_ALL if float(DebtEquity) <= 0.8 and float(DebtEquity) != -1 else 4*'\t' + Fore.RED + Style.BRIGHT + f'Debt/Equity: {round(float(DebtEquity), 2)} (<0.8, <0.4)' + Style.RESET_ALL)
		
		print(Fore.GREEN + Style.BRIGHT + f'PEG: {PEG} (<1.3, <1)' + Style.RESET_ALL if float(PEG) <= 1.3 and float(PEG) != -1 else Fore.RED + Style.BRIGHT + f'PEG: {PEG} (<1.3, <1)', end = '')
		print(4*'\t' + Fore.GREEN + Style.BRIGHT + f'InterestExpense/EBIT: {round(RatioLE, 2)} (<0.33)' + Style.RESET_ALL if RatioLE <= 0.33 and RatioLE != -1 else 4*'\t' + Fore.RED + Style.BRIGHT + f'InterestExpense/EBIT: {round(RatioLE, 2)} (<0.33)' + Style.RESET_ALL)
		
		print(Fore.GREEN + Style.BRIGHT + f'PS: {PS} (<1.8, <1)' + Style.RESET_ALL if float(PS) <= 1.8 and float(PS) != -1 else Fore.RED + Style.BRIGHT + f'PS: {PS} (<1.8, <1)' + Style.RESET_ALL, end = '')		
		print(4*'\t' + Fore.GREEN + Style.BRIGHT + f'NetOperatingCashFlow/Debt: {round(RatioFD, 2)} (>0.25, >0.5, >1)' + Style.RESET_ALL if RatioFD >= 0.5 else 4*'\t' + Fore.RED + Style.BRIGHT + f'NetOperatingCashFlow/Debt: {round(RatioFD, 2)} (>0.25, >0.5, >1)' + Style.RESET_ALL)

		print(Fore.GREEN + Style.BRIGHT + f'PB: {PB} (<3, <1)' + Style.RESET_ALL if float(PB) <= 3 and float(PB) != -1 else Fore.RED + Style.BRIGHT + f'PB: {PB} (<3, <1)' + Style.RESET_ALL, end = '')
		print(4*'\t' + Fore.GREEN + Style.BRIGHT + f'CurrentLiabilities/CurrentAssets: {round(RatioLA, 2)} (<1)' + Style.RESET_ALL if RatioLA < 1 and RatioLA != -1 else 4*'\t' + Fore.RED + Style.BRIGHT + f'CurrentLiabilities/CurrentAssets: {round(RatioLA, 2)} (<1)' + Style.RESET_ALL)

		print(Fore.GREEN + Style.BRIGHT + f'Golden Ratio: {round(GoldenRatio, 2)} (<15, <10)' + Style.RESET_ALL if GoldenRatio < 15 and GoldenRatio != -1 else Fore.RED + Style.BRIGHT + f'Golden Ratio: {round(GoldenRatio, 2)} (<15, <10)' + Style.RESET_ALL, end = '') 
		print(3*'\t' + Fore.GREEN + Style.BRIGHT + f'LongTermLiabilities/CurrentAssets: {round(RatioLA2, 2)} (<1.25, <1)' + Style.RESET_ALL if RatioLA2 <= 1.25 and RatioLA2 != -1 else 3*'\t' + Fore.RED + Style.BRIGHT + f'LongTermLiabilities/CurrentAssets: {round(RatioLA2, 2)} (<1.25, <1)' + Style.RESET_ALL)

		print(Fore.GREEN + Style.BRIGHT + f'-% 52WHigh: {YearHighPercent} (<-10, <-20)' + Style.RESET_ALL if float(YearHighPercent) <= -10 else Fore.RED + Style.BRIGHT + f'-% 52WHigh: {YearHighPercent} (<-10, <-20)' + Style.RESET_ALL, end = '')
		print(3*'\t' + Fore.GREEN + Style.BRIGHT + f'Liabilities&Equity/Assets: {round(RatioLA3, 2)} (<1)' + Style.RESET_ALL if RatioLA3 < 1 and RatioLA3 != -1 else 3*'\t' + Fore.RED + Style.BRIGHT + f'Liabilities&Equity/Assets: {round(RatioLA3, 2)} (<1)' + Style.RESET_ALL)
		
		print(6*'\t' + Fore.GREEN + Style.BRIGHT + f'Growth Liabilities/Assets: {GrowthLA} (<0)' + Style.RESET_ALL if GrowthLA < 0 and GrowthLA != -1 else 6*'\t' + Fore.RED + Style.BRIGHT + f'Growth Liabilities/Assets: {GrowthLA} (<0)' + Style.RESET_ALL)
		print(6*'\t' + Fore.GREEN + Style.BRIGHT + f'Growth Debt/Assets: {GrowthDA} (<0)' + Style.RESET_ALL if GrowthDA < 0 and GrowthDA != -1 else 6*'\t' + Fore.RED + Style.BRIGHT + f'Growth Debt/Assets: {GrowthDA} (<0)' + Style.RESET_ALL)
		print(6*'\t' + Fore.GREEN + Style.BRIGHT + f'Debt Reduction: {TotalDebtReduction} (<0)' + Style.RESET_ALL if TotalDebtReduction < 0 and TotalDebtReduction != -1 else 6*'\t' + Fore.RED + Style.BRIGHT + f'Debt Reduction: {TotalDebtReduction} (<0)' + Style.RESET_ALL)

		print()
		print()

		print(f'Future: {round(pointsEarnedFuture * 10 / TotalpointsFuture, 2)} ({pointsEarnedFuture}/{TotalpointsFuture})' + 4*'\t' + f'Past: {pointsEarnedPast * 10 / TotalpointsPast} ({pointsEarnedPast}/{TotalpointsPast})')

		print(Fore.GREEN + Style.BRIGHT + f'EPS %Growth NextY: {EPSNextY} (>10, >20)' + Style.RESET_ALL if float(EPSNextY) > 10 and float(EPSNextY) != -1 else Fore.RED + Style.BRIGHT + f'EPS %Growth NextY: {EPSNextY} (>10, >20)' + Style.RESET_ALL, end = '')
		print(2*'\t' + Fore.GREEN + Style.BRIGHT + f'EPS %Growth Past5Y: {round(float(EPSgrowthPast5), 2)} (>10, >20)' + Style.RESET_ALL if float(EPSgrowthPast5) > 10 and float(EPSgrowthPast5) != -1 else 2*'\t' + Fore.RED + Style.BRIGHT + f'EPS %Growth Past5Y: {round(float(EPSgrowthPast5), 2)} (>10, >20)' + Style.RESET_ALL)	

		print(Fore.GREEN + Style.BRIGHT + f'EPS %Growth Next5Y: {EPSNext5Y} (>10, >20)' + Style.RESET_ALL if float(EPSNext5Y) > 10 and float(EPSNext5Y) != -1 else Fore.RED + Style.BRIGHT + f'EPS %Growth Next5Y: {EPSNext5Y} (>10, >20)' + Style.RESET_ALL, end = '')
		print(2*'\t' + Fore.GREEN + Style.BRIGHT + f'Rev %Growth Past5Y: {round(float(RevenueGrowthPast5), 2)} (>10, >20)' + Style.RESET_ALL if float(RevenueGrowthPast5) > 10 and float(RevenueGrowthPast5) != -1 else 2*'\t' + Fore.RED + Style.BRIGHT + f'Rev %Growth Past5Y: {round(float(RevenueGrowthPast5), 2)} (>10, >20)' + Style.RESET_ALL)		

		print(Fore.GREEN + Style.BRIGHT + f'Estimate Revision: {round(estimateRevision1, 2)} (>0)' + Style.RESET_ALL if estimateRevision1 > 0 and estimateRevision1 != -1 else Fore.RED + Style.BRIGHT + f'Estimate Revision: {round(estimateRevision1, 2)} (>0)' + Style.RESET_ALL, end = '')
		print(3*'\t' + Fore.GREEN + Style.BRIGHT + f'ROE: {float(ROE)} (>20)' + Style.RESET_ALL if float(ROE) >= 20 and float(ROE) != -1 else 3*'\t' + Fore.RED + Style.BRIGHT + f'ROE: {float(ROE)} (>20)' + Style.RESET_ALL)		

		print(Fore.GREEN + Style.BRIGHT + f'Price/AverageTarget: {round(float(Price) / AverageTarget, 2)} (<1)' + Style.RESET_ALL if float(Price) / AverageTarget < 1 and AverageTarget != -1 else Fore.RED + Style.BRIGHT + f'Price/AverageTarget: {round(float(Price) / AverageTarget, 2)} (<1)' + Style.RESET_ALL, end = '')
		print(3*'\t' + Fore.GREEN + Style.BRIGHT + f'ROA: {float(ROA)} (>5, >10)' + Style.RESET_ALL if float(ROA) >= 5 and float(ROA) != -1 else 3*'\t' + Fore.RED + Style.BRIGHT + f'ROA: {float(ROA)} (>5, >10)' + Style.RESET_ALL)			

		print(Fore.GREEN + Style.BRIGHT + f'Rev %Growth NextY: {RevenueGrowthNextY} (>5, >10, >20)' + Style.RESET_ALL if float(RevenueGrowthNextY) > 5 and float(RevenueGrowthNextY) != -1 else Fore.RED + Style.BRIGHT + f'Rev %Growth NextY: {RevenueGrowthNextY} (>5, >10, >20)' + Style.RESET_ALL, end = '')
		print(2*'\t' + Fore.GREEN + Style.BRIGHT + f'ProfMargin Growth: {round(float(ProfitMarginsGrowth), 2)} (>0, >10)' + Style.RESET_ALL if float(ProfitMarginsGrowth) > 0 and float(ProfitMarginsGrowth) != -1 else 2*'\t' + Fore.RED + Style.BRIGHT + f'ProfMargin Growth: {round(float(ProfitMarginsGrowth), 2)} (>0, >10)' + Style.RESET_ALL)		

		print(Fore.GREEN + Style.BRIGHT + f'Analyst Recom: {(numBuy + numOverweight) - (numHold + numSell + numUnderweight)} (>0)' + Style.RESET_ALL if (numBuy + numOverweight) - (numHold + numSell + numUnderweight) > 0 else Fore.RED + Style.BRIGHT + f'Analyst Recom: {(numBuy + numOverweight) - (numHold + numSell + numUnderweight)} (>0)' + Style.RESET_ALL)

		print()
		print()

		print(f'Insiders: {round(pointsEarnedInsiders * 10 / TotalpointsInsiders, 2)} ({pointsEarnedInsiders}/{TotalpointsInsiders})' if TotalpointsInsiders != 0 else f'Insiders: 0 ({pointsEarnedInsiders}/{TotalpointsInsiders})') 
		print(Fore.GREEN + Style.BRIGHT + f'%Insider Transactions: {InsiderTrans} (>0)' + Style.RESET_ALL if float(InsiderTrans) > 0 else Fore.RED + Style.BRIGHT + f'%Insider Transactions: {InsiderTrans} (>0)' + Style.RESET_ALL)
		print(Fore.GREEN + Style.BRIGHT + f'%Institution Transactions: {InstitutionTrans} (>0, >5)' + Style.RESET_ALL if float(InstitutionTrans) > 0 else Fore.RED + Style.BRIGHT + f'%Institution Transactions: {InstitutionTrans} (>0, >5)' + Style.RESET_ALL)


		#we define different figures for each chart and then place them in different parts of the screen
		plt.figure(1)
		RBchart(Ticker, columnNames, Buy, Overweight, Hold, Underweight, Sell)
		plt.figure(2)
		REchart(Ticker, RevenuePast5, NetIncomePast5, soup2, soup1)
		plt.figure(3)
		PTchart(Ticker, Price, HighTarget, LowTarget, AverageTarget, NumberOfRatings)

		plt.show()


if __name__ == '__main__': main() 