# Kalista Damage Calculator
# Anthony Kuntz

def calculateDamage(itemList, level, enemyHP, enemyArmor, enemyMR, jumping, actives, doPrint = True):

	AD = 53.46 + 3.25*level + 50
	AS = 0.658 * 1.033**level
	MS = 325
	critChance = 50
	flatAPen = 0
	perAPen = 0
	lifeSteal = 0
	bonusList = []
	alreadyAppliedBoots = False


	for item in itemList:
		try: critChance += item["Crit"]
		except: pass

		try: AD += item["AD"]
		except: pass

		try: AS *= (1 + item["AS"] / 100.0)
		except: pass

		try: flatAPen += item["aPen"] if type(item["aPen"]) == int else 0
		except: pass

		try: perAPen += item["aPen"] if type(item["aPen"]) == float else 0
		except: pass

		try: lifeSteal += item["LS"]
		except: pass

		try: 
			if not alreadyAppliedBoots:
				MS += item["MS"] if type(item["MS"]) == int else 0
				if item == zerks: alreadyAppliedBoots = True
		except: pass

		try: MS *= (1 + item["MS"] / 100.0) if type(item["MS"]) == float else 1
		except: pass

		try: bonusList.extend(item["Bonus"])
		except: pass

	bonusList = set(bonusList)
	bonusList = list(bonusList)
	# Remove duplicates


	kalistaADFactor = 0.90
	kalistaDmg = kalistaADFactor * AD
	hasIE = "ieCrits" in bonusList
	critFactor = 2 + .5 * (hasIE)
	critChance /= 100.0

	if "youmuuActive" in bonusList and actives:
		MS *= 1.2
		AS *= 1.4

	# Check for maxes
	if critChance > 1: critChance = 1
	if AS > 2.5: AS = 2.5

	if AS > 2 and "bolts" in bonusList: AS = 2
	# Richard Adjustment for hurricane bolt travel time
	if jumping: AS *= .67
	# Richard Adjustment for jumping delay


	
	dmgPerAddSpear = 10 + .2 * AD
	if level > 3:
		dmgPerAddSpear = 14 + .225 * AD
		if level > 4:
			dmgPerAddSpear = 19 + .25 * AD
			if level > 6:
				dmgPerAddSpear = 25 + .275 * AD
				if level > 8:
					dmgPerAddSpear = 32 + .30 * AD

	qDmg = 0
	if level > 1:
		qDmg = 10 + AD
		if level > 7:
			qDmg = 70 + AD
			if level > 9:
				qDmg = 130 + AD
				if level > 11:
					qDmg = 190 + AD
					if level > 12:
						qDmg = 250 + AD

	pureDPS = ((kalistaDmg * critFactor * critChance) + (kalistaDmg * (1 - critChance))) * AS
	spearDPS = dmgPerAddSpear * AS
	addPhyDmg = (enemyHP * .04) * AS if "botrkDmg" in bonusList else 0

	totalNonReducedPhyDmg = pureDPS + spearDPS + addPhyDmg

	adBurst = 0
	if actives: adBurst = enemyHP * .10 if "botrkActive" in bonusList else 0
	adBurst += 20 + .60 * AD
	# For first spear
	adBurst += qDmg

	apBurst = 100 * critFactor * critChance + 100 * (1 - critChance) if "shivDmg" in bonusList else 0

	enemyArmor -= enemyArmor * perAPen
	enemyArmor -= flatAPen
	if enemyArmor < 0: enemyArmor = 0

	redAdBurst = round( adBurst * ( 100.0 / (100 + enemyArmor)) , 2 )
	redApBurst = round( apBurst * ( 100.0 / (100 + enemyMR)) , 2 )
	redDPS = round( totalNonReducedPhyDmg * ( 100.0 / (100 + enemyArmor)) , 3 )

	if doPrint:
		print "Bonus effects and abilties: " + str(bonusList)
		print "Movement Speed: " + str(int(round(MS)))
		print "Life Steal: \t" + str(lifeSteal)
		print "Attack Damage: \t" + str(int(round(AD)))
		print "Crit Chance: \t" + str(critChance)
		print "Modified AS: \t" + str(AS)
		print "AP Burst: \t\t" + str(redApBurst)
		print "AD Burst: \t\t" + str(redAdBurst)
		print "DPS: \t\t\t" + str(redDPS)

		

	return redDPS


zerks  	  = { "AS" : 25, "MS" : 45, "Bonus" : ["Better Hops"] , "Name" : "Zerks"}
ie 		  = { "AD" : 80, "Crit" : 20, "Bonus" : ["ieCrits"], "Name" : "IE"}
botrk	  = { "AD" : 25, "AS" : 40, "LS" : 10, "Bonus" : ["botrkDmg", "botrkActive"], "Name" : "BotRK"}
pd		  = { "AS" : 50, "Crit" : 35, "MS" : 5.0, "Bonus" : ["moveThrough"], "Name" : "PD"}
shiv 	  = { "AS" : 40, "Crit" : 20, "MS" : 6.0, "Bonus" : ["shivDmg"], "Name" : "Shiv"}
youmuu    = { "AD" : 30, "Crit" : 15, "aPen" : 20, "Bonus" : ["youmuuActive"], "Name" : "Youmuus"}
hurricane = { "AS" : 70, "Bonus" : ["bolts"], "Name" : "Hurricane"}
bt 		  = { "AD" : 80, "LS" : 20, "Bonus" : ["btShield"], "Name" : "BT"}
lw		  = { "AD" : 40, "aPen" : 35.0, "Name" : "LW"}
frozMal   = { "AD" : 30, "Bonus" : ["Slow"], "Name" : "Frozen Mallet"}
mercScim  = { "AD" : 80, "Bonus" : ["QSS"], "Name" : "Merc Scimitar"}

allItems = [zerks, ie, botrk, pd, shiv, youmuu, hurricane, bt, lw, frozMal, mercScim]


# Enter whether zerks are required, level, enemy hp, enemy armor, enemy MR, 
# whether jumping, whether actives count, and whether multiple IE are allowed
# Brute forces the max DPS (Not including any burst damage)
def determineMaxDPS( zerksRequired, level, enemyHP, enemyArmor, enemyMR, jumping, actives, multipleIE):

	allItems = [ie, botrk, pd, shiv, youmuu, hurricane, bt, lw]
	allButIE = [botrk, pd, shiv, youmuu, hurricane, bt, lw]
	possibleItems = [ie, botrk, pd, shiv, youmuu, hurricane, bt, lw] if multipleIE else allButIE
	firstList = possibleItems if not zerksRequired else [ zerks ]

	maxDps = 0
	for a in firstList:
		for b in allItems:
			for c in [hurricane]:
				for d in possibleItems:
					for e in possibleItems:
						for f in possibleItems:
							dmg = calculateDamage( [a,b,c,d,e,f], level, enemyHP, enemyArmor, enemyMR, jumping, actives, doPrint = False)
							if dmg > maxDps: 
								maxDps = dmg
								bestbuild = [ a["Name"], b["Name"], c["Name"], d["Name"], e["Name"], f["Name"] ]
	print ""
	print "Build for max dps under given conditions is:"
	print bestbuild, maxDps

def run( itemList, level, enemyHP, enemyArmor, enemyMR, jumping, actives, zerksRequired, multipleIE):
	calculateDamage( itemList, level, enemyHP, enemyArmor, enemyMR, jumping, actives)
	determineMaxDPS( zerksRequired, level, enemyHP, enemyArmor, enemyMR, jumping, actives, multipleIE)



###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
"""
											START BELOW
"""
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################


allItems = [zerks, ie, botrk, pd, shiv, youmuu, hurricane, bt, lw, frozMal, mercScim]

# Enter a list of items, your level, enemy HP, enemy Armor, enemy MR, 
# whether jumping, whether using actives, whether zerks are required,
# and whether the code can suggest multiple Infinity Edges
#
# Stats, DPS, and burst damage will be printed out after being run
# Then, code will brute force the max DPS build for the given conditions
#

# FORMAT: 
#
# run(itemList, level, enemyHP, enemyArmor, enemyMR, jumping, actives, zerksRequired, multipleIE)

run( [pd, pd, pd, pd, pd, pd], 18, 2000, 100, 50, False, True, True, False)