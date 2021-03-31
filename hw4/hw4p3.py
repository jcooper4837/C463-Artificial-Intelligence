#Cooper Martin
#C463 HW4 Part 3
#3/20/2021

import math
import random

class Regression:
    #this class uses standard regression without gradient descent
    def __init__(self,size,y,x1,x2):
        self.size = size #number of data elements
        self.y = y #array of y values
        self.x1 = x1 #array of x1 values
        self.x2 = x2 #array of x2 values
        self.x1y = self.multiplyArrays(self.x1,self.y) #array of x1*y values
        self.x2y = self.multiplyArrays(self.x2,self.y) #array of x2*y values
        self.x1x2 = self.multiplyArrays(self.x1,self.x2) #array of x1*x2 values
        self.ySum = self.getSum(self.y) #sum of all respective values
        self.x1Sum = self.getSum(self.x1)
        self.x2Sum = self.getSum(self.x2)
        self.x1ySum = self.getSum(self.x1y)
        self.x2ySum = self.getSum(self.x2y)
        self.x1x2Sum = self.getSum(self.x1x2)
        self.yMean = self.getMean(self.ySum) #mean of all respective values
        self.x1Mean = self.getMean(self.x1Sum)
        self.x2Mean = self.getMean(self.x2Sum)
        self.yUSS = self.getSumOfSquares(self.y,self.yMean) #sum of squares of all respective values
        self.x1USS = self.getSumOfSquares(self.x1,self.x1Mean)
        self.x2USS = self.getSumOfSquares(self.x2,self.x2Mean)
        self.x1yLower = self.getLower(self.x1ySum,self.x1Sum,self.ySum) #used for coefficient calculation
        self.x2yLower = self.getLower(self.x2ySum,self.x2Sum,self.ySum)
        self.x1x2Lower = self.getLower(self.x1x2Sum,self.x1Sum,self.x2Sum)
        self.b1 = self.getCoefficient(self.x2USS,self.x1yLower,self.x1x2Lower,self.x2yLower,self.x1USS) #coefficients
        self.b2 = self.getCoefficient(self.x1USS,self.x2yLower,self.x1x2Lower,self.x1yLower,self.x2USS)
        self.a = self.getIntercept(self.yMean,self.b1,self.x1Mean,self.b2,self.x2Mean) #intercept
        self.t1 = -1 #test values, used later
        self.t2 = -1

    def setTest(self,t1,t2):
        #set values to be tested
        self.t1 = t1
        self.t2 = t2

    def multiplyArrays(self,a,b):
        #multiply 2 arrays and return array containing product
        res = []
        for i in range(self.size):
            res.append(a[i] * b[i])
        return res

    def getSum(self,arr):
        #sum 2 arrays and return array containing sum
        res = 0
        for i in range(self.size):
            res = res + arr[i]
        return res

    def getMean(self,summation):
        #return an average
        return summation / self.size

    def getSumOfSquares(self,arr,mean):
        #get the sum of all squares in an array
        res = 0
        for i in range(self.size):
            res = res + math.pow(arr[i] - mean,2)
        return res

    def getLower(self,a,b,c):
        #calculate values used to find coefficients
        return a - (b * c / self.size)

    def getCoefficient(self,a,b,c,d,e):
        #calculate the coefficients
        return (a * b - c * d) / (e * a - math.pow(c,2))

    def getIntercept(self,y,b1,x1,b2,x2):
        #get the y-intercept
        return y - b1 * x1 - b2 * x2

    def testInput(self):
        #plug in test values into regression formula
        return self.a + self.b1 * self.t1 + self.b2 * self.t2

class GradientDescent:
    #this class utilizes gradient descent for regression
    def __init__(self,size,y,x1,x2):
        self.size = size #number of data elements
        self.y = y #array of y values
        self.x1 = x1 #array of x1 values
        self.x2 = x2 #array of x2 values
        self.yMax = self.getMaximum(self.y) #get maximum value in respective array
        self.x1Max = self.getMaximum(self.x1)
        self.x2Max = self.getMaximum(self.x2)
        self.yMin = self.getMinimum(self.y) #get minimum value in respective array
        self.x1Min = self.getMinimum(self.x1)
        self.x2Min = self.getMinimum(self.x2)
        self.yNormal = self.getNormalized(self.y,self.yMax,self.yMin) #get normalized value in respective array
        self.x1Normal = self.getNormalized(self.x1,self.x1Max,self.x1Min)
        self.x2Normal = self.getNormalized(self.x2,self.x2Max,self.x2Min)
        self.a = random.random() #initialize random number between 0 and 1
        self.b1 = random.random()
        self.b2 = random.random()
        self.yp = self.getYP() #get y prediction value
        self.sse = self.getSSE() #get sum of squares error
        self.da = self.getDerivative(-1) #get derivative of respective variables
        self.db1 = self.getDerivative(self.x1Normal)
        self.db2 = self.getDerivative(self.x2Normal)
        self.sseSum = self.getSum(self.sse) #get sum of sum of squares error
        self.daSum = self.getSum(self.da) #get sum of respective derivatives
        self.db1Sum = self.getSum(self.db1)
        self.db2Sum = self.getSum(self.db2)
        self.t1 = -1 #test values, used later
        self.t2 = -1

    def setTest(self,t1,t2):
        #set values to be tested
        self.t1 = t1
        self.t2 = t2

    def getMaximum(self,arr):
        #find and return the maximum value of an array
        res = arr[0]
        for i in range(self.size):
            if arr[i] > res:
                res = arr[i]
        return res

    def getMinimum(self,arr):
        #find and return the minimum value of an array
        res = arr[0]
        for i in range(self.size):
            if arr[i] < res:
                res = arr[i]
        return res

    def getNormalized(self,arr,maxi,mini):
        #normalize all values in an array for ease in calculations
        res = []
        for i in range(self.size):
            res.append((arr[i] - mini) / (maxi - mini))
        return res

    def getYP(self):
        #get all y prediction values in an array
        res = []
        for i in range(self.size):
            res.append(self.a + self.b1 * self.x1Normal[i] + self.b2 * self.x2Normal[i])
        return res

    def getSSE(self):
        #get all sum of squares errors in an array
        res = []
        for i in range(self.size):
            res.append(0.5 * math.pow(self.yNormal[i] - self.yp[i],2))
        return res

    def getDerivative(self,arr):
        #get all derivates in an array
        res = []
        for i in range(self.size):
            if arr != -1: #case for b values
                res.append(-(self.yNormal[i] - self.yp[i]) * arr[i])
            else: #case for a values
                res.append(-(self.yNormal[i] - self.yp[i]))
        return res

    def getSum(self,arr):
        #sum 2 arrays and return array containing sum
        res = 0
        for i in range(self.size):
            res = res + arr[i]
        return res

    def testInput(self):
        #plug in test values into regression formula and return denormalized y prediction value
        x1Normal = (self.t1 - self.x1Min) / (self.x1Max - self.x1Min)
        x2Normal = (self.t2 - self.x2Min) / (self.x2Max - self.x2Min)
        ypNormal = self.a + self.b1 * x1Normal + self.b2 * x2Normal
        yp = ypNormal * (self.yMax - self.yMin) + self.yMin
        return yp

    def GD(self,epochs,rate):
        #gradient descent algorithm: itarate through a and b values to minimize sse sum
        aNext = self.a - (rate * self.daSum) #first iteration values to try next
        b1Next = self.b1 - (rate * self.db1Sum)
        b2Next = self.b2 - (rate * self.db2Sum)
        for i in range(epochs): #ideally loop until sse reduction is negligible
            self.a = aNext #set next values
            self.b1 = b1Next
            self.b2 = b2Next
            self.yp = self.getYP() #perform same calculations from init function with new a and b values
            self.sse = self.getSSE()
            self.da = self.getDerivative(-1)
            self.db1 = self.getDerivative(self.x1Normal)
            self.db2 = self.getDerivative(self.x2Normal)
            self.sseSum = self.getSum(self.sse)
            self.daSum = self.getSum(self.da)
            self.db1Sum = self.getSum(self.db1)
            self.db2Sum = self.getSum(self.db2)
            aNext = self.a - (rate * self.daSum) #calculate new a and b values based on rate
            b1Next = self.b1 - (rate * self.db1Sum)
            b2Next = self.b2 - (rate * self.db2Sum)
            if (i + 1) % 100  == 0: #optional print statement to demonstrate algorithm progress
                print("After",i+1,"iterations: a = {:0.3f}".format(self.a),"|| b1 = {:0.3f}".format(self.b1),"|| b2 = {:0.3f}".format(self.b2),"|| SSE = {:0.3f}".format(self.sseSum))

def parseFile(name,y,x1,x2):
    f = open(name,"r")
    size = int(f.readline()) #first value is size
    for i in range(size): #y values
        y.append(float(f.readline()))
    for i in range(size): #x1 values
        x1.append(float(f.readline()))
    for i in range(size): #x2 values
        x2.append(float(f.readline()))
    return size

def main():
    y,x1,x2 = [],[],[]
    size = parseFile("acs2015.txt",y,x1,x2) #read data in custom formatted text file for ease
    case = Regression(size,y,x1,x2) #standard regression case, no gradient descent
    print("Standard regression function: Y = {:0.3f}".format(case.a),"+ X1 * {:0.3f}".format(case.b1),"+ X2 * {:0.3f}".format(case.b2))
    case2 = GradientDescent(size,y,x1,x2) #regression + gradient descent case
    print("Now linear regression utilizing gradient descent")
    print("Starting Values: a = {:0.3f}".format(case2.a),"|| b1 = {:0.3f}".format(case2.b1),"|| b2 = {:0.3f}".format(case2.b2),"|| SSE = {:0.3f}".format(case2.sseSum))
    case2.GD(1000,0.0005) #1000 iterations, 0.00005 reduction rate. both can be changed
    while True:
        test1 = eval(input("Enter value for IncomePerCap (enter -1 to quit):"))
        if test1 == -1:
            break
        test2 = eval(input("Enter value for Unemployment (enter -1 to quit):"))
        if test2 == -1:
            break
        case.setTest(test1,test2)
        print("Predicted value for ChildPoverty using standard regression: {:0.6f}".format(case.testInput()))
        case2.setTest(test1,test2)
        print("Predicted value for ChildPoverty using gradient descent: {:0.6f}".format(case2.testInput()))

main()
