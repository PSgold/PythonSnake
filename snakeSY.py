###################################################IMPORTED LIBRARIES#########################################
import pygame,sys,os,random,pickle
from pathlib import Path
from shutil import copyfile
from time import time
###################################################IMPORTED LIBRARIES#########################################



##################################################GLOBAL VARIABLES############################################
Colordict = {
    'white':(255,255,255),
    'black':(0,0,0),
    'blue':(0,0,220),
    'lsb':(176,196,222), #light steel blue
    'lsg':(32,178,170), #light sea green
    'green':(0,128,0),
    'olive':(128,128,0),
    'OliveDrab':(107,142,35),
    'palegoldenrod': (238,232,170),
    'khaki': 	(240,230,140),
    'DarkKhaki':(189,183,107),
    'DarkGoldenrod':(184,134,11),
    'Goldenrod':(218,165,32),
    'SaddleBrown':(139,69,19),
    'Sienna':(160,82,45),
    'Peru':(205,133,63),
    'yellowgreen':(154,205,50),
    'yellow':(250,230,0),
    'gold':(255,215,0),
    'mediumyellow':(250,180,0),
    'orange':(255,165,0),
    'crimson':(220,20,60),
    'red':(255,0,0)
}
cwd = os.path.dirname(os.path.realpath(__file__))
MW_Width, MW_Height = 1920, 1080
Resolution = (MW_Width,MW_Height)
MW = pygame.display.set_mode(Resolution,pygame.FULLSCREEN)

ssize = 10 #snake size based on radius
sizeB2cc = 6 #size between 2 circle centers of snake
fsize = ssize - 2 #food size based on radius
fpsint = 40 #Sets the speed of the snake 

userDict = {}#global user database
gusername = ''#global username
#gUDscore = ''#global user duplicate score
userEntryDefault = {'username':'****','Hscore':'****','time':'****'}
##################################################GLOBAL VARIABLES############################################



##################################################CLASSES AND DEFINITIONS#################################################

class snake:
    @staticmethod
    def Draw_Snake(SP):
        for s in SP:
            pygame.draw.circle(MW, Colordict['DarkKhaki'], s, ssize)
    
    @staticmethod
    def Move_Snake(SP,dir,cdir,score,timeCounter):
        if dir == 'Right' and cdir != 'Left':
            SPH = [SP[0][0]+6,SP[0][1]]
            SP.insert(0,SPH)
            SP.pop(-1)
            
        elif dir == 'Down' and cdir != 'Up':
            SPH = [SP[0][0],SP[0][1]+6]
            SP.insert(0,SPH)
            SP.pop(-1)
            
        elif dir == 'Left' and cdir != 'Right':
            SPH = [SP[0][0]-6,SP[0][1]]
            SP.insert(0,SPH)
            SP.pop(-1)
            
        elif dir == 'Up' and cdir != 'Down':
            SPH = [SP[0][0],SP[0][1]-6]
            SP.insert(0,SPH)
            SP.pop(-1)
        else:
            End_Game(score,timeCounter) #End game when you move turn in the opposite direction the snake is moving
            
        return dir, SP


class food:
    @staticmethod
    def Make_Food(pos=None,ate=0):
        if ate == 1:
            posw = random.choice(range(fsize, MW_Width - fsize))
            posh = random.choice(range(int(MW_Height / 8.3),MW_Height - fsize))
            pos = [posw,posh]
        
        return pos
        
    @staticmethod
    def Draw_Food(pos):
        pygame.draw.circle(MW,Colordict['yellowgreen'],pos,fsize)


class ChangeSnake:
    @staticmethod    
    def Ate_Food(SP,Cfood,dir,score): #Cfood = current food position
        snakepos = [SP[0][0],SP[0][1]]
        if (abs(Cfood[0] - snakepos[0]) <= (ssize + fsize) and abs(Cfood[1] - snakepos[1]) <= (ssize + fsize)):  
            foodpos = food.Make_Food(ate=1)
            score = Score_Screen.Set_Score(score)
            SP = ChangeSnake.Add_ToSnake(SP,dir,score)
            return foodpos, SP, score
        else:
            return Cfood, SP, score


    @staticmethod
    def Add_ToSnake(SP,dir,score):
        numOfCircleAdded = 3
        difficulty = score/5+1
        if difficulty >= 1:
            numOfCircleAdded = difficulty * numOfCircleAdded
        
        if dir == 'Right':
            c = 1
            while c <= numOfCircleAdded:
                SPH = [SP[0][0]+sizeB2cc,SP[0][1]]
                SP.insert(0,SPH)
                c+=1
        if dir == 'Left':
            c = 1
            while c<=numOfCircleAdded:
                SPH = [SP[0][0]-sizeB2cc,SP[0][1]]
                SP.insert(0,SPH)
                c+=1
            
        if dir == 'Up':
            c = 1
            while c<=numOfCircleAdded:
                SPH = [SP[0][0],SP[0][1]-sizeB2cc]
                SP.insert(0,SPH)
                c+=1
            
        if dir == 'Down':
            c = 1
            while c<=numOfCircleAdded:
                SPH = [SP[0][0],SP[0][1]+sizeB2cc]
                SP.insert(0,SPH)
                c+=1
            
        
        '''
        #Adds on to back of snake
        if dir == 'Right':
            SPH = [SP[-1][0]-sizeB2cc,SP[-1][1]]
            SP.insert(-1,SPH)
            SP.insert(-1,SPH)
        if dir == 'Left':
            SPH = [SP[-1][0]+sizeB2cc,SP[-1][1]]
            SP.insert(-1,SPH)
            SP.insert(-1,SPH)
        if dir == 'Up':
            SPH = [SP[-1][0],SP[-1][1]+sizeB2cc]
            SP.insert(-1,SPH)
            SP.insert(-1,SPH)
        if dir == 'Down':
            SPH = [SP[-1][0],SP[-1][1]-sizeB2cc]
            SP.insert(-1,SPH)
            SP.insert(-1,SPH)    
        '''
        return SP


    @staticmethod
    def Test_Collision(SP,score,timeCounter):
        if SP[0][0] <= (sizeB2cc):
            End_Game(score,timeCounter)
        elif SP[0][0] >= (MW_Width-sizeB2cc):
            End_Game(score,timeCounter)
        elif SP[0][1] <= MW_Height/8.85:
            End_Game(score,timeCounter)
        elif SP[0][1] >= MW_Height-sizeB2cc:
            End_Game(score,timeCounter)
        
        #print(SP)
        snakeHeadPos = [SP[0][0],SP[0][1]]
        count = 1
        for S in SP:
            if count < 4:
                pass
            else:
                if (abs(S[0] - snakeHeadPos[0]) <= sizeB2cc and abs(S[1] - snakeHeadPos[1]) <= sizeB2cc):
                    '''
                    print(S)
                    print (SP[0])
                    print (SP)
                    '''
                    End_Game(score,timeCounter)
            count += 1


class Score_Screen:
    @staticmethod
    def Set_ScoreScreen(score=0,timeCounter=0):
        SS = pygame.Surface((MW_Width,MW_Height/9))
        SS.fill(Colordict['olive'])
        SS = MW.blit(SS,(1,1))
        
        
        txtObjHeight = MW_Height/45

        txt = 'SCORE:'
        txtObjIndent1 = MW_Width/4.5
        txtObjIndent2 = MW_Width/3.2
        scoreTxtObj = New_Txt(txt,'Comic Sans MS',40,'yellow',1,0)
        scoreObj = New_Txt(str(score),'Comic Sans MS',40,'yellow',1,0)
        MW.blit(scoreTxtObj,(txtObjIndent1,txtObjHeight))
        MW.blit(scoreObj,(txtObjIndent2,txtObjHeight))

        
        txt2 = 'Time:' 
        time = convertToTime(timeCounter)
        txtObj2Indent1 = MW_Width/1.6
        txtObj2Indent2 = MW_Width /1.4
        scoreTxtObj2 = New_Txt(txt2,'Comic Sans MS',40,'yellow',1,0)
        scoreObj2 = New_Txt(time,'Comic Sans MS',40,'yellow',1,0)
        MW.blit(scoreTxtObj2,(txtObj2Indent1,txtObjHeight))
        MW.blit(scoreObj2,(txtObj2Indent2,txtObjHeight))

    @staticmethod
    def Set_Score(score):
        score += 1
        return score


class Rect:
    
    def __init__(self,pos):
        self.pos = pos
        self.rect = pygame.Rect(self.pos)
        self.rect_surf = pygame.Surface((self.pos[2],self.pos[3]))
        self.txtobjpos = self.rect[0]+(self.rect[2]*.35),self.rect[1]+(self.rect[3]*.15)
    
    def New_Button(self,surf,color,outline=0,txt=None):
        if outline == 1:
            self.outline = 1
            self.rect_surf.fill(Colordict[color])
            surf.blit(self.rect_surf,self.rect)
            pygame.draw.rect(surf,Colordict[color],self.rect,4)
        elif outline ==2:
            self.outline = 2
            self.rect_surf.fill(Colordict[color])   
            surf.blit(self.rect_surf,self.rect)
            pygame.draw.rect(surf,Colordict['black'],self.rect,4)
        elif outline == 0:
            if self.outline == 1:
                self.rect_surf.fill(Colordict[color])
                surf.blit(self.rect_surf,self.rect)
                pygame.draw.rect(surf,Colordict[color],self.rect,4)
            elif self.outline == 2:
                self.rect_surf.fill(Colordict[color])
                surf.blit(self.rect_surf,self.rect)
                pygame.draw.rect(surf,Colordict['black'],self.rect,4)
        if txt != None:
            surf.blit(txt,self.txtobjpos)

    def New_TxtBox(self,surf,color,outline=2):
        if outline == 1:
            self.outline = outline
            self.rect_surf.fill(Colordict[color])
            surf.blit(self.rect_surf,self.rect)
            pygame.draw.rect(surf,Colordict['black'],self.rect,3)
        elif outline == 0:
            self.outline = outline
            self.rect_surf.fill(Colordict[color])
            surf.blit(self.rect_surf,self.rect)
            pygame.draw.rect(surf,Colordict[color],self.rect,3)
        elif outline == 2:
            if self.outline == 1:
                self.rect_surf.fill(Colordict[color])
                surf.blit(self.rect_surf,self.rect)
                pygame.draw.rect(surf,Colordict['black'],self.rect,3)
            elif self.outline == 0:
                self.rect_surf.fill(Colordict[color])
                surf.blit(self.rect_surf,self.rect)
                pygame.draw.rect(surf,Colordict[color],self.rect,3)

def New_Txt(txt,font,fsize,color,bold,italic):
    TxtFont = pygame.font.SysFont(font,int(fsize),bold,italic)
    txtobj = TxtFont.render(txt,1,Colordict[color])
    return txtobj


def Get_Upper():
    keymod = pygame.key.get_mods()
    if keymod & pygame.KMOD_SHIFT or keymod & pygame.KMOD_CAPS:
        return 1
    else:
        return 0


def End_Game(score,timeCounter):
    global userDict
    global gusername
    timeCounter = convertToTime(timeCounter)
    currentUserEntry = {'username':gusername,'Hscore':score,'time':timeCounter}
    if gusername in userDict:
        if score > userDict[gusername]['Hscore']:
            userDict[gusername]['Hscore'] = score
            userDict[gusername]['time'] = str(timeCounter)
    writeDataPickle(userDict)
    HscoreSorted = sortHscore(userDict)
    checkDuplicate = checkDuplicates(HscoreSorted)
    if len(HscoreSorted) > 2:
        dict1 = getHscore123(HscoreSorted,userDict,1,checkDuplicate)
        dict2 = getHscore123(HscoreSorted,userDict,2,checkDuplicate)
        dict3 = getHscore123(HscoreSorted,userDict,3,checkDuplicate)
        gameOver(currentUserEntry,dict1,dict2,dict3)
    elif len(HscoreSorted) == 2:
        dict1 = getHscore123(HscoreSorted,userDict,1,checkDuplicate)
        dict2 = getHscore123(HscoreSorted,userDict,2,checkDuplicate)
        print(dict2)
        gameOver(currentUserEntry,dict1,dict2)
    elif len(HscoreSorted) == 1:
        dict1 = getHscore123(HscoreSorted,userDict,1,checkDuplicate)
        gameOver(currentUserEntry,dict1)


def Quit_Game():
    pygame.QUIT()
    sys.exit()


def writeDataPickle(dictToWrite):
        if sys.platform == 'win32':
            pfile_path = cwd + '\\data.pickle'
            pfile_path = pfile_path.replace('\\','/')
        else:
            pfile_path = cwd + '/data.pickle'
        
        pfile_path = str(Path(pfile_path))
        pdatafile = open(pfile_path,'wb')
        pickle.dump(dictToWrite,pdatafile)
        pdatafile.close()


def Check_User(username,password,los=None): #los = login or sign up submit button pressed
    global userDict
    global gusername 
    gusername = username
    adddict = {'username':username,'password':password,'Hscore':0,'time':'0:00'}
    
    if sys.platform == 'win32':
        pfile_path = cwd + '\\data.pickle'
        pfile_path = pfile_path.replace('\\','/')
        dfile_path = cwd + '\\default.pickle'
        dfile_path = dfile_path.replace('\\','/')    
    else:
        pfile_path = cwd + '/data.pickle'
        dfile_path = cwd + '/default.pickle'
    
    pfile_path = str(Path(pfile_path))
    dfile_path = str(Path(dfile_path))

    pfile_path0 = Path(pfile_path) #variable that keeps Path posix and doesn't turn it to string

    if pfile_path0.is_file():
        pdatafile = open(pfile_path,'rb')
        pdata = pickle.load(pdatafile)
        pdatafile.close()
        if username in pdata:
            if los == 's':
                Set_LoginWindow(userlogin=0,usersignup=1)
            elif los == 'l' and password != pdata[username]['password']:
                Set_LoginWindow(userlogin=1,usersignup=0)
            elif los == 'l' and password == pdata[username]['password']:
                userDict = pdata
                Intro_Window()
        else:
            if los == 's':
                pdata[username] = adddict
                pdatafile = open(pfile_path,'wb')
                pickle.dump(pdata,pdatafile)
                pdatafile.close()
                userDict = pdata
                Intro_Window()
            elif los == 'l':
                Set_LoginWindow(userlogin=1,usersignup=0)
        
    else:
        copyfile(dfile_path,pfile_path)
        pdatafile = open(pfile_path,'rb')
        pdata = pickle.load(pdatafile)
        pdatafile.close()
        if username in pdata:
            if los == 's':
                Set_LoginWindow(userlogin=0,usersignup=1)
            elif los == 'l' and password != pdata[username]['password']:
                Set_LoginWindow(userlogin=1,usersignup=0)
            elif los == 'l' and password == pdata[username]['password']:
                userDict = pdata
                Intro_Window()
        else:
            if los == 's':
                pdata[username] = adddict
                pdatafile = open(pfile_path,'wb')
                pickle.dump(pdata,pdatafile)
                pdatafile.close()
                userDict = pdata
                Intro_Window()
            elif los == 'l':
                Set_LoginWindow(userlogin=1,usersignup=0)
    

def sortHscore(userDict):
    emptylist = []
    for user in userDict:
        if user != 'default' and user != 'Default':
            emptylist.append(userDict[user]['Hscore'])
    emptylist.sort(reverse=True)
    return emptylist


def checkDuplicates(sortedList):
    #0 no duplicate;1 duplicate 1,2;2 duplicate 2,3;
    #3 duplicate 1,3;4 duplicate 1,2,3
    duplicate = 0
    if len(sortedList) > 2: 
        if (sortedList[0] == sortedList[1]
        and sortedList[0] != sortedList[2]):
            duplicate = 1
        elif (sortedList[1] == sortedList[2]
        and sortedList[1] != sortedList[0]):
            duplicate = 2
        elif (sortedList[0] == sortedList[2]
        and sortedList[0] != sortedList[1]):
            duplicate = 3
        elif (sortedList[0] == sortedList[1]
        and sortedList[0] == sortedList[2]):
            duplicate = 4
        return duplicate
    elif len(sortedList) == 2:
        if(sortedList[0] == sortedList[1]):
            duplicate = 1
        return duplicate
    elif len(sortedList) == 1:
        return duplicate


def getHscore123(numListSorted,userDict,num,duplicate):
    if duplicate == 0:
        if num == 1:
            for user in userDict:
                if userDict[user]['Hscore'] == numListSorted[0]:
                    return userDict[user]
        elif num == 2:
            for user in userDict:
                if userDict[user]['Hscore'] == numListSorted[1]:
                    return userDict[user]
        elif num == 3:
            for user in userDict:
                if userDict[user]['Hscore'] == numListSorted[2]:
                    return userDict[user]
    elif duplicate == 1:
        if num == 1:
            for user in userDict:
                if userDict[user]['Hscore'] == numListSorted[0]:
                    return userDict[user]
        elif num == 2:
            count = 0
            for user in userDict:
                if (userDict[user]['Hscore'] == numListSorted[1]
                and count == 0):
                    count += 1
                elif userDict[user]['Hscore'] == numListSorted[1]:
                    return userDict[user]
        elif num == 3:
            for user in userDict:
                if userDict[user]['Hscore'] == numListSorted[2]:
                    return userDict[user]
    elif duplicate == 2:
        if num == 1:
            for user in userDict:
                if userDict[user]['Hscore'] == numListSorted[0]:
                    return userDict[user]
        elif num == 2:
            for user in userDict:
                if userDict[user]['Hscore'] == numListSorted[1]:
                    return userDict[user]
        elif num == 3:
            count = 0
            for user in userDict:
                if (userDict[user]['Hscore'] == numListSorted[2]
                and count == 0):
                    count += 1
                elif userDict[user]['Hscore'] == numListSorted[2]:
                    return userDict[user]        
    elif duplicate == 3:
        if num == 1:
            for user in userDict:
                if userDict[user]['Hscore'] == numListSorted[0]:
                    return userDict[user]
        elif num == 2:
            for user in userDict:
                if userDict[user]['Hscore'] == numListSorted[1]:
                    return userDict[user]
        elif num == 3:
            count = 0
            for user in userDict:
                if (userDict[user]['Hscore'] == numListSorted[2]
                and count == 0):
                    count += 1
                elif userDict[user]['Hscore'] == numListSorted[2]:
                    return userDict[user]        
    elif duplicate == 4:
        if num == 1:
            for user in userDict:
                if userDict[user]['Hscore'] == numListSorted[0]:
                    return userDict[user]
        elif num == 2:
            count = 0
            for user in userDict:
                if (userDict[user]['Hscore'] == numListSorted[1]
                and count == 0):
                    count += 1
                elif userDict[user]['Hscore'] == numListSorted[1]:
                    return userDict[user]        
        elif num == 3:
            count = 0
            for user in userDict:
                if (userDict[user]['Hscore'] == numListSorted[2]
                and count < 2):
                    count += 1
                elif userDict[user]['Hscore'] == numListSorted[2]:
                    return userDict[user]        


def convertToTime(seconds):
    minutes = int(seconds / 60)
    Seconds = seconds % 60
    strMinutes = '{:02d}'.format(minutes)
    strSeconds = '{:02d}'.format(Seconds)
    strMS = strMinutes + ':' + strSeconds
    return strMS


def playMusic(fileName):
    #Start load music file
    music = cwd + '/' + fileName
    pygame.mixer.init()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
    #End load music file


def stopMusic():
    pygame.mixer.music.stop()


def Set_LoginWindow(userlogin=0,usersignup=0):
    global userDict
    MW.fill(Colordict['SaddleBrown'])

    '''
    YG_Width, YG_Height = MW_Width,MW_Height/2
    YGsurf = pygame.Surface((YG_Width,YG_Height))
    YGsurf.fill(Colordict['yellowgreen'])
    MW.blit(YGsurf,(1,YG_Height))
    '''


    #Start Login Title Txt
    LTT = 'WELCOME TO THE FABULOUS GAME OF SNAKE' #Login Title Text
    LTTfs = (MW_Width * MW_Height)/35000 #fs = font size
    if LTTfs <= 30:
        LTTfs = LTTfs+10
    LTTfont = 'Times New Roman' #fonttype
    LTTtxtobj = New_Txt(LTT,LTTfont,int(LTTfs),'DarkKhaki',1,1) #T_txtobj = Title text object
    MW.blit(LTTtxtobj,(MW_Width/7,MW_Height/8))
    #END Login Title Txt


    #start Login Txt
    LT = 'SIGN IN - EXISTING USER'
    LTfs = (MW_Width * MW_Height)/60000 #fs = font size
    if LTfs <= 30:
        LTfs = LTfs+10
    LTfont = 'Times New Roman'
    LTtxtobj = New_Txt(LT,LTfont,int(LTfs),'DarkKhaki',0,0)
    MW.blit(LTtxtobj,(MW_Width/4.4,MW_Height/3.1))
    #end Login Txt


    #start sign up Txt
    SU = 'SIGN UP - NEW USER' #SU = sign up 
    SUfs = (MW_Width * MW_Height)/60000 #fs = font size
    if SUfs <= 30:
        SUfs = SUfs+10
    SUfont = 'Times New Roman'
    SUtxtobj = New_Txt(SU,SUfont,int(SUfs),'DarkKhaki',0,0)
    MW.blit(SUtxtobj,(MW_Width/1.85,MW_Height/3.1))
    #end Login Txt


    #start Login username Txt
    LTUN = 'Username' #LTUN = Login Txt Username 
    LTUNfs = (MW_Width * MW_Height)/120000 #fs = font size
    if LTUNfs <= 30:
        LTUNfs = LTUNfs+10
    LTUNfont = 'Times New Roman'
    LTUNtxtobj = New_Txt(LTUN,LTUNfont,int(LTUNfs),'yellow',0,0)
    MW.blit(LTUNtxtobj,(MW_Width/3.4,MW_Height/2.7))
    #end Login username Txt


    #start Login password Txt
    LPT = 'Password' #LPT = Login Password Txt 
    LPTfs = (MW_Width * MW_Height)/120000 #fs = font size
    if LPTfs <= 30:
        LPTfs = LPTfs+10
    LPTfont = 'Times New Roman'
    LPTtxtobj = New_Txt(LPT,LPTfont,int(LPTfs),'yellow',0,0)
    MW.blit(LPTtxtobj,(MW_Width/3.4,MW_Height/2.15))
    #end Login password Txt


    #start Sign Up username Txt
    SUUN = 'Username' #SUUN = Sign Up Username 
    SUUNfs = (MW_Width * MW_Height)/120000 #fs = font size
    if SUUNfs <= 30:
        SUUNfs = SUUNfs+10
    SUUNfont = 'Times New Roman'
    SUUNtxtobj = New_Txt(SUUN,SUUNfont,int(SUUNfs),'yellow',0,0)
    MW.blit(SUUNtxtobj,(MW_Width/1.68,MW_Height/2.7))
    #end Sign Up username Txt


    #start Sign Up password Txt
    SUPT = 'Password' #SUPT = Sign Up Password Txt
    SUPTfs = (MW_Width * MW_Height)/120000 #fs = font size
    if SUPTfs <= 30:
        SUPTfs = SUPTfs+10
    SUPTfont = 'Times New Roman'
    SUPTtxtobj = New_Txt(SUPT,SUPTfont,int(SUPTfs),'yellow',0,0)
    MW.blit(SUPTtxtobj,(MW_Width/1.68,MW_Height/2.15))
    #end Sign Up password Txt


    #Start Login Submit Button
    LSBtxt = 'SUBMIT' #LSB = Login Submit Button
    LSBtxtfs = (MW_Width * MW_Height)/150000 #fs = font size
    if LSBtxtfs <= 30:
        LSBtxtfs = LSBtxtfs+10
    LSBtxtfont = 'Times New Roman'
    LSBTO = New_Txt(LSBtxt,LSBtxtfont,int(LSBtxtfs),'black',1,0)

    Rect_Width,Rect_Height = MW_Width/16,MW_Height/34
    LSB_Pos = (MW_Width/3.38,MW_Height/1.78,Rect_Width,Rect_Height)
    LSB = Rect(LSB_Pos)
    LSB.txtobjpos = (MW_Width/3.38)+(Rect_Width*.12),(MW_Height/1.78)+(Rect_Height*.15)
    LSB.New_Button(MW,'khaki',1,LSBTO) #LSB = Login Submit Button
    #End Login Submit Button



    #Start Sign Up Submit Button
    SUSBtxt = 'SUBMIT' #LSB = Login Submit Button
    SUSBtxtfs = (MW_Width * MW_Height)/150000 #fs = font size
    if SUSBtxtfs <= 30:
        SUSBtxtfs = SUSBtxtfs+10
    SUSBtxtfont = 'Times New Roman'
    SUSBTO = New_Txt(SUSBtxt,SUSBtxtfont,int(SUSBtxtfs),'black',1,0)

    Rect_Width,Rect_Height = MW_Width/16,MW_Height/34
    SUSB_Pos = (MW_Width/1.67,MW_Height/1.78,Rect_Width,Rect_Height)
    SUSB = Rect(SUSB_Pos)
    SUSB.txtobjpos = (MW_Width/1.67)+(Rect_Width*.12),(MW_Height/1.78)+(Rect_Height*.15)
    SUSB.New_Button(MW,'khaki',1,SUSBTO) #LSB = Login Submit Button
    #End Sign Up Submit Button

    if usersignup == 1:
        #start Sign Up user already exists txt
        SUAE = 'USERNAME ALREADY EXISTS.' #SUPT = Sign Up User already exists
        SUAEfs = (MW_Width * MW_Height)/140000 #fs = font size
        if SUAEfs <= 30:
            SUAEfs = SUAEfs+10
        SUAEfont = 'Times New Roman'
        SUAEtxtobj = New_Txt(SUAE,SUAEfont,int(SUAEfs),'red',0,0)
        MW.blit(SUAEtxtobj,(MW_Width/1.4,MW_Height/2.35))

        SUAE2 = 'PLEASE CHOOSE A DIFFERENT NAME.'
        SUAE2fs = (MW_Width * MW_Height)/140000 #fs = font size
        if SUAE2fs <= 30:
            SUAE2fs = SUAE2fs+10
        SUAE2font = 'Times New Roman'
        SUAE2txtobj = New_Txt(SUAE2,SUAE2font,int(SUAE2fs),'red',0,0)
        MW.blit(SUAE2txtobj,(MW_Width/1.4,MW_Height/2.2))
        #end Sign Up user already exists txt


    if userlogin == 1:
        #start Login user does not exist txt
        SUAE = 'USER DOES NOT EXIST' #SUPT = Sign Up User already exists
        SUAEfs = (MW_Width * MW_Height)/140000 #fs = font size
        if SUAEfs <= 30:
            SUAEfs = SUAEfs+10
        SUAEfont = 'Times New Roman'
        SUAEtxtobj = New_Txt(SUAE,SUAEfont,int(SUAEfs),'red',0,0)
        MW.blit(SUAEtxtobj,(MW_Width/10,MW_Height/2.4))

        SUAE1 = 'OR'
        SUAE1fs = (MW_Width * MW_Height)/140000 #fs = font size
        if SUAE1fs <= 30:
            SUAE1fs = SUAE1fs+10
        SUAE1font = 'Times New Roman'
        SUAE1txtobj = New_Txt(SUAE1,SUAE1font,int(SUAE1fs),'red',0,0)
        MW.blit(SUAE1txtobj,(MW_Width/6.5,MW_Height/2.25))
        #end Login user does not exist txt
        
        SUAE2 = 'PASSWORD IS WRONG'
        SUAE2fs = (MW_Width * MW_Height)/140000 #fs = font size
        if SUAE2fs <= 30:
            SUAE2fs = SUAE2fs+10
        SUAE2font = 'Times New Roman'
        SUAE2txtobj = New_Txt(SUAE2,SUAE2font,int(SUAE2fs),'red',0,0)
        MW.blit(SUAE2txtobj,(MW_Width/10,MW_Height/2.1))
        #end Login user does not exist txt



    #Start Instructions Txt
    INT = "NOTE: USE TAB KEY TO TRAVERSE THE TEXT BOXES AND SUBMIT BUTTON." #Instructions Text
    INTfs = (MW_Width * MW_Height)/250000 #fs = font size
    if INTfs <= 30:
        INTfs = INTfs+10
    INTfont = 'Times New Roman' #fonttype
    INTtxtobj = New_Txt(INT,INTfont,int(INTfs),'palegoldenrod',0,0)
    MW.blit(INTtxtobj,(MW_Width/3.43,MW_Height/1.45))
    #END Instructions Title Txt


    #Start Instructions Txt 3
    INT3 = "USERNAME AND PASSWORD CAN BE UP TO 12 CHARACTERS." #Instructions Text
    INTfs3 = (MW_Width * MW_Height)/250000 #fs = font size
    if INTfs3 <= 30:
        INTfs3 = INTfs3+10
    INTfont3 = 'Times New Roman' #fonttype
    INTtxtobj3 = New_Txt(INT3,INTfont3,int(INTfs3),'palegoldenrod',0,0)
    MW.blit(INTtxtobj3,(MW_Width/3.1,MW_Height/1.4))
    #END Instructions Title Txt 3


    #Start Instructions Txt 4
    INT4 = "THEY CAN INCLUDE UPPER AND LOWERCASE LETTERS AND NUMBERS." #Instructions Text
    INTfs4 = (MW_Width * MW_Height)/250000 #fs = font size
    if INTfs4 <= 30:
        INTfs4 = INTfs4+10
    INTfont4 = 'Times New Roman' #fonttype
    INTtxtobj4 = New_Txt(INT4,INTfont4,int(INTfs4),'palegoldenrod',0,0)
    MW.blit(INTtxtobj4,(MW_Width/3.1,MW_Height/1.35))
    #END Instructions Title Txt 4


    #Start Instructions Txt 2
    INT2 = "PRESS THE RETURN KEY ON ONE OF THE SUBMIT BUTTONS. " #Instructions Text
    INTfs2 = (MW_Width * MW_Height)/250000 #fs = font size
    if INTfs2 <= 30:
        INTfs2 = INTfs2+10
    INTfont2 = 'Times New Roman' #fonttype
    INTtxtobj2 = New_Txt(INT2,INTfont2,int(INTfs2),'palegoldenrod',0,0)
    MW.blit(INTtxtobj2,(MW_Width/3.1,MW_Height/1.3))
    #END Instructions Title Txt 2


    Rect_Width,Rect_Height = MW_Width/12,MW_Height/28
    TB1pos = (MW_Width/3.5,MW_Height/2.5,Rect_Width,Rect_Height)
    TB1 = Rect(TB1pos)
    TB1.New_TxtBox(MW,'white',1)

    Rect_Width,Rect_Height = MW_Width/12,MW_Height/28
    TB2pos = (MW_Width/3.5,MW_Height/2.0,Rect_Width,Rect_Height)
    TB2 = Rect(TB2pos)
    TB2.New_TxtBox(MW,'white',0)

    Rect_Width,Rect_Height = MW_Width/12,MW_Height/28
    TB3pos = (MW_Width/1.7,MW_Height/2.5,Rect_Width,Rect_Height)
    TB3 = Rect(TB3pos)
    TB3.New_TxtBox(MW,'white',0)

    Rect_Width,Rect_Height = MW_Width/12,MW_Height/28
    TB4pos = (MW_Width/1.7,MW_Height/2.0,Rect_Width,Rect_Height)
    TB4 = Rect(TB4pos)
    TB4.New_TxtBox(MW,'white',0)

    TB1txt = ''
    TB2txt = ''
    TB3txt = ''
    TB4txt = ''
    TBfsize = (MW_Width * MW_Height)/80000

    while True:
        TB1.New_TxtBox(MW,'white')
        TB2.New_TxtBox(MW,'white')
        TB3.New_TxtBox(MW,'white')
        TB4.New_TxtBox(MW,'white')
        TB1txt = '%.12s' % TB1txt
        TB2txt = '%.12s' % TB2txt
        TB3txt = '%.12s' % TB3txt
        TB4txt = '%.12s' % TB4txt
        
        TB2txtShow = ''
        for t in TB2txt:
            TB2txtShow += 'x'
        TB4txtShow = ''
        for t in TB4txt:
            TB4txtShow += 'x'

        TB1txtobj = New_Txt(TB1txt,'Calibri',TBfsize,'black',0,0)
        TB2txtobj = New_Txt(TB2txtShow,'Calibri',TBfsize,'black',0,0)
        TB3txtobj = New_Txt(TB3txt,'Calibri',TBfsize,'black',0,0)
        TB4txtobj = New_Txt(TB4txtShow,'Calibri',TBfsize,'black',0,0)

        if TB1.outline == 1:
            MW.blit(TB1txtobj,(TB1.pos[0]+5,TB1.pos[1]+5))
            MW.blit(TB2txtobj,(TB2.pos[0]+5,TB2.pos[1]+5))
            MW.blit(TB3txtobj,(TB3.pos[0]+5,TB3.pos[1]+5))
            MW.blit(TB4txtobj,(TB4.pos[0]+5,TB4.pos[1]+5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Quit_Game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            Quit_Game()
                    elif event.key == pygame.K_TAB:
                        TB1.outline = 0
                        TB2.outline = 1
                    elif event.key == pygame.K_q:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_w:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_e:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_r:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_t:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_y:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_u:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_i:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_o:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_p:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_a:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_s:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_d:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_f:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_g:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_h:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_j:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_k:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_l:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_z:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_x:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_c:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_v:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_b:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_n:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_m:
                        if Get_Upper() == 1:
                            TB1txt+=chr(event.key).upper()
                        else:    
                            TB1txt+=chr(event.key)
                    elif event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        TB1txt+=chr(pygame.K_0)
                    elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        TB1txt+=chr(pygame.K_1)
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        TB1txt+=chr(pygame.K_2)
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        TB1txt+=chr(pygame.K_3)
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        TB1txt+=chr(pygame.K_4)
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        TB1txt+=chr(pygame.K_5)
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        TB1txt+=chr(pygame.K_6)
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        TB1txt+=chr(pygame.K_7)
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        TB1txt+=chr(pygame.K_8)
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        TB1txt+=chr(pygame.K_9)
                    elif event.key == pygame.K_BACKSPACE:
                        TB1txt = TB1txt[:-1]
                    elif event.key == pygame.K_RETURN:
                        done=False
        elif TB2.outline == 1:
            MW.blit(TB1txtobj,(TB1.pos[0]+5,TB1.pos[1]+5))
            MW.blit(TB2txtobj,(TB2.pos[0]+5,TB2.pos[1]+5))
            MW.blit(TB3txtobj,(TB3.pos[0]+5,TB3.pos[1]+5))
            MW.blit(TB4txtobj,(TB4.pos[0]+5,TB4.pos[1]+5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Quit_Game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Quit_Game()
                    elif event.key == pygame.K_TAB:
                            TB2.outline = 0
                            LSB.New_Button(MW,'khaki',2,LSBTO)
                    elif event.key == pygame.K_q:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_w:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_e:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_r:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_t:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_y:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_u:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_i:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_o:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_p:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_a:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_s:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_d:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_f:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_g:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_h:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_j:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_k:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_l:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_z:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_x:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_c:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_v:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_b:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_n:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_m:
                        if Get_Upper() == 1:
                            TB2txt+=chr(event.key).upper()
                        else:    
                            TB2txt+=chr(event.key)
                    elif event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        TB2txt+=chr(pygame.K_0)
                    elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        TB2txt+=chr(pygame.K_1)
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        TB2txt+=chr(pygame.K_2)
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        TB2txt+=chr(pygame.K_3)
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        TB2txt+=chr(pygame.K_4)
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        TB2txt+=chr(pygame.K_5)
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        TB2txt+=chr(pygame.K_6)
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        TB2txt+=chr(pygame.K_7)
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        TB2txt+=chr(pygame.K_8)
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        TB2txt+=chr(pygame.K_9)
                    elif event.key == pygame.K_BACKSPACE:
                        TB2txt = TB2txt[:-1]
                    elif event.key == pygame.K_RETURN:
                        done=False
        elif LSB.outline == 2:
            MW.blit(TB1txtobj,(TB1.pos[0]+5,TB1.pos[1]+5))
            MW.blit(TB2txtobj,(TB2.pos[0]+5,TB2.pos[1]+5))
            MW.blit(TB3txtobj,(TB3.pos[0]+5,TB3.pos[1]+5))
            MW.blit(TB4txtobj,(TB4.pos[0]+5,TB4.pos[1]+5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Quit_Game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Quit_Game()
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        Check_User(TB1txt,TB2txt,'l')
                    elif event.key == pygame.K_TAB:
                        LSB.New_Button(MW,'khaki',1,LSBTO)
                        TB3.outline = 1    
        elif TB3.outline == 1:
            MW.blit(TB1txtobj,(TB1.pos[0]+5,TB1.pos[1]+5))
            MW.blit(TB2txtobj,(TB2.pos[0]+5,TB2.pos[1]+5))
            MW.blit(TB3txtobj,(TB3.pos[0]+5,TB3.pos[1]+5))
            MW.blit(TB4txtobj,(TB4.pos[0]+5,TB4.pos[1]+5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Quit_Game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Quit_Game()
                    elif event.key == pygame.K_TAB:
                            TB3.outline = 0
                            TB4.outline = 1
                    elif event.key == pygame.K_q:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_w:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_e:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_r:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_t:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_y:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_u:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_i:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_o:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_p:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_a:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_s:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_d:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_f:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_g:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_h:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_j:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_k:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_l:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_z:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_x:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_c:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_v:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_b:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_n:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_m:
                        if Get_Upper() == 1:
                            TB3txt+=chr(event.key).upper()
                        else:    
                            TB3txt+=chr(event.key)
                    elif event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        TB3txt+=chr(pygame.K_0)
                    elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        TB3txt+=chr(pygame.K_1)
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        TB3txt+=chr(pygame.K_2)
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        TB3txt+=chr(pygame.K_3)
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        TB3txt+=chr(pygame.K_4)
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        TB3txt+=chr(pygame.K_5)
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        TB3txt+=chr(pygame.K_6)
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        TB3txt+=chr(pygame.K_7)
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        TB3txt+=chr(pygame.K_8)
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        TB3txt+=chr(pygame.K_9)
                    elif event.key == pygame.K_BACKSPACE:
                        TB3txt = TB3txt[:-1]
                    elif event.key == pygame.K_RETURN:
                        done=False
        elif TB4.outline == 1:
            MW.blit(TB1txtobj,(TB1.pos[0]+5,TB1.pos[1]+5))
            MW.blit(TB2txtobj,(TB2.pos[0]+5,TB2.pos[1]+5))
            MW.blit(TB3txtobj,(TB3.pos[0]+5,TB3.pos[1]+5))
            MW.blit(TB4txtobj,(TB4.pos[0]+5,TB4.pos[1]+5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Quit_Game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Quit_Game()
                    elif event.key == pygame.K_TAB:
                            TB4.outline = 0
                            SUSB.New_Button(MW,'khaki',2,SUSBTO)
                    elif event.key == pygame.K_q:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_w:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_e:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_r:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_t:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_y:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_u:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_i:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_o:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_p:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_a:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_s:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_d:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_f:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_g:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_h:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_j:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_k:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_l:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_z:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_x:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_c:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_v:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_b:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_n:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_m:
                        if Get_Upper() == 1:
                            TB4txt+=chr(event.key).upper()
                        else:    
                            TB4txt+=chr(event.key)
                    elif event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        TB4txt+=chr(pygame.K_0)
                    elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        TB4txt+=chr(pygame.K_1)
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        TB4txt+=chr(pygame.K_2)
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        TB4txt+=chr(pygame.K_3)
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        TB4txt+=chr(pygame.K_4)
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        TB4txt+=chr(pygame.K_5)
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        TB4txt+=chr(pygame.K_6)
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        TB4txt+=chr(pygame.K_7)
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        TB4txt+=chr(pygame.K_8)
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        TB4txt+=chr(pygame.K_9)
                    elif event.key == pygame.K_BACKSPACE:
                        TB4txt = TB4txt[:-1]
                    elif event.key == pygame.K_RETURN:
                        done=False
        elif SUSB.outline == 2:
            MW.blit(TB1txtobj,(TB1.pos[0]+5,TB1.pos[1]+5))
            MW.blit(TB2txtobj,(TB2.pos[0]+5,TB2.pos[1]+5))
            MW.blit(TB3txtobj,(TB3.pos[0]+5,TB3.pos[1]+5))
            MW.blit(TB4txtobj,(TB4.pos[0]+5,TB4.pos[1]+5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Quit_Game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Quit_Game()
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        Check_User(TB3txt,TB4txt,'s')
                    elif event.key == pygame.K_TAB:
                        TB1.outline = 1
                        SUSB.New_Button(MW,'khaki',1,SUSBTO) 
        pygame.display.update()


def Intro_Window():
    MW.fill(Colordict['Sienna'])

    #Start Intro Title Txt
    Title_txt = '"LET\'S PLAY SNAKE"'
    fts = (MW_Width * MW_Height)/48000 #fts = font title size
    if fts <= 30:
        fts = fts+10
    ftype = 'Times New Roman' #fonttype
    fcolor = 'gold' #fontcolor
    T_txtobj = New_Txt(Title_txt,ftype,int(fts),fcolor,1,1) #T_txtobj = Title text object
    MW.blit(T_txtobj,(MW_Width/2.8,MW_Height/5.4))
    #END Intro Title Txt


    #New fontobject for buttons
    fbs = (MW_Width * MW_Height)/54000 #font button size
    if fbs <= 30:
        fbs = fbs+9
    ftype = 'Times New Roman' #fonttype
    fcolor = 'gold' #fontcolor
    B1TO = New_Txt('Easy',ftype,int(fbs),fcolor,1,0) #Button 1 TextObject
    B2TO = New_Txt('Hard',ftype,int(fbs),fcolor,1,0) #Button 2 TextObject
    B3TO = New_Txt('Quit',ftype,int(fbs),fcolor,1,0) #Button 3 TextObject

    #New Rec/Button Positions
    Rect_Width,Rect_Height = MW_Width/7.7,MW_Height/15.5
    B1_Pos = (MW_Width/2.5,MW_Height/2.5,Rect_Width,Rect_Height) #B1 = Button1
    B2_Pos = (MW_Width/2.5,MW_Height/1.9,Rect_Width,Rect_Height) 
    B3_Pos = (MW_Width/2.5,MW_Height/1.53,Rect_Width,Rect_Height)

    #New Rect objects
    B1 = Rect(B1_Pos)
    B2 = Rect(B2_Pos)
    B3 = Rect(B3_Pos)

    #Set Buttons
    B1.New_Button(MW,'DarkGoldenrod',2,txt=B1TO)
    B2.New_Button(MW,'DarkGoldenrod',1,txt=B2TO)
    B3.New_Button(MW,'DarkGoldenrod',1,txt=B3TO)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Quit_Game()
            elif event.type == pygame.KEYDOWN:
                if event.key == (pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and B3.outline == 2:
                    Quit_Game()
                elif event.key == (pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and B1.outline == 2:
                    Play_Snake()
                elif event.key == pygame.K_ESCAPE:
                    Quit_Game()
                elif event.key == pygame.K_DOWN:
                    if B1.outline == 2:
                        B1.New_Button(MW,'DarkGoldenrod',1,txt=B1TO)
                        B2.New_Button(MW,'DarkGoldenrod',2,txt=B2TO)
                    elif B2.outline == 2:                    
                        B2.New_Button(MW,'DarkGoldenrod',1,txt=B2TO)
                        B3.New_Button(MW,'DarkGoldenrod',2,txt=B3TO)
                    elif B3.outline == 2:
                        B1.New_Button(MW,'DarkGoldenrod',2,txt=B1TO)
                        B3.New_Button(MW,'DarkGoldenrod',1,txt=B3TO)
                elif event.key == pygame.K_UP: 
                    if B1.outline == 2:
                        B1.New_Button(MW,'DarkGoldenrod',1,txt=B1TO)
                        B3.New_Button(MW,'DarkGoldenrod',2,txt=B3TO)
                    elif B2.outline == 2:
                        B1.New_Button(MW,'DarkGoldenrod',2,txt=B1TO)
                        B2.New_Button(MW,'DarkGoldenrod',1,txt=B2TO)
                    elif B3.outline == 2:
                        B2.New_Button(MW,'DarkGoldenrod',2,txt=B2TO)
                        B3.New_Button(MW,'DarkGoldenrod',1,txt=B3TO)
            elif event.type == pygame.MOUSEMOTION:
                B1MT = B1.rect.collidepoint(pygame.mouse.get_pos()) #B1MT = Button 1 Mouse Test
                B2MT = B2.rect.collidepoint(pygame.mouse.get_pos()) #B2MT = Button 2 Mouse Test
                B3MT = B3.rect.collidepoint(pygame.mouse.get_pos()) #B2MT = Button 3 Mouse Test
                if B1MT == 1:
                    B1.New_Button(MW,'DarkKhaki',txt=B1TO)
                    B2.New_Button(MW,'DarkGoldenrod',txt=B2TO)
                    B3.New_Button(MW,'DarkGoldenrod',txt=B3TO)
                elif B2MT ==1:
                    B1.New_Button(MW,'DarkGoldenrod',txt=B1TO)
                    B2.New_Button(MW,'DarkKhaki',txt=B2TO)
                    B3.New_Button(MW,'DarkGoldenrod',txt=B3TO)
                elif B3MT ==1:
                    B1.New_Button(MW,'DarkGoldenrod',txt=B1TO)
                    B2.New_Button(MW,'DarkGoldenrod',txt=B2TO)
                    B3.New_Button(MW,'DarkKhaki',txt=B3TO)
                else:
                    B1.New_Button(MW,'DarkGoldenrod',txt=B1TO)
                    B2.New_Button(MW,'DarkGoldenrod',txt=B2TO)
                    B3.New_Button(MW,'DarkGoldenrod',txt=B3TO)
        pygame.display.update()            


def Play_Snake():
    global userDict
    #ssize = 10 #snake size based on radius
    #fsize = ssize - 2 #food size based on radius 


    #Start snake start position
    PH = [274,200]
    P1 = [PH[0]-sizeB2cc,200]
    P2 = [P1[0]-sizeB2cc,200]
    P3 = [P2[0]-sizeB2cc,200]
    P4 = [P3[0]-sizeB2cc,200]
    P5 = [P4[0]-sizeB2cc,200]
    P6 = [P5[0]-sizeB2cc,200]
    P7 = [P6[0]-sizeB2cc,200]
    P8 = [P7[0]-sizeB2cc,200]
    P9 = [P8[0]-sizeB2cc,200]
    P10 = [P9[0]-sizeB2cc,200]
    P11 = [P10[0]-sizeB2cc,200]
    P12 = [P11[0]-sizeB2cc,200]
    P13 = [P12[0]-sizeB2cc,200]
    P14 = [P13[0]-sizeB2cc,200]

    SP = [PH,P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14]
    dir = 'Right'
    #End snake start position


    playMusic('Scott_HolmesHappyEnding.mp3')
    '''
    #Start load music file
    music = cwd + '/Scott_HolmesHappyEnding.mp3'
    pygame.mixer.init()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
    #End load music file
    '''

    foodpos = food.Make_Food(ate=1) #Randomize food starting position
    score = 0 #Start set score to 0
    fps = pygame.time.Clock() #Create fps clock
    now = time()
    timeCounter = 1

    #Start Main Game Loop
    while True:
        fps.tick(fpsint)
        MW.fill(Colordict['SaddleBrown'])
        Score_Screen.Set_ScoreScreen(score,timeCounter)
        snake.Draw_Snake(SP)
        food.Draw_Food(foodpos)
        foodpos, SP, score = ChangeSnake.Ate_Food(SP,foodpos,dir,score)
        ChangeSnake.Test_Collision(SP,score,timeCounter)
        pygame.display.update()
        cdir = dir
        dir, SP = snake.Move_Snake(SP,dir,cdir,score,timeCounter)

        if time() >= now + timeCounter:
            timeCounter += 1
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Quit_Game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        Quit_Game()
                elif event.key == pygame.K_RIGHT:
                    dir, SP = snake.Move_Snake(SP,'Right',cdir,score,timeCounter)

                elif event.key == pygame.K_DOWN:
                    dir, SP = snake.Move_Snake(SP,'Down',cdir,score,timeCounter)

                elif event.key == pygame.K_LEFT:
                    dir, SP = snake.Move_Snake(SP,'Left',cdir,score,timeCounter)

                elif event.key == pygame.K_UP:
                    dir, SP = snake.Move_Snake(SP,'Up',cdir,score,timeCounter)
    #End Main Game Loop


def gameOver(userEntry,userEntry1=userEntryDefault,userEntry2=userEntryDefault,userEntry3=userEntryDefault):
    stopMusic()
    MW.fill(Colordict['SaddleBrown'])#SaddleBrown / Sienna
    
    #Start Game Over TXT
    GOT = '===============================GAME OVER====================================' #Login Title Text
    GOTfs = (MW_Width * MW_Height)/48000 #fs = font size
    if GOTfs <= 30:
        GOTfs = GOTfs+10
    GOTfont = 'Times New Roman' #fonttype
    GOTtxtobj = New_Txt(GOT,GOTfont,int(GOTfs),'DarkKhaki',1,1) #T_txtobj = Title text object
    MW.blit(GOTtxtobj,(MW_Width/MW_Width,MW_Height/8))
    #END Game Over Txt    

    #Start name txt
    NT = 'Name' #Login Title Text
    NTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if NTfs <= 30:
        NTfs = NTfs+10
    NTfont = 'Times New Roman' #fonttype
    NTtxtobj = New_Txt(NT,NTfont,int(NTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(NTtxtobj,(MW_Width/5,MW_Height/4))
    pygame.draw.line(MW,Colordict['DarkKhaki'],(MW_Width/5.1,MW_Height/3.45),(MW_Width/3.6,MW_Height/3.45),3)
    #END name Txt
    
    #Start score txt
    ST = 'Score' #Login Title Text
    STfs = (MW_Width * MW_Height)/50000 #fs = font size
    if STfs <= 30:
        STfs = STfs+10
    STfont = 'Times New Roman' #fonttype
    STtxtobj = New_Txt(ST,STfont,int(STfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(STtxtobj,(MW_Width/2.3,MW_Height/4))
    pygame.draw.line(MW,Colordict['DarkKhaki'],(MW_Width/2.3,MW_Height/3.45),(MW_Width/1.98,MW_Height/3.45),3)
    #END score Txt

    #Start time txt
    TT = 'Time' #Login Title Text
    TTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if TTfs <= 30:
        TTfs = TTfs+10
    TTfont = 'Times New Roman' #fonttype
    TTtxtobj = New_Txt(TT,TTfont,int(TTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(TTtxtobj,(MW_Width/1.4,MW_Height/4))
    pygame.draw.line(MW,Colordict['DarkKhaki'],(MW_Width/1.4,MW_Height/3.45),(MW_Width/1.28,MW_Height/3.45),3)
    #END time Txt

    #Start playername txt
    PT = userEntry['username'] #Login Title Text
    PTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if PTfs <= 30:
        PTfs = PTfs+10
    PTfont = 'Times New Roman' #fonttype
    PTtxtobj = New_Txt(PT,PTfont,int(PTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(PTtxtobj,(MW_Width/4.8,MW_Height/3.0))
    #END playername Txt

    #Start playerscore txt
    PST = str(userEntry['Hscore']) #Login Title Text
    PSTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if PSTfs <= 30:
        PSTfs = PSTfs+10
    PSTfont = 'Times New Roman' #fonttype
    PSTtxtobj = New_Txt(PST,PSTfont,int(PSTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(PSTtxtobj,(MW_Width/2.2,MW_Height/3.0))
    #END playerscore Txt

    #Start playertime txt
    PST = str(userEntry['time']) #Login Title Text
    PSTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if PSTfs <= 30:
        PSTfs = PSTfs+10
    PSTfont = 'Times New Roman' #fonttype
    PSTtxtobj = New_Txt(PST,PSTfont,int(PSTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(PSTtxtobj,(MW_Width/1.37,MW_Height/3.0))
    #END playertime Txt    

    #Start Top Player TXT
    GOT = '================================Top 3 Players====================================' #Login Title Text
    GOTfs = (MW_Width * MW_Height)/48000 #fs = font size
    if GOTfs <= 30:
        GOTfs = GOTfs+10
    GOTfont = 'Times New Roman' #fonttype
    GOTtxtobj = New_Txt(GOT,GOTfont,int(GOTfs),'DarkKhaki',1,1) #T_txtobj = Title text object
    MW.blit(GOTtxtobj,(MW_Width/MW_Width,MW_Height/2.1))
    #END Top Player Txt

    #Start Topplayername1 txt
    PT = userEntry1['username'] #Login Title Text
    PTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if PTfs <= 30:
        PTfs = PTfs+10
    PTfont = 'Times New Roman' #fonttype
    PTtxtobj = New_Txt(PT,PTfont,int(PTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(PTtxtobj,(MW_Width/4.8,MW_Height/1.8))
    #END Topplayername1 Txt

    #Start Topplayerscore1 txt
    PST = str(userEntry1['Hscore']) #Login Title Text
    PSTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if PSTfs <= 30:
        PSTfs = PSTfs+10
    PSTfont = 'Times New Roman' #fonttype
    PSTtxtobj = New_Txt(PST,PSTfont,int(PSTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(PSTtxtobj,(MW_Width/2.2,MW_Height/1.8))
    #END Topplayerscore1 Txt

    #Start topplayertime1 txt
    PST = str(userEntry1['time']) #Login Title Text
    PSTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if PSTfs <= 30:
        PSTfs = PSTfs+10
    PSTfont = 'Times New Roman' #fonttype
    PSTtxtobj = New_Txt(PST,PSTfont,int(PSTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(PSTtxtobj,(MW_Width/1.37,MW_Height/1.8))
    #END topplayertime1 Txt

    #Start Topplayername2 txt
    PT = userEntry2['username'] #Login Title Text
    PTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if PTfs <= 30:
        PTfs = PTfs+10
    PTfont = 'Times New Roman' #fonttype
    PTtxtobj = New_Txt(PT,PTfont,int(PTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(PTtxtobj,(MW_Width/4.8,MW_Height/1.55))
    #END Topplayername1 Txt

    #Start Topplayerscore2 txt
    PST = str(userEntry2['Hscore']) #Login Title Text
    PSTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if PSTfs <= 30:
        PSTfs = PSTfs+10
    PSTfont = 'Times New Roman' #fonttype
    PSTtxtobj = New_Txt(PST,PSTfont,int(PSTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(PSTtxtobj,(MW_Width/2.2,MW_Height/1.55))
    #END Topplayerscore2 Txt

    #Start topplayertime2 txt
    PST = str(userEntry2['time']) #Login Title Text
    PSTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if PSTfs <= 30:
        PSTfs = PSTfs+10
    PSTfont = 'Times New Roman' #fonttype
    PSTtxtobj = New_Txt(PST,PSTfont,int(PSTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(PSTtxtobj,(MW_Width/1.37,MW_Height/1.55))
    #END topplayertime2 Txt

    #Start Topplayername3 txt
    PT = userEntry3['username'] #Login Title Text
    PTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if PTfs <= 30:
        PTfs = PTfs+10
    PTfont = 'Times New Roman' #fonttype
    PTtxtobj = New_Txt(PT,PTfont,int(PTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(PTtxtobj,(MW_Width/4.8,MW_Height/1.35))
    #END Topplayername3 Txt

    #Start Topplayerscore3 txt
    PST = str(userEntry3['Hscore']) #Login Title Text
    PSTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if PSTfs <= 30:
        PSTfs = PSTfs+10
    PSTfont = 'Times New Roman' #fonttype
    PSTtxtobj = New_Txt(PST,PSTfont,int(PSTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(PSTtxtobj,(MW_Width/2.2,MW_Height/1.35))
    #END Topplayerscore3 Txt

    #Start topplayertime3 txt
    PST = str(userEntry3['time']) #Login Title Text
    PSTfs = (MW_Width * MW_Height)/50000 #fs = font size
    if PSTfs <= 30:
        PSTfs = PSTfs+10
    PSTfont = 'Times New Roman' #fonttype
    PSTtxtobj = New_Txt(PST,PSTfont,int(PSTfs),'DarkKhaki',0,0) #T_txtobj = Title text object
    MW.blit(PSTtxtobj,(MW_Width/1.37,MW_Height/1.35))
    #END topplayertime3 Txt
    
    GOBT = 'MAIN MENU'
    GOBTfs = (MW_Width * MW_Height)/95000 #fs = font size
    if GOBTfs <= 30:
        GOBTfs = GOBTfs+10
    GOBTfont = 'Times New Roman'
    GOBTobj = New_Txt(GOBT,GOBTfont,int(GOBTfs),'yellow',1,0)

    Rect_Width,Rect_Height = MW_Width/7.7,MW_Height/15.5
    GOBpos = (MW_Width/2.42,MW_Height/1.2,Rect_Width,Rect_Height)
    GOB = Rect(GOBpos)
    GOB.txtobjpos = (MW_Width/2.42)+(Rect_Width*.12),(MW_Height/1.2)+(Rect_Height*.23)
    GOB.New_Button(MW,'Peru',2,GOBTobj)
    
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Quit_Game()
            elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            Quit_Game()
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        Intro_Window()

##################################################CLASSES AND DEFINITIONS#################################################
pygame.init()
Set_LoginWindow(0,0)
