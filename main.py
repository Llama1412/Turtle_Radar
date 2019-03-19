import turtle as tt
import urllib.request
import json
import time
import math
import os
import geopy.distance
import random
from gtts import gTTS
import os
from consolemenu import *
from consolemenu.items import *

players = []
menu = SelectionMenu(players)

with urllib.request.urlopen("https://state.hoggitworld.com/f67eecc6-4659-44fd-a4fd-8816c993ad0e") as url:
	data = json.loads(url.read().decode())
	for i in range(len(data["objects"])):
		if data["objects"][i]["Flags"]["Human"] == True:
			players.append(data["objects"][i]["UnitName"])

player_index = menu.get_selection(players, title="GAW Turtle Radar", subtitle="By [CVW-69] Llama")
target = players[player_index]

turtles = []
tt.bgcolor("black")
tt.setup(width=600,height=600,startx=300,starty=300)


class THREAT:
	HIGH = "red"
	MEDIUM = "yellow"
	LOW = "green"
	NONE = "blue"

colors  = ["red","orange","purple","pink","yellow","cyan"]

threats = {
	"Su-27": THREAT.HIGH,
	"F-5E-3": THREAT.HIGH,
	"Su-25T": THREAT.MEDIUM,
	"Mi-26": THREAT.LOW,
	"J-11A": THREAT.HIGH,
	"A-50": THREAT.NONE,
	"MiG-21Bis": THREAT.HIGH,
	"MiG-29S": THREAT.HIGH,
	"MiG-31": THREAT.HIGH
}


def drawCircle(radius):
	steve = tt.Turtle()
	steve.color("green")
	steve.width(3)
	steve.hideturtle()
	steve.speed(1000)

	steve.pu()
	steve.right(90)

	steve.forward(radius)
	if (radius/2.5 < 10) == False:
		steve.write(str(radius/2.5))
	steve.left(90)
	steve.pd()
	steve.circle(radius)

def getHeading(head):
	return float((head*180)/math.pi)

def drawDash(angle, length):
	constant = 10
	steve = tt.Turtle()
	steve.color("green")
	steve.width(1)
	steve.hideturtle()
	steve.speed(5000)

	steve.right(angle-90)
	curdistance = 0
	blank = 0
	while length > curdistance:
		if length-curdistance >= constant:
			if blank == 1:
				steve.pu()
				steve.forward(constant)
				blank = 0
				curdistance = curdistance + 10
			if blank == 0:
				steve.pd()
				steve.forward(constant)
				blank = 1
				curdistance = curdistance + 10
		else:
				if blank == 1:
					steve.pu()
					steve.forward(length-curdistance)
					blank = 0
					curdistance = curdistance + (length-curdistance)
				if blank == 0:
					steve.pd()
					steve.forward(length-curdistance)
					blank = 1
					curdistance = curdistance + (length-curdistance)




def drawRadarBackground():
	largest_radius = 250
	#1 mile is 2.5px

	division = largest_radius/4
	#drawCircle(5)
	drawCircle(largest_radius) #100 miles
	#drawCircle(largest_radius - division) #75 Miles
	drawCircle(largest_radius - (2*division)) #50 miles
	#drawCircle(largest_radius - (3*division)) #25 Miles
	#drawDash(45, 250)
	#drawDash(135, 250)
	#drawDash(225, 250)
	#drawDash(315, 250)

def calculate_initial_compass_bearing(pointA, pointB):
	lat1 = math.radians(pointA[0])
	lat2 = math.radians(pointB[0])
	diffLong = math.radians(pointB[1] - pointA[1])
	x = math.sin(diffLong) * math.cos(lat2)
	y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
	* math.cos(lat2) * math.cos(diffLong))
	initial_bearing = math.atan2(x, y)
	initial_bearing = math.degrees(initial_bearing)
	compass_bearing = (initial_bearing + 360) % 360
	return compass_bearing




drawRadarBackground()
while True:
	with urllib.request.urlopen("https://state.hoggitworld.com/f67eecc6-4659-44fd-a4fd-8816c993ad0e") as url:
		data = json.loads(url.read().decode())
		for i in range(len(data["objects"])):
			if data["objects"][i]["Flags"]["Human"] == True:
				if data["objects"][i]["UnitName"] == target:
					MyLat = data["objects"][i]["LatLongAlt"]["Lat"]
					MyLon = data["objects"][i]["LatLongAlt"]["Long"]
					MyAlt = data["objects"][i]["LatLongAlt"]["Alt"]
					MyHeading = data["objects"][i]["Heading"]
					MyHeadingDeg = getHeading(MyHeading)
					Pointer = tt.Turtle()
					Pointer.shape("arrow")
					Pointer.speed(0)
					Pointer.turtlesize(1,3)
					Pointer.color("green")
					Pointer.left(90-MyHeadingDeg)

					Label = tt.Turtle()
					Label.color("green")
					Label.hideturtle()
					Label.pu()
					Label.setpos(-250,250)
					Label.write("Radar for: "+str(target))

		onscreen = 0
		for i in range(len(data["objects"])):
			MyPos = (MyLat, MyLon)
			if data["objects"][i]["Coalition"] == "Allies" and data["objects"][i]["Flags"]["Born"] == True:
				plane = data["objects"][i]
				Type = False
				Threat = False
				if plane["Name"] in threats.keys():
					Type = plane["Name"]
					Threat = threats[plane["Name"]]
					Lat = plane["LatLongAlt"]["Lat"]
					Lon = plane["LatLongAlt"]["Long"]
					Alt = plane["LatLongAlt"]["Alt"]
					ALtFeet = float(Alt/0.3048)
					TPos = (Lat, Lon)
					Distance = geopy.distance.distance(MyPos,TPos).nm
					A = (MyLat, MyLon)
					B = (Lat, Lon)
					Bearing = calculate_initial_compass_bearing(A, B)
					Heading = getHeading(plane["Heading"])
					if Distance <= 100 and ALtFeet >= 500:
						turtles.append(tt.Turtle())
						turtles[-1].speed(0)
						turtles[-1].turtlesize(1,3)
						turtles[-1].pu()
						turtles[-1].color(random.choice(colors))
						turtles[-1].right(Bearing-90)
						turtles[-1].forward(2.5*Distance)
						lturn = 90-Heading
						turtles[-1].left(lturn)
						turtles[-1].write(Type)
						onscreen = onscreen+1

				if not Type:
					continue
	time.sleep(10)
	Pointer.reset()
	for turts in turtles:
		turts.reset()
	turtles = []
