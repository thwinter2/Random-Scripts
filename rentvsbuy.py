import numpy

class RentedHouse:
	def __init__(self, monthly_rent, pet_fee, pet_rate, rent_inflation_rate,months):
		self.monthly_rent = monthly_rent
		self.pet_fee = pet_fee
		self.pet_rate = pet_rate
		self.monthly_renters_insurance = 90.00/12 #Used $90 for typical yearly Trisure renters insurance
		self.months = months
		self.rent_inflation_rate = rent_inflation_rate/100

	def buildMonthlyPaymentsArray(self):
		monthly_payments = []
		for year in range((self.months-1)//12+1):
			monthly_payments.append(self.getCurrentMonthlyRent(year*12))
		return monthly_payments

	def getCurrentMonthlyRent(self,months):
		year = months//12
		return self.monthly_rent*(1+self.rent_inflation_rate)**year +self.pet_rate + self.monthly_renters_insurance

	def calculateAverageMonthlyPayment(self):
		average_monthly_payments = numpy.array(self.buildMonthlyPaymentsArray())
		return numpy.average(average_monthly_payments)

	def calculateOverallCost(self):
		return sum(self.buildMonthlyPaymentsArray())*12+self.pet_fee

class OwnedHouse:
	def __init__(self, value_of_house, down_payment, rate, length_of_loan, appreciation_APY, property_tax_rate,
	home_insurance_rate, monthly_hoa_fees, yearly_home_repairs, additional_principle, months):
		self.value_of_house = value_of_house
		if down_payment <= 1:
			self.down_payment = value_of_house*float(down_payment)
		else:
			self.down_payment = float(down_payment)
		self.rate = rate/1200 #divided by 12 months and 100%
		self.length_of_loan = length_of_loan*12 #convert length of loan to in terms of months
		if months < 0:
			self.months = 0
		else:
			self.months = months
		self.appreciation_rate = (appreciation_APY/100+1)**(1.0/12.0)
		self.property_tax_rate = property_tax_rate/1200 #divided by 12 months and 100%
		self.home_insurance_rate = home_insurance_rate/1200 #divided by 12 months and 100%
		self.monthly_hoa_fees = monthly_hoa_fees
		self.monthly_home_repairs = yearly_home_repairs/12
		self.additional_principle = additional_principle

	def getAppreciationRate(self):
		return self.appreciation_rate

	def buildMonthlyLoanAmountHash(self, months):
		loan_amount = self.value_of_house - self.down_payment
		minimum_monthly_payment = self.calculateMinimumMonthlyPrinciplePayment()
		loan_payments = [{'Interest Payment' : 0, 'Principle Payment' : 0, 'Loan Amount Remaining' : loan_amount}]
		for month in range(1,months):
			interest_payment = loan_payments[month-1]['Loan Amount Remaining']*self.rate
			principle_payment = minimum_monthly_payment + self.additional_principle - interest_payment
			loan_amount = loan_payments[month-1]['Loan Amount Remaining'] - principle_payment
			loan_payments.append({'Interest Payment' : interest_payment, 'Principle Payment' : principle_payment, 'Loan Amount Remaining' : loan_amount})
			if loan_amount < 0:
				break
		return loan_payments

	def buildMonthlyPaymentsArray(self,months):
		loan_payments = self.buildMonthlyLoanAmountHash(months)
		minimum_monthly_payment = self.calculateMinimumMonthlyPrinciplePayment()
		monthly_payments = [0]
		PMI = self.calculateMonthlyPMI()
		if PMI > 0:
			last_month_of_PMI = self.findLastMonthOfPMI()
		for month in range(1,months):
			home_value = self.calculateHomeValueAppreciation(month)
			if PMI > 0 and month > last_month_of_PMI:
				PMI = 0
			monthly_payments.append(home_value*(self.property_tax_rate+self.home_insurance_rate) + PMI + self.monthly_hoa_fees + self.monthly_home_repairs)
			if self.additional_principle <= 0:
				monthly_payments[month] += minimum_monthly_payment
			else:
				try:
					monthly_payments[month] += loan_payments[month]['Interest Payment'] + loan_payments[month]['Principle Payment']
				except IndexError:
					pass
		return monthly_payments

	def calculateHomeValueAppreciation(self, months):
		return self.value_of_house*self.appreciation_rate**months

	def calculateMinimumMonthlyPrinciplePayment(self):
		principle = self.value_of_house-self.down_payment
		return principle*(self.rate*(1+self.rate)**self.length_of_loan)/((1+self.rate)**self.length_of_loan-1)

	def calculateMonthlyPMI(self):
		if self.down_payment/float(self.value_of_house) < 0.2:
			return self.value_of_house/self.length_of_loan*0.01
		else:
			return 0

	def findLastMonthOfPMI(self):
		loan_payments = self.buildMonthlyLoanAmountHash(self.months)
		for month in range(self.months+1):
			if loan_payments[month]['Loan Amount Remaining']/self.value_of_house <= 0.80:
				return month
			return self.months

	def calculateHomeEquity(self, months):
		loan_remaining = self.buildMonthlyLoanAmountHash(months)[-1]['Loan Amount Remaining']
		if loan_remaining < 0:
			loan_remaining = 0
		return self.calculateHomeValueAppreciation(months) - loan_remaining

	def calculateTotalCost(self):
		equity = self.calculateHomeEquity(self.months)
		buying_closing_costs = self.value_of_house*0.04 #initial value of house times 4% closing cost
		selling_closing_costs = self.calculateHomeValueAppreciation(self.months)*0.06 #final value of house times 6% closing cost
		#add down payment only to cancel it out being subtracted from total cost when calculating the equity. Down payment should not be considered a gain or loss
		return sum(self.buildMonthlyPaymentsArray(self.months)) + buying_closing_costs + selling_closing_costs - equity + self.down_payment 

	def calculateAverageMonthlyPayment(self):
		average_monthly_payments = numpy.array(self.buildMonthlyPaymentsArray(self.months))
		return numpy.average(average_monthly_payments)


months = 24

house_value = 200000
down_payment = 40000
mortgage_rate = 3.625
years_of_mortgage = 30
appreciation_APY = 5.0
property_tax_rate = 1.0
home_insurance_rate = 0.5
monthly_hoa_fees = 0
yearly_home_repairs = house_value*0.01
additional_principle = 1000

monthly_rent = 1000
pet_fee = 200
pet_rate = 15
yearly_rent_inflation_rate = 5.0

buy_house = OwnedHouse(house_value,down_payment,mortgage_rate,years_of_mortgage,appreciation_APY,property_tax_rate,
	home_insurance_rate,monthly_hoa_fees,yearly_home_repairs,additional_principle,months)
buy_overall_cost = buy_house.calculateTotalCost()
rent_house = RentedHouse(monthly_rent,pet_fee,pet_rate,yearly_rent_inflation_rate,months)
rent_monthly_payment = rent_house.calculateAverageMonthlyPayment()
rent_overall_cost = rent_house.calculateOverallCost()

#print('Appreciated value of owned house is '+str(buy_house.calculateHomeValueAppreciation(months)))
print("Average Monthly Payment of buying a $"+"{:,}".format(house_value)+
	" house with a $"+"{:,}".format(down_payment)+
	" down payment is $"+"{:,.2f}".format(buy_house.calculateAverageMonthlyPayment()))

print("Monthly Payment of renting is $"+"{:,.2f}".format(rent_monthly_payment))

print("Over the course of "+str(months)+
	" months, the cost of buying a home is $"+"{:,.2f}".format(buy_overall_cost)+
	" and the cost of renting a home is $"+"{:,.2f}".format(rent_overall_cost))

if rent_overall_cost <= buy_overall_cost:
	difference = buy_overall_cost - rent_overall_cost
	print("Renting will save you $"+"{:,.2f}".format(difference))
else:
	difference = rent_overall_cost - buy_overall_cost
	print("Buying will save you $"+"{:,.2f}".format(difference))
