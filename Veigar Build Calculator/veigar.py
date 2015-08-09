# Anthony Kuntz
# Veigar build and damage calculator with UI


# Returns the burst damage of a build given certain limitations and stats
def calculateVeigar(itemList, level, bonusAP, neededCDR, neededMS, enemyMR, enemyAP, numberOfItems, runesList):

	mana = 342.4 + 55 * level
	AP = 0.89 * level + 6 + bonusAP
	CDR = 5
	flatPen = 0
	perPen = 6
	MS = 340

	if runesList != None:
		AP += int(runesList[0]) if runesList[0] != "" else 0
		CDR += int(runesList[1]) if runesList[1] != "" else 0
		flatPen += int(runesList[2]) if runesList[2] != "" else 0
		perPen += int(runesList[3]) if runesList[3] != "" else 0

	masteryMS = 1
	masteryAP = 1.05

	arcaneBlade = .05

	for item in itemList:
		try: AP += item["AP"]
		except: pass

		try: CDR += item["CDR"]
		except: pass

		try: mana += item["mana"]
		except: pass

		try: flatPen += item["mPen"] if item["Name"] == "Sorcs" else 0
		except: pass

		try: 
			if not alreadyAppliedBoots:
				MS += item["MS"] if type(item["MS"]) == int else 0
				if item == sorcs: alreadyAppliedBoots = True
		except: pass

		try: MS *= (1 + item["MS"] / 100.0) if type(item["MS"]) == float else 1
		except: pass

	# Try and pass used incase the stat is not included in the dictionary

	if CDR < neededCDR: return 0
	if MS < neededMS: return 0

	if liandries in itemList: flatPen += 15
	if voidstaff in itemList: perPen += 35


	AP *= masteryAP
	if deathcap in itemList: AP *= 1.35
	if aaa in itemList: AP += mana * .03

	qDmg = 80
	if level > 3:
		qDmg = 125
		if level > 4:
			qDmg = 170
			if level > 6:
				qDmg = 215
				if level > 8:
					qDmg = 260

	# Veigar's Q dmg assuming that it is maxed first

	qDmg += AP * .60

	wDmg = 0
	if level > 3:
		wDmg = 120
		if level > 11:
			wDmg = 170
			if level > 12:
				wDmg = 220
				if level > 13:
					wDmg = 270
					if level > 14:
						wDmg = 320

	# W damage assuming W is maxed after reaching 3 levels in E

	wDmg += AP

	rDmg = 0
	if level > 5:
		rDmg = 250
		if level > 10:
			rDmg = 375
			if level > 15:
				rDmg += 500

	rDmg += AP
	rDmg += enemyAP * .80

	basicDmg = AP * arcaneBlade
	if lichbane in itemList: basicDmg += AP * .50
	if nashors in itemList: basicDmg += 15 + AP * .15

	rawDmg = qDmg + wDmg + rDmg + basicDmg

	if ludens in itemList: rawDmg += 100 + AP * .10

	enemyMR -= enemyMR * ( perPen / 100.0 )
	enemyMR -= flatPen
	if enemyMR < 0: enemyMR = 0

	realDmg = rawDmg * (100.0 / (100 + enemyMR))

	return realDmg


# Dictionaries for every item included thus far
voidstaff = { "AP" : 80, "CDR" : 0, "mana" : 0, "mPen" : 35.0, "MS" : 0, "Name" : "Void Staff"}
abyssal = { "AP" : 70, "CDR" : 0, "mana" : 0, "mPen" : 20, "MS" : 0, "Name" : "Abyssal"}
liandries = { "AP" : 80, "CDR" : 0, "mana" : 0, "mPen" : 15, "MS" : 0, "Name" : "Liandries"}
ludens = { "AP" : 100, "CDR" : 0, "mana" : 0, "mPen" : 0, "MS" : 10.0, "Name" : "Ludens"}
deathcap = { "AP" : 120, "CDR" : 0, "mana" : 0, "mPen" : 0, "MS" : 0, "Name" : "Deathcap"}
roa = { "AP" : 100, "CDR" : 0, "mana" : 800, "mPen" : 0, "MS" : 0, "Name" : "ROA"}
athenes = { "AP" : 60, "CDR" : 20, "mana" : 0, "mPen" : 0, "MS" : 0, "Name" : "Athenes"}
lichbane = { "AP" : 80, "CDR" : 0, "mana" : 250, "mPen" : 0, "MS" : 5.0, "Name" : "Lich Bane"}
nashors = { "AP" : 80, "CDR" : 20, "mana" : 0, "mPen" : 0, "MS" : 0, "Name" : "Nashors"}
wota = { "AP" : 80, "CDR" : 10, "mana" : 0, "mPen" : 0, "MS" : 0, "Name" : "WOTA"}
twinshadows = { "AP" :80 , "CDR" : 10, "mana" : 0, "mPen" : 0, "MS" : 6.0, "Name" : "Twin Shadows"}
morello = { "AP" : 80, "CDR" : 20, "mana" : 0, "mPen" : 0, "MS" : 0, "Name" : "Morello"}
aaa = { "AP" : 80, "CDR" : 0, "mana" : 1000, "mPen" : 0, "MS" : 0, "Name" : "AAA"}
zhonyas = { "AP" : 100, "CDR" : 0, "mana" : 0, "mPen" : 0, "MS" : 0, "Name" : "Zhonyas"}
sorcs = { "AP" : 0, "CDR" : 0, "mana" : 0, "mPen" : 15, "MS" : 45, "Name" : "Sorcs"}


# Brute forces the best build given an amount of items and stats
def bestVeigar(level, bonusAP, neededCDR, neededMS, enemyMR, enemyAP, numberOfItems, requiredItems, runesList):

	allItems = [voidstaff, abyssal, lichbane, 
			liandries, ludens, deathcap, 
			roa, nashors, twinshadows, morello,
			aaa, sorcs, athenes, zhonyas, wota]

	bestBuild = []
	bestDmg = 0

	if numberOfItems == 6:
		for a in allItems:
			for b in allItems:
				for c in allItems:
					for d in allItems:
						for e in allItems:
							for f in allItems:
								flag = True
								itemList = [a, b, c, d, e, f]
								for item in requiredItems:
									if item not in itemList:
										flag = False
								if flag == False: continue
								dmg = calculateVeigar(itemList, level, bonusAP, neededCDR, neededMS, enemyMR, enemyAP, numberOfItems, runesList)
								if dmg > bestDmg: 
									bestDmg = dmg
									bestBuild = itemList
	elif numberOfItems == 5:
		for a in allItems:
			for b in allItems:
				for c in allItems:
					for d in allItems:
						for e in allItems:
								flag = True
								itemList = [a, b, c, d, e]
								for item in requiredItems:
									if item not in itemList:
										flag = False
								if flag == False: continue
								dmg = calculateVeigar(itemList, level, bonusAP, neededCDR, neededMS, enemyMR, enemyAP, numberOfItems, runesList)
								if dmg > bestDmg: 
									bestDmg = dmg
									bestBuild = itemList

	elif numberOfItems == 4:
		for a in allItems:
			for b in allItems:
				for c in allItems:
					for d in allItems:
								flag = True
								itemList = [a, b, c, d]
								for item in requiredItems:
									if item not in itemList:
										flag = False
								if flag == False: continue
								dmg = calculateVeigar(itemList, level, bonusAP, neededCDR, neededMS, enemyMR, enemyAP, numberOfItems, runesList)
								if dmg > bestDmg: 
									bestDmg = dmg
									bestBuild = itemList

	elif numberOfItems == 3:
		for a in allItems:
			for b in allItems:
				for c in allItems:
								flag = True
								itemList = [a, b, c]
								for item in requiredItems:
									if item not in itemList:
										flag = False
								if flag == False: continue
								dmg = calculateVeigar(itemList, level, bonusAP, neededCDR, neededMS, enemyMR, enemyAP, numberOfItems, runesList)
								if dmg > bestDmg: 
									bestDmg = dmg
									bestBuild = itemList

	elif numberOfItems == 2:
		for a in allItems:
			for b in allItems:
								flag = True
								itemList = [a, b]
								for item in requiredItems:
									if item not in itemList:
										flag = False
								if flag == False: continue
								dmg = calculateVeigar(itemList, level, bonusAP, neededCDR, neededMS, enemyMR, enemyAP, numberOfItems, runesList)
								if dmg > bestDmg: 
									bestDmg = dmg
									bestBuild = itemList

	elif numberOfItems == 1:
		for a in allItems:
								flag = True
								itemList = [a]
								for item in requiredItems:
									if item not in itemList:
										flag = False
								if flag == False: continue
								dmg = calculateVeigar(itemList, level, bonusAP, neededCDR, neededMS, enemyMR, enemyAP, numberOfItems, runesList)
								if dmg > bestDmg: 
									bestDmg = dmg
									bestBuild = itemList


	return bestBuild, bestDmg

from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import os

# Buttons for stats
class MyDialog2(tkSimpleDialog.Dialog):
	def body(self, master):
		canvas.modalResult = None
		Label(master, text="Level:").grid(row=0)
		Label(master, text="Q Stacks:").grid(row=1)
		Label(master, text="Required CDR:").grid(row=2)
		Label(master, text="Required MS:").grid(row=3)
		Label(master, text="Enemy MR:").grid(row=4)
		Label(master, text="Enemy AP").grid(row=5)
		Label(master, text="Number of Items:").grid(row=6)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e3 = Entry(master)
		self.e4 = Entry(master)
		self.e5 = Entry(master)
		self.e6 = Entry(master)
		self.e7 = Entry(master)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		self.e3.grid(row=2, column=1)
		self.e4.grid(row=3, column=1)
		self.e5.grid(row=4, column=1)
		self.e6.grid(row=5, column=1)
		self.e7.grid(row=6, column=1)
		return self.e1 # initial focus
	def apply(self):
		first = self.e1.get()
		second = self.e2.get()
		third = self.e3.get()
		fourth = self.e4.get()
		fifth = self.e5.get()
		sixth = self.e6.get()
		seventh = self.e7.get()
		global canvas
		canvas.modalResult2 = (first, second, third, fourth, fifth, sixth, seventh)

# Buttons for required items
class MyDialog(tkSimpleDialog.Dialog):
	def body(self, master):
		canvas.modalResult = None
		Label(master, text="Required Item:").grid(row=0)
		Label(master, text="Required Item:").grid(row=1)
		Label(master, text="Required Item:").grid(row=2)
		Label(master, text="Required Item:").grid(row=3)
		Label(master, text="Required Item:").grid(row=4)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e3 = Entry(master)
		self.e4 = Entry(master)
		self.e5 = Entry(master)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		self.e3.grid(row=2, column=1)
		self.e4.grid(row=3, column=1)
		self.e5.grid(row=4, column=1)
		return self.e1 # initial focus
	def apply(self):
		first = self.e1.get()
		second = self.e2.get()
		third = self.e3.get()
		fourth = self.e4.get()
		fifth = self.e5.get()
		global canvas
		canvas.modalResult = (first, second, third, fourth, fifth)

# Button for runes
class MyDialog3(tkSimpleDialog.Dialog):
	def body(self, master):
		canvas.modalResult = None
		Label(master, text="AP from Runes:").grid(row=0)
		Label(master, text="CDR from Runes:").grid(row=1)
		Label(master, text="Flat Pen from Runes:").grid(row=2)
		Label(master, text="Percent Pen from Runes:").grid(row=3)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e3 = Entry(master)
		self.e4 = Entry(master)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		self.e3.grid(row=2, column=1)
		self.e4.grid(row=3, column=1)
		return self.e1 # initial focus
	def apply(self):
		first = self.e1.get()
		second = self.e2.get()
		third = self.e3.get()
		fourth = self.e4.get()
		global canvas
		canvas.modalResult3 = (first, second, third, fourth)

def showDialog3(canvas):
	MyDialog3(canvas)
	return canvas.modalResult3

def showDialog(canvas):
	MyDialog(canvas)
	return canvas.modalResult

def button1Pressed():
	global canvas
	message = str(showDialog(canvas))
	# And update and redraw our canvas
	canvas.message = message
	if canvas.message == "('', '', '', '', '')": canvas.message = "None"
	print canvas.message
	canvas.create_text(10, 175, text = "Required Items: " + canvas.message, fill = "white", anchor = W)

def buttonRunesPressed():
	global canvas
	canvas.runes = str(showDialog3(canvas))

def button0Pressed():
	global canvas
	canvas.stats = str(showDialog2(canvas))

def showDialog2(canvas):
	MyDialog2(canvas)
	return canvas.modalResult2
	

def button2Pressed():
	# Pressing the Calculate button executes the following
	global canvas
	requiredItems = []
	if canvas.runes != None:
		# Modify the list-formatted string into something readable
		canvas.runes = canvas.runes[1:-2]
		canvas.runes = canvas.runes.replace("'", "")
		canvas.runesList = canvas.runes.split(", ")
	if canvas.stats != None:
		# Modify the list-formatted string into something readable
		canvas.stats = canvas.stats[1:-2]
		canvas.stats = canvas.stats.replace("'", "")
		canvas.statsList = canvas.stats.split(", ")
	# Modify the list-formatted string into something readable
	canvas.message = canvas.message[1:-2]
	canvas.message = canvas.message.replace("'", "")
	canvas.list = canvas.message.split(", ")

	# Gather required items
	for itemName in canvas.list:
		for item in canvas.allItems:
			if item["Name"] == itemName:
				requiredItems.append(item)

	# Use stats if provided, else use the  following defaults
	try: level = int(canvas.statsList[0])
	except: level = 18
	try: qStacks = int(canvas.statsList[1])
	except: qStacks = 200
	try: neededCDR = int(canvas.statsList[2])
	except: neededCDR = 0
	try: neededMS = int(canvas.statsList[3])
	except: neededMS = 0
	try: enemyMR = int(canvas.statsList[4])
	except: enemyMR = 100
	try: enemyAP = int(canvas.statsList[5])
	except: enemyAP = 200
	try: numItems = int(canvas.statsList[6])
	except: numItems = 6

	# Return the best build and burst daamge
	build, dmg = bestVeigar(level, qStacks, neededCDR, neededMS, enemyMR, enemyAP, numItems, requiredItems, canvas.runesList)
	x = 30
	try: 
		canvas.p1 = PhotoImage( file = "Pictures" + os.sep + build[0]["Name"] + ".gif")
		canvas.create_image(x, 265, image = canvas.p1, anchor = W)
	except: pass
	x += 75
	try: 
		canvas.p2 = PhotoImage( file = "Pictures" + os.sep + build[1]["Name"] + ".gif")
		canvas.create_image(x, 265, image = canvas.p2, anchor = W)
	except: pass
	x += 75
	try: 
		canvas.p3 = PhotoImage( file = "Pictures" + os.sep + build[2]["Name"] + ".gif")
		canvas.create_image(x, 265, image = canvas.p3, anchor = W)
	except: pass
	x += 75
	try: 
		canvas.p4 = PhotoImage( file = "Pictures" + os.sep + build[3]["Name"] + ".gif")
		canvas.create_image(x, 265, image = canvas.p4, anchor = W)
	except: pass
	x += 75
	try: 
		canvas.p5 = PhotoImage( file = "Pictures" + os.sep + build[4]["Name"] + ".gif")
		canvas.create_image(x, 265, image = canvas.p5, anchor = W)
	except: pass
	x += 75
	try: 
		canvas.p6 = PhotoImage( file = "Pictures" + os.sep + build[5]["Name"] + ".gif")
		canvas.create_image(x, 265, image = canvas.p6, anchor = W)
	except: pass
	x += 75
	dmg = int(dmg)
	canvas.create_text(250, 310, text = "Damage Dealt with Full Combo: " + str(dmg), fill = "White", font = "Arial 15 bold")

	# Illustrate the build and display its damage ^

def init(root, canvas):
	initPix(canvas)
	canvas.stats = None
	canvas.runesList = None
	canvas.runes = None
	canvas.message = "None"
	canvas.allItems = [voidstaff, abyssal, lichbane, 
			liandries, ludens, deathcap, 
			roa, nashors, twinshadows, morello,
			aaa, sorcs, athenes, zhonyas, wota]

	buttonFrame = Frame(root)
	b1 = Button(buttonFrame, text="Set Required Items", command=button1Pressed)
	b1.grid(row=0,column=2)
	b2 = Button(buttonFrame, text="Calculate Build", command=button2Pressed)
	b2.grid(row=0,column=3)
	b0 = Button(buttonFrame, text="Set Level and Stats", command=button0Pressed)
	b0.grid(row=0,column=1)
	bR = Button(buttonFrame, text="Enter Runes", command= buttonRunesPressed)
	bR.grid(row=0,column=0)
	buttonFrame.pack(side=TOP)
	canvas.pack()

def main():
	global root
	root = Tk()
	global canvas
	canvas = Canvas(root, width = 500, height = 500, bg = "steel blue")
	canvas.pack()
	root.canvas = canvas.canvas = canvas
	root.bind("<Button-1>", onMousePressed)
	root.bind("<Key>", onKeyPressed)
	init(root, canvas)
	root.mainloop()

def onMousePressed(event):
	if isinstance(event.widget, Button): return
	canvas = event.widget.canvas

def onKeyPressed(event):
	canvas = event.widget.canvas
	if event.keysym == "r":
		canvas.message = ""
		canvas.stats = ""
		canvas.delete(ALL)
		initPix(canvas)

def initPix(canvas):
	# Used to redraw everything
	canvas.create_text(10,10, anchor = NW, 
		text = "Welcome to the Veigar Build Calculator! \nEnter info in the buttons below to begin.", fill = "white")
	canvas.create_text(10,50, anchor = NW, 
		text = "Please be patient when calculating. \nThe calculator can take up to 2 minutes.", fill = "white")
	canvas.create_text(10,350, anchor = NW, 
		text = "Finally, please realize that spelling matters. \n\nItem names must be spelled as follows: \
		\n\nAAA, Abyssal, Athenes, Deathcap, Liandries, Lich Bane, \
		\nLudens, Morello, Nashors, ROA, Sorcs, Twin Shadows, Void Staff", fill = "white")
	canvas.logo = PhotoImage( file = "Pictures" + os.sep + "logo.gif")
	canvas.create_image(510,-10, anchor = NE, image = canvas.logo)
	canvas.create_text(490,475, anchor = NE, 
		text = "Press r to restart.", fill = "white")

	


main() # Opens and executes UI