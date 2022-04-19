import re
import numpy as np

#正規表現に含まれない入力を除去する
def bindText2RE(targetString,pattern)->[str]:
    return re.findall(pattern,targetString)
   

#テキストボックスへの入力を整数のみに制限する
def bindText2Integer(targetString="")->[str]:
    return bindText2RE(targetString=targetString,pattern = r'([1-9][0-9]*)')

def diceRoll(amount=2,numberOfFaces=6,participant = 1):
    return np.random.randint(1,numberOfFaces+1,size=(amount,participant))

def makeDiceRollDetailString(target:np.ndarray):
    output = ''
    for index,d in enumerate(target.tolist()):
        output += '{:>4}つめ: {:>4}\n'.format(index+1,d)
    return output