# Anthony Kuntz
# Kayle Damage and Build Calculator, with UI


# Returns the DPS of a specific build given certain limitations and stats
def calculateKayle(itemList, level, neededCDR, enemyMR, enemyArmor, enemyHP, numberOfItems, runesList):

	mana = 322.2 + 40 * level
	AP = 6 + 0.89 * level
	CDR = 5
	flatPen = 0 
	perPen = 12 + 6
	critChance = 0
	flatArmorPen = 0
	perArmorPen = 12 + 6
	AD = 56.004 + 2.8 * level
	AS = 0.638 * 1.022**level * 1.025

	if runesList != None:
		AP += int(runesList[0]) if runesList[0] != "" else 0
		CDR += int(runesList[1]) if runesList[1] != "" else 0
		flatPen += int(runesList[2]) if runesList[2] != "" else 0
		perPen += int(runesList[3]) if runesList[3] != "" else 0
		flatArmorPen += int(runesList[4]) if runesList[4] != "" else 0
		perArmorPen += int(runesList[5]) if runesList[5] != "" else 0
		AS *= ( 1 + int(runesList[6]) / 100.0) if runesList[6] != "" else 1
		AD += int(runesList[7]) if runesList[7] != "" else 0

	masteryAP = 1.05

	arcaneBlade = .05

	for item in itemList:
		try: AD += item["AD"]
		except: pass

		try: critChance += item["Crit"]
		except: pass

		try: AS *= (1 + item["AS"] / 100.0)
		except: pass

		try: AP += item["AP"]
		except: pass

		try: CDR += item["CDR"]
		except: pass

		try: mana += item["mana"]
		except: pass

		try: flatPen += item["mPen"] if item["Name"] == "Sorcs" else 0
		except: pass

	# Tries included incase stat is not in the dictionary


	if CDR < neededCDR: return 0


	if liandries in itemList: flatPen += 15
	if voidstaff in itemList: perPen += 35
	if lw in itemList: perArmorPen += 35
	if bc in itemList: perArmorPen += 15
	if youmuu in itemList: flatArmorPen += 20
	# Unique passives applied as such so that they don't double count


	AP *= masteryAP
	if deathcap in itemList: AP *= 1.35
	if aaa in itemList: AP += mana * .03

	eDmg = 20
	if level > 3:
		eDmg = 30
		if level > 4:
			eDmg = 40
			if level > 6:
				eDmg = 50
				if level > 8:
					eDmg = 60
	# Damage of Kayle's E assuming it is maxed first

	eDmg += AP * .30

	hasIE = ie in itemList
	critFactor = 2 + .5 * (hasIE)
	critChance /= 100.0

	if critChance > 1: critChance = 1
	if AS > 2.5: AS = 2.5
	# Stat caps

	pureAD = ((AD * critFactor * critChance) + (AD * (1 - critChance))) * AS

	purePhysOnHitDmg = enemyHP * .04 if botrk in itemList else 0
	pureMagOnHitDmg  = 42 if witsend in itemList else 0
	pureMagOnHitDmg += 60 if devourer in itemList else 0
	pureMagOnHitDmg += eDmg
	pureMagOnHitDmg += (15 + AP * 0.15) if nashors in itemList else 0
	pureMagOnHitDmg *= 1.5 if devourer in itemList else 1

	totalPureAD = pureAD + purePhysOnHitDmg * AS
	totalPureAP = ( pureMagOnHitDmg + (AP * arcaneBlade)) * AS

	enemyMR -= enemyMR * ( perPen / 100.0 )
	enemyMR -= flatPen
	enemyMR -= 15 if witsend in itemList else 0
	if enemyMR < 0: enemyMR = 0

	enemyArmor -= enemyArmor * ( perArmorPen / 100.0 )
	enemyArmor -= flatArmorPen
	if enemyArmor < 0: enemyArmor = 0

	redAD = round( totalPureAD * ( 100.0 / (100 + enemyArmor)) , 2 )
	redAP = round( totalPureAP * ( 100.0 / (100 + enemyMR)) , 2 )

	dps = redAP + redAD

	return dps



# Dictionaries for the stats of every item added thus far
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
zerks  	  = { "AS" : 25, "MS" : 45, "Bonus" : ["Better Hops"] , "Name" : "Zerks"}
ie 		  = { "AD" : 80, "Crit" : 20, "Bonus" : ["ieCrits"], "Name" : "IE"}
botrk	  = { "AD" : 25, "AS" : 40, "LS" : 10, "Bonus" : ["botrkDmg", "botrkActive"], "Name" : "BotRK"}
pd		  = { "AS" : 50, "Crit" : 35, "MS" : 5.0, "Bonus" : ["moveThrough"], "Name" : "PD"}
shiv 	  = { "AS" : 40, "Crit" : 20, "MS" : 6.0, "Bonus" : ["shivDmg"], "Name" : "Shiv"}
youmuu    = { "AD" : 30, "Crit" : 15, "aPen" : 20, "Bonus" : ["youmuuActive"], "Name" : "Youmuus"}
hurricane = { "AS" : 70, "Bonus" : ["bolts"], "Name" : "Hurricane"}
lw		  = { "AD" : 40, "aPen" : 35.0, "Name" : "LW"}
frozMal   = { "AD" : 30, "Bonus" : ["Slow"], "Name" : "Frozen Mallet"}
mercScim  = { "AD" : 80, "Bonus" : ["QSS"], "Name" : "Merc Scimitar"}
witsend = {"AS" : 50, "Name" : "Wits End"}
devourer = {"AS" : 50, "Name" : "Sated Devourer"}
essreav  = {"AD" : 80, "CDR" : 10, "Name" : "Essence Reaver"}
bc = {"AD" : 40, "CDR" : 10, "Name" : "BC"}



# Brute forces every possible build, returning the build with the highest DPS
def bestKayle(requiredItems, level, neededCDR, enemyMR, enemyArmor, enemyHP, numberOfItems, runesList):

	# Only viable items were included below
	allItems = [voidstaff, abyssal, 
			liandries, deathcap, nashors,
			aaa,
			ie, botrk, pd, youmuu,
			hurricane, lw,
			witsend, devourer, bc]

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
								dmg = calculateKayle(itemList, level, neededCDR, enemyMR, enemyArmor, enemyHP, numberOfItems, runesList)
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
								dmg = calculateKayle(itemList, level, neededCDR, enemyMR, enemyArmor, enemyHP, numberOfItems, runesList)
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
								dmg = calculateKayle(itemList, level, neededCDR, enemyMR, enemyArmor, enemyHP, numberOfItems, runesList)
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
								dmg = calculateKayle(itemList, level, neededCDR, enemyMR, enemyArmor, enemyHP, numberOfItems, runesList)
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
								dmg = calculateKayle(itemList, level, neededCDR, enemyMR, enemyArmor, enemyHP, numberOfItems, runesList)
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
								dmg = calculateKayle(itemList, level, neededCDR, enemyMR, enemyArmor, enemyHP, numberOfItems, runesList)
								if dmg > bestDmg: 
									bestDmg = dmg
									bestBuild = itemList


	return bestBuild, bestDmg

from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import os


# Buttons for Stats
class MyDialog2(tkSimpleDialog.Dialog):
	def body(self, master):
		canvas.modalResult = None
		Label(master, text="Level:").grid(row=0)
		Label(master, text="Required CDR:").grid(row=1)
		Label(master, text="Enemy Armor:").grid(row=2)
		Label(master, text="Enemy MR:").grid(row=3)
		Label(master, text="Enemy HP").grid(row=4)
		Label(master, text="Number of Items:").grid(row=5)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e3 = Entry(master)
		self.e4 = Entry(master)
		self.e5 = Entry(master)
		self.e6 = Entry(master)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		self.e3.grid(row=2, column=1)
		self.e4.grid(row=3, column=1)
		self.e5.grid(row=4, column=1)
		self.e6.grid(row=5, column=1)
		return self.e1 # initial focus
	def apply(self):
		first = self.e1.get()
		second = self.e2.get()
		third = self.e3.get()
		fourth = self.e4.get()
		fifth = self.e5.get()
		sixth = self.e6.get()
		global canvas
		canvas.modalResult2 = (first, second, third, fourth, fifth, sixth)

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

# Buttons for Runes
class MyDialog3(tkSimpleDialog.Dialog):
	def body(self, master):
		canvas.modalResult = None
		Label(master, text="AP from Runes:").grid(row=0)
		Label(master, text="CDR from Runes:").grid(row=1)
		Label(master, text="Flat Magic Pen from Runes:").grid(row=2)
		Label(master, text="Percent Magic Pen from Runes:").grid(row=3)
		Label(master, text="Flat Armor Pen from Runes:").grid(row=4)
		Label(master, text="Percent Armor Pen from Runes:").grid(row=5)
		Label(master, text="AS from Runes:").grid(row=6)
		Label(master, text="AD from Runes:").grid(row=7)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e3 = Entry(master)
		self.e4 = Entry(master)
		self.e5 = Entry(master)
		self.e6 = Entry(master)
		self.e7 = Entry(master)
		self.e8 = Entry(master)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		self.e3.grid(row=2, column=1)
		self.e4.grid(row=3, column=1)
		self.e5.grid(row=4, column=1)
		self.e6.grid(row=5, column=1)
		self.e7.grid(row=6, column=1)
		self.e8.grid(row=7, column=1)
		return self.e1 # initial focus
	def apply(self):
		first = self.e1.get()
		second = self.e2.get()
		third = self.e3.get()
		fourth = self.e4.get()
		fifth = self.e5.get()
		sixth = self.e6.get()
		seventh = self.e7.get()
		eight = self.e8.get()
		global canvas
		canvas.modalResult3 = (first, second, third, fourth, fifth, sixth, seventh, eight)

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
	# When the Calculate button is pressed, the following runs
	global canvas
	requiredItems = []
	if canvas.runes != None:
		# edit the list-formatted string into something readable
		canvas.runes = canvas.runes[1:-2]
		canvas.runes = canvas.runes.replace("'", "")
		canvas.runesList = canvas.runes.split(", ")
	if canvas.stats != None:
		# edit the list-formatted string into something readable
		canvas.stats = canvas.stats[1:-2]
		canvas.stats = canvas.stats.replace("'", "")
		canvas.statsList = canvas.stats.split(", ")
	# edit the list-formatted string into something readable
	canvas.message = canvas.message[1:-2]
	canvas.message = canvas.message.replace("'", "")
	canvas.list = canvas.message.split(", ")


	for itemName in canvas.list:
		# Include all required items
		for item in canvas.allItems:
			if item["Name"] == itemName:
				requiredItems.append(item)

	# Use provided stats if provided, otherwise use defaults
	try: level = int(canvas.statsList[0])
	except: level = 18
	try: neededCDR = int(canvas.statsList[1])
	except: neededCDR = 0
	try: enemyArmor = int(canvas.statsList[2])
	except: enemyArmor = 100
	try: enemyMR = int(canvas.statsList[3])
	except: enemyMR = 70
	try: enemyHP = int(canvas.statsList[4])
	except: enemyHP = 2000
	try: numItems = int(canvas.statsList[5])
	except: numItems = 6

	# Find the best build and its actual DPS
	build, dmg = bestKayle(requiredItems, level, neededCDR, enemyMR, enemyArmor, enemyHP, numItems, canvas.runesList)
	print build
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
	canvas.create_text(250, 310, text = "DPS: " + str(dmg), fill = "White", font = "Arial 15 bold")

	# Create the pictures and text for the build returned ^

def init(root, canvas):
	# Starts or restarts everything
	initPix(canvas)
	canvas.stats = None
	canvas.runesList = None
	canvas.runes = None
	canvas.message = "None"
	canvas.allItems = [voidstaff, abyssal, lichbane, 
			liandries, ludens, deathcap, 
			roa, nashors,
			aaa, sorcs, athenes, zhonyas,
			zerks, ie, botrk, pd, youmuu,
			hurricane, lw,
			witsend, devourer, essreav, witsend, bc]

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
	# Used to redraw everything on a restart
	canvas.create_text(10,10, anchor = NW, 
		text = "Welcome to the Kayle Build Calculator! \nEnter info in the buttons below to begin.", fill = "white")
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

	


main() # Open and run the UI