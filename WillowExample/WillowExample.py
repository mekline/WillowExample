import random
from willow.willow import *

def session(me):
	
	def ping():
		put({"tag":"PING", "client": me})
	
	#Make a unique paycode for this user!  Note that all paycodes end with the session number as a reality check!
	x = random.randint(0, 16777215000)
	payCode = "%x" % x
	payCode = payCode + str(me) 
	
	#Randomize order of item presentation!
	items = open('Stimlist_full.csv', 'r').readlines()[1:]
	random.shuffle(items)

	#Get all files/parameters we'll need from the stimlist
	stimNo = []
	stimName = []
	movieBase = []
	movieLength = []
	transitive = []
	noncausal = []
	baseline = []
	change1 = []
	#change2 = []
	toChange=[]
	for i in xrange(len(items)):
		fields = items[i].strip().split(',')
		stimNo.append(fields[0])
		stimName.append(fields[1])
		m = fields[1] + "/" + fields[1] + "_" + fields[2]
		movieBase.append(m)
		movieLength.append(fields[3])
		transitive.append(fields[4])
		noncausal.append(fields[5])
		baseline.append("")
		m = fields[1] + "/" + fields[1] + "_" + fields[6]
		change1.append(m)
		#m = fields[1] + "/" + fields[1] + "_" + fields[7]
		#change2.append(m)
		toChange.append(int(fields[7]))
	
	#Choose sentence condition
	condlist = [1,2,3]
	random.shuffle(condlist)
	if (condlist[0]==1):
		sentCond = "noncausal"
		sentences=noncausal
	elif (condlist[0]==2):
		sentCond = "transitive"
		sentences=transitive
	elif (condlist[0]==3):
		sentCond = "baseline"
		sentences=baseline
	else:
		print("Error of shuffling!")
		
	#Choose changetype condition
	
	changeCond = "change1"
	
	#BETWEEN SUBJECTS
	#~ condlist = [1,2]
	#~ random.shuffle(condlist)
	#~ if (condlist[0]==1):
		#~ changeCond = "change1"
	#~ elif (condlist[0]==2):
		#~ changeCond = "change2"
	#~ else:
		#~ print("Error of shuffling!")
	
	#~ #WITHIN SUBJECTS
	#~ changeCond = []
	#~ 1cap =  0
	#~ 2cap = 0
	#~ for i in xrange(len(items)):
		#~ if toChange[i]:
			#~ do1 = random.randrange(2)
			#~ if do1:
				#~ if 1cap < 3: #allowed?
					#~ changeCond.append("change1")
					#~ 1cap = 1cap + 1
				#~ else:
					#~ changeCond.append("change2")
					#~ 2cap = 2cap + 1
			#~ else: #want to do a 2
				#~ if Rcap < 6: #allowed?
					#~ changeCond.append("change2")
					#~ 2cap = 2cap + 1
				#~ else:
					#~ changeCond.append("change1")
					#~ 1cap = 1cap + 1
		#~ else:
			#~ changeCond.append("none")

	
	#Set test movies!
	movieTest = []
	for i in xrange(len(items)):
		if toChange[i]:
			if (changeCond=="change1"):
				movieTest.append(change1[i])
			elif (changeCond =="change2"):
				movieTest.append(change2[i])
		else:
			movieTest.append(movieBase[i])
	
	#Okay, now we start the experiment!
	log('willowSubNo','Paycode','VideoComment','sentCond','changeCond','isChange','trialNo','itemNo','Verb','OrigVid','NewVid','Response','Error','Correct')
	
	#Consent screen with button
	add(open("consent.html"))
	take({"tag": "click", "id": "ConsentButton", "client": me})
	let("")
	
	#System requirements screen with button
	add(open("requirements.html"))
	take({"tag": "click", "id": "ReqButton", "client": me})
	let("")
	
	#Test movie 
	let("")
	add(open("empty.html"))
	#Load up the test movie page!
	vidcode = open("CB_video_exposure.html", "r").read()
	vidcode = vidcode.replace("XXX", "http://www.mit.edu/~mekline/Resources/WillowExample/Movies/GiveBalloon/GiveBalloon") 
	add(vidcode)
	#Wait until the video is finished
	background(ping, 7)
	take({"tag":"PING", "client": me})
	#...and add the question
	add(open("moviecheck.html")) 	
	msg = take({"tag": "click", "client": me})
	
	#Kick them off if they didn't see it!  (Deadends this user)
	if (msg["id"]=="No"):
		let("")
		add(open("sorry.html"))
	#Otherwise make them describe!
	else:
		add(open("moviecheck2.html")) 	
		
	take({"tag": "click", "id": "GoButton", "client": me})
	#Find out if they saw and reported the video!
	movieCheck = peek("#MovieDescrip")
	#print(movieCheck)
	let("")
	
	#Show instruction screen with button
	add(open("instructions.html"))
	take({"tag": "click", "id": "InstructButton", "client": me})
	let("")
	
	
	add(open("empty.html"))
	#Wait 1 second before displaying first trial!
	
	background(ping, 1)
	take({"tag":"PING", "client": me})
	
	#Cycle through trial presentation/exposure
	testError = []
	score = 0
	
	for i in xrange(len(items)):
	#for i in xrange(2): #xxxDebug!!
		let("") #Make sure screen is clear!
		
		#Display the sentence:
		before = open("CB_video_before.html").read()
		before = before.replace("ZZZ", sentences[i])
		add(before)
		
		background(ping,4)
		take({"tag":"PING", "client": me})
		
		let("")
		add(open("empty.html"))
		background(ping,0.5)
		take({"tag":"PING", "client": me})
		
		#Load up the movie page!
		vidcode = open("CB_video_exposure.html", "r").read()
		vidcode = vidcode.replace("XXX", "http://www.mit.edu/~mekline/Resources/WillowExample/Movies/" +movieBase[i])
		add(vidcode)
	
		
		#Wait until the video is finished, then move on
		background(ping, float(movieLength[i])+ 1.5)
		take({"tag":"PING", "client": me})
		
		#Display the sentence again, little pause before going on.
		let("")
		after = open("CB_video_after.html").read()
		after = after.replace("ZZZ", sentences[i])
		add(after)
		
		background(ping,3)
		take({"tag":"PING", "client": me})

		#End Exposure sequence
		
		#Time for math problems!	
		mathA = range(10)
		mathB = range(10)
		random.shuffle(mathA)
		random.shuffle(mathB)
		let("")
		add(open("empty.html"))
		mathy = open("mathproblems.html").read()
		for j in xrange(10):
			mathy = mathy.replace("f"+str(j+1) + "a", str(mathA[j]))
			mathy = mathy.replace("f"+str(j+1) + "b", str(mathB[j]))
		add(mathy)
		background(ping, 5) #xxx Debug!
		take({"tag":"PING", "client": me})
		

		#Start Test sequence
		let("")
		add(open("empty.html"))
		#Load up the movie page!
		vidcode = open("CB_video_exposure.html", "r").read()
		vidcode = vidcode.replace("XXX", "http://www.mit.edu/~mekline/Resources/WillowExample/Movies/" +movieTest[i])
		add(vidcode)
		
		#Wait until the video is finished...
		background(ping, float(movieLength[i])+1.5)
		take({"tag":"PING", "client": me})
		
		#Hide it
		let("")
		add(open("empty.html"))
		add(open("hide.html"))
		
		#...and add the response question"
		add(open("newold_question.html"))
		#add(open("error.html"))
		
		#Wait until the participant hits a button (It also records error if that's what was pressed!)
		testError.append(0)
		msg=take({"tag":"click", "client": me})
		if (msg["id"] == "Error"):
			testError[i] = 1
		if (((msg["id"] == "Same") and (not toChange[i])) | ((msg["id"] == "Different") and (toChange[i]))):
			wasCorrect = 1
		else:
			wasCorrect = 0
		
		score = score + wasCorrect
		
		#Little pause before going on
		background(ping,0.5)
		take({"tag":"PING", "client": me})
		let("")
		
		#Show feedback screen!
		if testError[i]:
			add(open("waserror.html"))
		elif wasCorrect:
			add(open("right.html"))
		else:
			add(open("wrong.html"))
			
		#Add progress bar
		progress = open("progress.html", "r").read()
		progress = progress.replace("ZZZ", str(i+1))
		progress = progress.replace("PPP", str(100*(i+1)/18))
		add(progress)
		
				
		#Little pause before going on
		background(ping,2)
		take({"tag":"PING", "client": me})
		
		#Did the subject error on this item?
		wasError = "None"
		#if (presError[i] | testError[i]):
		if (testError[i]):
			wasError = "Error"
			
		#Session, Paycode, Condition1, Condition2, DidChange?, Trial, ItemNo, ItemName, MovieBase, MovieTest, Response
		log(me, payCode, movieCheck, sentCond, changeCond, toChange[i], i, stimNo[i], stimName[i], movieBase[i], movieTest[i], msg["id"], wasError, wasCorrect)
		
		
		#Little pause before going on
		background(ping,0.5)
		take({"tag":"PING", "client": me})
		
	#End Memory loop
	
	#Show thankyou and total score!
	percRight = str(100*float(score)/float(18)).split(".")[0]
	let("")
	thanks = open("thankyou.html", "r").read()
	thanks = thanks.replace("YYY", payCode)
	thanks = thanks.replace("XXX", str(score))
	thanks = thanks.replace("ZZZ", str(percRight))
	add(thanks)
		
		
	

run(session, 6999)
