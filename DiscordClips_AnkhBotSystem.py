#---------------------------------------
#	Import Libraries
#---------------------------------------
import clr, sys, json, os, codecs
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "DiscordClips"
Website = ""
Creator = "Yaz12321"
Version = "1.0"
Description = "Post twitch clips on discord"

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
#   Version Information
#---------------------------------------

# Version:


# > 1.0 < 
    # Official Release

class Settings:
    # Tries to load settings from file if given 
    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile = None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig',mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig') 
        else: #set variables if no settings file
            
            self.Command = "!discordclip"
            self.Permission = "Caster"
            self.PermissionInfo = ""
            self.Channel = ""
            self.Period = "day"
            

            
    # Reload settings on save through UI
    def ReloadSettings(self, data):
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile,  encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig',mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
        return


#---------------------------------------
# Initialize Data on Load
#---------------------------------------
def Init():
    # Globals
    global MySettings

    # Load in saved settings
    MySettings = Settings(settingsFile)

    # End of Init
    return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
    # Globals
    global MySettings

    # Reload saved settings
    MySettings.ReloadSettings(jsonData)

    # End of ReloadSettings
    return

def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == MySettings.Command:
               
        #check if user has permission
        if Parent.HasPermission(data.User, MySettings.Permission, MySettings.PermissionInfo):
            # Get clips through API    
            header = {'Accept': 'application/vnd.twitchtv.v5+json','Client-ID': '4l912jdf5x78xwe5l096mxti4tkzv3'}
            if MySettings.Channel == "":
                Channel = Parent.GetChannelName()
            else:
                Channel = MySettings.Channel
            api = "https://api.twitch.tv/kraken/clips/top?channel={}&period={}&trending=false&limit=100".format(Channel,MySettings.Period)

            result = dict()
            result = json.loads(Parent.GetRequest(api, header))
            
            global allclips
            allclips = json.loads(result['response'])['clips']
            i = 0

            ClipsDetails = []
                    
            for clip in allclips:
                clipi = []
                
                clipi.append(allclips[i]['slug']) #ClipsDetails[0]
                clipi.append(allclips[i]['title']) #ClipsDetails[1]
                clipi.append(allclips[i]['duration']) #ClipsDetails[2]
                createdt = allclips[i]['created_at'].replace("T"," ")
                created = createdt.replace("Z","")
                clipi.append(created) #ClipsDetails[3]
                clipi.append(allclips[i]['curator']['name']) #ClipsDetails[4]
                clipi.append(allclips[i]['tracking_id']) #ClipsDetails[5]
                ClipsDetails.append(clipi)
                i=i+1
            for i in ClipsDetails:
                Parent.SendDiscordMessage("[{}] {}, by {}. https://clips.twitch.tv/{}".format(i[3],i[1],i[4],i[0]))
            Parent.SendTwitchMessage("Today's clips have been posted on discord")
            

    return

def Tick():
    return

def UpdateSettings():
    with open(m_ConfigFile) as ConfigFile:
        MySettings.__dict__ = json.load(ConfigFile)
    return
