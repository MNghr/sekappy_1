import PySimpleGUI as sg
import copy
import numpy as np
import utility

np.set_printoptions(threshold=10000,linewidth=1)

UPPER_DIGIT={}
UPPER_DIGIT['amountOfDice'] = 3
UPPER_DIGIT['numberOfFaces'] = 3

PLAYER_NAME = ['あなた','対戦相手']
DETAIL_KEY = ['detail1P','detail2P']
RESULT_KEY = ['result1P','result2P']

LAYOUT_DICEROLL_MODE_PREFIX = [
    [sg.Column([
        [sg.Text('ダイスロール結果',font=('Noto Serif CJK JP',15,'bold'))]
    ],justification='center')
    ]
]

LAYOUT_DICEROLL_MODE_SUFFIX = [
    [sg.Column([
        [sg.Button('もう一回ふる',key='reRoll'),sg.Button('設定を変える',key='move2InputMode'),sg.Button('アプリを閉じる',key='quit')]
    ],justification='center')
    ]
]

LAYOUT_INPUT_MODE = [
    [sg.Text('参加人数'),sg.Combo((1,2),default_value=1,key='participant')],
    [sg.Text('サイコロの面数'),sg.InputText(default_text='6',enable_events=True,key='numberOfFaces',size=(UPPER_DIGIT['numberOfFaces'],1)),],
    [sg.Text('サイコロの数'),sg.InputText(default_text='2',enable_events=True,key='amountOfDice',size=(UPPER_DIGIT['amountOfDice'],1))],
    [sg.Button('Dice Roll!',key='doDiceRoll'),sg.Button('アプリを閉じる',key='quit')]
]



APPLICATION_NAME = 'DiceRollSimulator'


class GUI():
    __selfdiceRollWindow = None
    __inputWindow = None
    __layoutDiceRollMode = None
    __layoutInputMode = None
    __currentWindow = None
    __lastParticipant = 1
    __lastNumberOfFaces = 6
    __lastAmountOfDice = 2
    __lastResult = None
    __subWindow = None
    
    def __init__(self):
        self.__currentWindow = self.makeInputWindow()

    def makeInputWindow(self):
        layout = copy.deepcopy(LAYOUT_INPUT_MODE) 
        return sg.Window(APPLICATION_NAME+':各種設定',layout)

    def makeDiceRollWindow(self,numberOfParticipants=1,numberOfFaces=6,amountOfDice=2,result=np.zeros((1,1))):
        layout = copy.deepcopy(LAYOUT_DICEROLL_MODE_PREFIX)
        layout.append(list([sg.Column([
            [sg.Text('サイコロの面数:'+str(numberOfFaces)+'面,サイコロの数:'+str(amountOfDice)+'個')]
        ],justification='center')]))
        mainContentColumn = [[]]

        playerFrame = []
        for i in range(numberOfParticipants):
            playerFrame.append( 
                sg.Frame(PLAYER_NAME[i],[
                    [sg.Column([
                        [sg.Text(str(result[:,i].sum()),key=RESULT_KEY[i],font=('Noto Serif CJK JP',35))]
                    ],justification='center')],
                    [sg.Column([
                        [sg.Button('詳細確認',key=DETAIL_KEY[i])]
                    ],justification='center')],
                ])
            )  

        for i in range(numberOfParticipants):
            mainContentColumn[0].append(playerFrame[i])
   
        layout.append(list([sg.Column(mainContentColumn,justification='center')]))
        layout.extend(copy.deepcopy(LAYOUT_DICEROLL_MODE_SUFFIX))

        return sg.Window(APPLICATION_NAME+':ダイスロール結果',layout)

    def move2DiceRollMode(self,numberOfParticipants=1,numberOfFaces=6,amountOfDice=2,result=np.zeros((1,1))):
        self.__lastParticipant = numberOfParticipants
        self.__lastNumberOfFaces = numberOfFaces
        self.__lastAmountOfDice = amountOfDice
        self.__lastResult = copy.deepcopy(result)

        self.__currentWindow.close()
        self.__currentWindow = self.makeDiceRollWindow(numberOfParticipants=numberOfParticipants,numberOfFaces=numberOfFaces,amountOfDice=amountOfDice,result=result)
        #self.__currentWindow['result1P'].update(str(result[:,0]))

        #if numberOfParticipants == 2:
        #    self.__currentWindow[1].update()

    def reRoll(self):
        result = utility.diceRoll(amount=self.__lastAmountOfDice,participant = self.__lastParticipant,numberOfFaces=self.__lastNumberOfFaces)
        self.move2DiceRollMode(numberOfParticipants = self.__lastParticipant,numberOfFaces=self.__lastNumberOfFaces,amountOfDice=self.__lastAmountOfDice,result = result)


    def move2InputMode(self):
        self.__currentWindow.close()
        self.__currentWindow = self.makeInputWindow()

    def makeDetailSubWindow(self,participantIndex):
        participantIndex -= 1
        PLAYER_NAME = ['あなた','対戦相手']
        contentColumn = [
            [sg.Text(PLAYER_NAME[participantIndex]+'の各サイコロの出目')],
            [sg.Text('サイコロの面数:'+str(self.__lastNumberOfFaces)+'面, サイコロの数:'+str(self.__lastAmountOfDice))],
        ]
        
        layout = [
            [sg.Column(contentColumn)],
            [sg.Column([
                [sg.Text(utility.makeDiceRollDetailString(self.__lastResult[:,participantIndex]))]
                ],scrollable=True,vertical_scroll_only=True,justification='center',size=(None,50),expand_y=True)
            ],
            [sg.Column([
                [sg.Button('この画面を閉じる',key='quitSubWindow')]
                ],justification='center')
            ],
            
        ]

        return sg.Window(PLAYER_NAME[participantIndex]+'の各サイコロの出目',layout,resizable=True)

    def invokeDetail(self,participantIndex):
        self.__subWindow = self.makeDetailSubWindow(participantIndex)
    
    def finishSubWindow(self):
        self.__subWindow.close()

    def getWindow(self):
        return self.__currentWindow

    def getSubWindow(self):
        return self.__subWindow
    
    def getLastResult(self):
        return self.__lastResult
    
    def updateElement(self,keyOfElement: str,newValue: str):
        try:
            self.__currentWindow[keyOfElement].update(newValue)

        except:
            sg.popup_cancel('''※開発者向け
            おそらくキー文字列の値が不正です
            エラー箇所:GUI::updateElement()
            ''')
        else:
            pass



interface = GUI()