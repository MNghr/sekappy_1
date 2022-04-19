import numpy as np
import PySimpleGUI as sg
import GUI
import utility

#イベントループ
def main():
    while True:
        event, values = GUI.interface.getWindow().read()

        if event == sg.WIN_CLOSED or event == None:
            break

        if event == 'quit':
            break

        if event == 'doDiceRoll':
            result = None
            amount = None
            numberOfFaces = None
            participant = None
            try:
                amount = int(values['amountOfDice'])
                numberOfFaces = int(values['numberOfFaces'])
                participant = int(values['participant'])
                result=utility.diceRoll(amount=amount,numberOfFaces=numberOfFaces,participant=participant)
            except:
                sg.popup_cancel('テキストボックスに不正な値が入力されています')
            else:
                GUI.interface.move2DiceRollMode(participant,numberOfFaces=numberOfFaces,amountOfDice=amount,result=result)

        if event == 'reRoll':
            GUI.interface.reRoll()

        if event == 'move2InputMode':
            GUI.interface.move2InputMode()

        if event == 'numberOfFaces' or event == 'amountOfDice':
            try:
                GUI.interface.updateElement(event,''.join(utility.bindText2Integer(values[event])))
            except Exception as e:
                sg.popup_cancel('''※開発者向け
                エラー箇所:numberOfFaces,amountOfDiceのイベント中，正規表現処理時
                エラーメッセージ:
                '''+str(e))
            
            try :
                if GUI.UPPER_DIGIT[event] < len(values[event]):
                    GUI.interface.updateElement(event,values[event][:-1])
            except:
                sg.popup_cancel('''※開発者向け
                エラー箇所:numberOfFaces,amountOfDiceのイベント中，if(UPPER_DIGIT[event] < len(values[event])処理時
                ''')



        if event in ('detail1P','detail2P'):
            try:
                GUI.interface.invokeDetail(int(event[-2]))
            except Exception as e:
                sg.popup_cancel('''※開発者向け
                エラー箇所:detailのイベント中，invokeDetail処理時
                ''')
                print(e)
            else:
                while True:
                    subEvent,subValues = GUI.interface.getSubWindow().read()

                    if subEvent in ('quitSubWindow',sg.WIN_CLOSED,None):
                        break
                GUI.interface.finishSubWindow()




main()
