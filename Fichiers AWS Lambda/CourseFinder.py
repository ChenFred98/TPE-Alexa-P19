#usr/bin/python3

def getCourseData(courseName):
    data = open('data/data.txt').read()
    data = data.split('\n')
    collectMode = 0
    outputData = []
    for row in data:
        if collectMode == 1 and row[0] == '+':
            collectMode = 0 
        elif row[1:] == courseName:
            collectMode = 1
        elif collectMode == 1:
            outputData.append(row)
    for i in range(len(outputData)):
        outputData[i] = outputData[i].split(',')
    return outputData

def getCourseTimeSlot(courseName, courseType = ["C","D","T"], day = ["L","MA","ME","J","V","S"]):
    courseTimeSlots = getCourseData(courseName)
    dayDict = {
        "L" : "lundi",
        "MA": "mardi",
        "ME": "mercredi",
        "J" : "jeudi",
        "V" : "vendredi",
        "S" : "samedi"
        }
    timeSlotList = []
    for timeSlot in courseTimeSlots :
        timeSlotDay = timeSlot[3].split(' ')[0].split('=')[1]
        timeSlotStartTime = timeSlot[3].split(' ')[1]
        timeSlotRoom = timeSlot[5][2:6]
        isDoubleClass = (timeSlot[5][7] != '/')
        if (timeSlot[1][0] in courseType) and timeSlotDay in day:
            if not isDoubleClass:
                timeSlotList.append((courseName, timeSlot[1][0],dayDict[timeSlotDay],timeSlotStartTime,timeSlotRoom))
            else:
                temp = []
                temp.append((courseName, timeSlot[1][0],dayDict[timeSlotDay],timeSlotStartTime,timeSlotRoom))
                timeSlotDay = timeSlot[5].split('/')[1].split(' ')[0]
                timeSlotStartTime = timeSlot[5].split('/')[1].split(' ')[1]
                timeSlotRoom = timeSlot[7][2:6]
                temp.append((courseName, timeSlot[1][0],dayDict[timeSlotDay],timeSlotStartTime,timeSlotRoom))
                timeSlotList.append(tuple(temp))
    return timeSlotList

def mapCourseName(inputString):
    data = open('data/courseMapping.txt', "r+", encoding="utf-8").read()
    data = data.split('\n')
    for course in data:
        if inputString == course.split(',', 1)[1]:
            return course.split(',', 1)[0]    

if __name__ == "__main__":
    course = input("Saisissez le code du cours dont vous voulez connaitre les horaires : ")
    courseType = input("Saisissez le type de cours (C pour CM, D pour TD, T pour TP)")
    day = input("Saisissez le jour concerné (L pour Lundi, MA pour Mardi ...) :")

    for timeSlot in getCourseTimeSlot(course, [courseType], [day]):
        print(timeSlot)