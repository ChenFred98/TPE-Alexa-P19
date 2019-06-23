from ask import alexa
import boto3
import CourseFinder


def lambda_handler(request_obj, context=None):
    metadata = {}
    return alexa.route_request(request_obj, metadata)


@alexa.default_handler()
def default(request):
    return alexa.create_response('Vous pouvez rechercher une salle en demandant par exemple où est le cours de introduction à la vie politique')


@alexa.intent_handler('HelloWorldIntent')
def hello_world_handler(request):
    speech_text = "Hello World!"
    return alexa.create_response(speech_text)
        

@alexa.intent_handler('CUSTOM_SearchRoom')
def recherche_salle_handler(request):
    slots = request.request["request"]["intent"]["slots"]
    courseType = slots["typeDeCours"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]
    courseName = slots["nomDuCours"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]
    try:
        day = slots["jour"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]
        data = CourseFinder.getCourseTimeSlot(courseName["id"], [courseType["id"]], [day["id"]])
        dayAsked = True
    except :
        day = {"id" : []}
        data = CourseFinder.getCourseTimeSlot(courseName["id"], [courseType["id"]])
        dayAsked = False
        

    print(data)
    if len(data) == 0 :
        if dayAsked == True:
            return alexa.create_response("Il n'y a pas de " + courseType["name"] +
                                        " de " + courseName["name"] + " le " + day["name"] + " . ")
        else:
            return alexa.create_response("Il n'y a pas de " + courseType["name"] +
                                        " de " + courseName["name"]+ " . ")
    elif len(data) == 1:
        if dayAsked == True:
            return alexa.create_response("Le " + courseType["name"] + " de " + courseName["name"] + 
                                        " du " + data[0][2] + " a lieu en " + data[0][4] +" à " +
                                        data[0][3].split("-")[0].split(":")[0] + " heures " + 
                                        data[0][3].split("-")[0].split(":")[1])
        else:
            return alexa.create_response("Le " + courseType["name"] + " de " + courseName["name"] + 
                                         " aura lieu " + data[0][2] + " en " + data[0][4] +" à " +
                                        data[0][3].split("-")[0].split(":")[0] + " heures " + 
                                        data[0][3].split("-")[0].split(":")[1])
    else :
        if dayAsked == True :
            response = "Il y a plusieurs " + courseType["name"] + " de " + courseName["name"] + " le " + day["name"] + ". "
            response = response + ("Il y aura un " + courseType["name"] + " qui aura lieu en " + data[0][4] +" à " +
                                    data[0][3].split("-")[0].split(":")[0] + " heures " + data[0][3].split("-")[0].split(":")[1] + ". ")
            for i in range(1,len(data)):
                response = response + ("Il y aura un autre " + courseType["name"] + " qui aura lieu en " + data[i][4] +" à " +
                                    data[i][3].split("-")[0].split(":")[0] + " heures " + data[i][3].split("-")[0].split(":")[1] + ". ")
            return alexa.create_response(response)
        else :
            response = "Il y a plusieurs " + courseType["name"] + " de " + courseName["name"] + ". "
            response = response + ("Il y aura un " + courseType["name"] + " qui aura lieu le "+ data[0][2]+ " en " + data[0][4] +" à " +
                                    data[0][3].split("-")[0].split(":")[0] + " heures " + data[0][3].split("-")[0].split(":")[1] + ". ")
            
            for i in range(1,len(data)):
                response = response + ("Il y aura un autre " + courseType["name"] + " qui aura lieu le "+ data[i][2]+ " en " 
                                    + data[i][4] +" à " + data[i][3].split("-")[0].split(":")[0] + " heures " + 
                                    data[i][3].split("-")[0].split(":")[1] + ". ")
            return alexa.create_response(response)