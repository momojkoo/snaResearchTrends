# Python 3
#
# myNetworkAnalysis.py - korean
# created by Jasuk Koo, June 15, 2020
#
#    -make node, edge list

import sys
import re
import numpy as np

#---------------------------------
def readData(filename):
	try:
		f=open(filename, "r", encoding="UTF8")
		# f=open(filename, "r", encoding="euc-kr")
	except IOError:
		print('Error : File not found')
		sys.exit()
	else:
		with f:
				data=f.readlines()
	return data
	
def getPair(lines):
	pair=[]
	for line in lines:
		[k, valueline] = re.split('\|', line.strip())
		values = re.split('[\,]', valueline)
		for v in values:
			vv = v.strip()
			if vv == "" : continue
			vv = vv.lower()
			vv = vv.replace(" ", "_")
			pair.append([k.strip(), vv])
	return pair
	
def getColList(pair, noCol):
	return list(sorted(set([e[noCol] for e in pair])))
	
def getAdjMatrix(pair, rList, cList):
	rSize = len(rList)
	cSize = len(cList)
	# make an empty adjacency list
	adjMatrix = np.zeros((rSize, cSize), dtype=int)
	for x, y in pair:
		adjMatrix[rList.index(x)][cList.index(y)] += 1
	return adjMatrix
	
def getAutoRelation(adjMatrix, type='x'):
	if type.lower() == 'x' : # x->x
		auto = np.dot(adjMatrix, np.transpose(adjMatrix))
		np.fill_diagonal(auto, 0)
	else: # y->y
		auto = np.dot(np.transpose(adjMatrix), adjMatrix)
		np.fill_diagonal(auto, 0)
	return auto
	
def getPairFromMatrix(autoRelation, cList=None):
	autoPair = []
	i = 0
	for e in autoRelation:
		j = 0
		for n in e:
			if(autoRelation[i][j] != 0 ):
				if(cList == None):
					autoPair.append([i, j, autoRelation[i][j]])
				else:
					autoPair.append([cList[i], cList[j], autoRelation[i][j]])
			j += 1
		i += 1
	return autoPair
	
def writeTGF(rList, cList, pair, filename):
# TGF file for yED graph
	try:
		f=open(filename, "w")
	except IOError:
		print('Error : Can not make file %s'%filename)
		sys.exit()
	else:
		with f:
			for x in rList:
				f.write("%s\n"%(x))
			for x in cList:
				f.write("%s\n"%(x))
			f.write("#\n")
			for x in pair:
				if len(x) == 2:
					f.write("%s %s\n"%(x[0], x[1]))
				elif len(x) == 3:
					f.write("%s %s %s\n"%(x[0], x[1], x[2]))
				else:
					print("check your input")
					sys.exit()
					
def writeTGFedges(pair, filename):
# TGF file for yED graph
	try:
		f=open(filename, "w", encoding="UTF8")
	except IOError:
		print('Error : Can not make file %s'%filename)
		sys.exit()
	else:
		with f:
			f.write("#\n")
			for x in pair:
				if len(x) == 2:
					f.write("%s %s\n"%(x[0], x[1]))
				elif len(x) == 3:
					f.write("%s %s %s\n"%(x[0], x[1], x[2]))
				else:
					print("check your input")
					sys.exit()
					
def writeNodeList(nodeList, filename):
	try:
		f=open(filename, "w", encoding="UTF8")
	except IOError:
		print('Error : Can not make file %s'%filename)
		sys.exit()
	else:
		with f:
			f.write("node\n"%(x))
			for x in nodeList:
				f.write("%s\n"%(x))
				
def writeEdgeList(edgeList, filename):
	try:
		f=open(filename, "w", encoding="UTF8")
	except IOError:
		print('Error : Can not make file %s'%filename)
		sys.exit()
	else:
		with f:
			f.write("source, target, weight\n")
			for [x, y, w] in edgeList:
				f.write("%s, %s, %s\n"%(x, y, str(w)))
				
def printUsage():
	print("Usage : myNetworkAnalysis inputfile")
	print("\n==input file format==\nkey | item, item, item\nkey | item, item\n...\n")
	
def main():
	# read data
	if len(sys.argv) < 2 or len(sys.argv) >2 :
		printUsage()
		sys.exit(1)
	filename = sys.argv[1]
	
	#0. read input_str
	print("0. Read input str")
	input_str = readData(filename)
	#print(input_str)
	
	#1. get pair
	print("1. get pair")
	pair=getPair(input_str)
	print(pair)
	#
	print("1.1. write to TGF (edges only)")
	writeTGFedges(pair, "0_Edges.tgf")
	
	#2. get node list
	print("2. get node list")
	rList = getColList(pair, 0)
	print(rList)
	cList = getColList(pair, 1)
	print(cList)
	
	#3. get adjacency matrix
	print("3. get adjacency matrix")
	adjMatrix = getAdjMatrix(pair, rList, cList)
	print(adjMatrix)
	
	#4. get AutoList(x)
	print("4. get autoList -- A")
	# x to x
	autoRelationX = getAutoRelation(adjMatrix, "x")
	print(autoRelationX)
	autoListX = getPairFromMatrix(autoRelationX, rList)
	print(autoListX)
	# for yED
	writeTGFedges(autoListX, "0_Edges_A.tgf")
	# for gephi
	writeEdgeList(autoListX, "1_Edges_A.csv")
	
	#5. get AutoLIst(y)
	print("5. get autoList --B")
	# y to y
	autoRelationY = getAutoRelation(adjMatrix, "y")
	print(autoRelationY)
	autoListY = getPairFromMatrix(autoRelationY, cList)
	print(autoListY)
	# for yED
	writeTGFedges(autoListY, "0_Edges_B.tgf")
	# for gephi
	writeEdgeList(autoListY, "1_Edges_B.csv")
	
	print("== The End")
	
if __name__ == "__main__":
	sys.exit(main())
	