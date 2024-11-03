import IdeaAPIgIRON
import time
import sys
#計測スタート
all_do_start = time.time()



#渡す過程で出てくるじゃまなブロックを削除する
def deleteObjectStr(content:str):
    deletes = ["<",">","sys","SYS","INST","[","]","/","s>"]
    res = content
    for i in deletes:
        res = str(res).replace(i,"")
    return res

#list-text
def list_change_text(content:list):
    res = ""
    for i in content:
        res += i
    return res

def print_do_time(start_time,option):
    end_time=time.time()
    print(option,"かかった時間{:.2f}".format(end_time-start_time))



#Auto Test Mode
themes = "セキュリティーの価値はどこに宿るか?"


#Propaty
member = ['A','B','C','D','E','F','G','H','I','J','K','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
member_response = []
useMember = 3
turn= 2

#PROPATY-CHEACK
if useMember > len(member):
    sys.exit('ERROR:USE-MEMBER-OVER')
elif useMember == 0:
    sys.exit('ERROR:Not SET USE-MEMBER')

#makeMember_responseList
for i in range(useMember):
    member_response.append('')




#議論の種
rec_time_s = time.time()

IdeaAPIgIRON.SetSystemPrompt("あなたはプロの議論者,カムスキーさんです。")
giron_seed = deleteObjectStr(IdeaAPIgIRON.Outputs_custom(themes))
print(giron_seed)

print_do_time(rec_time_s,"gron_seed:")

#議論の種使用したか?
use_first = 0

giron_all_texts = []


#議論-本体(基本反論がメイン)
for i in range(turn):
    for m in range(useMember):
        return_crithikl_think_time = time.time()
        # IdeaAPIgIRON.SetSystemPrompt("あなたはプロの議論者"+member[m]+"さんです。"+"これから"+member[m-1]+"さんから来た回答に対して反論してください。また反論ができない場合は別の視点から意見を述べてください。また論点は"+themes+"です")

        #議論の種を使用したか
        if use_first == 0:
            IdeaAPIgIRON.SetSystemPrompt("あなたはプロの議論者"+member[m]+"さんです。これからカムスキーさんから来た回答に対して反論してください。また反論ができない場合は別の視点から意見を述べてください。また論点は"+themes+"です")
            member_response[m] = deleteObjectStr(IdeaAPIgIRON.Outputs_custom(giron_seed))
            use_first = 1

        #最初の人にローテーションが回ってきたら?
        elif m-1 < 0:
            IdeaAPIgIRON.SetSystemPrompt("あなたはプロの議論者"+member[m]+"さんです。"+"これから"+member[useMember-1]+"さんから来た回答に対して反論してください。また反論ができない場合は別の視点から意見を述べてください。また論点は"+themes+"です")
            member_response[m] = deleteObjectStr(IdeaAPIgIRON.Outputs_custom(member_response[useMember-1]))
        
        #通常のローテーション
        else:
            IdeaAPIgIRON.SetSystemPrompt("あなたはプロの議論者"+member[m]+"さんです。"+"これから"+member[m-1]+"さんから来た回答に対して反論してください。また反論ができない場合は別の視点から意見を述べてください。また論点は"+themes+"です")
            member_response[m] = deleteObjectStr(IdeaAPIgIRON.Outputs_custom(member_response[m-1]))
        
        #議事録作成
        giron_all_texts.append(member_response[m])

        print(f"{member[m]}さん:{member_response[m]}")

        print_do_time(return_crithikl_think_time,"議論の一人の時間:")

#議事録まとめ
giron_text = list_change_text(giron_all_texts)



#議論の結論
giron_end_time = time.time()

IdeaAPIgIRON.SetSystemPrompt("あなたはプロの議論者"+member[m]+"さんです。"+"これから渡す議事録より結論を教えてください。")
giron_end = deleteObjectStr(IdeaAPIgIRON.Outputs_custom(giron_text))
print(f"結論:{giron_end}")

print(giron_end_time,"結論が出るまでの時間:")

#SAVE
IdeaAPIgIRON.PromptSave()

all_do_end = time.time()
print("全ての演算に使用した時間:{:.2f}".format(all_do_end-all_do_start))
