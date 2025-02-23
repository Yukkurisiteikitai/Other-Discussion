import time
import aiAPI.IdeaAPIgIRON as IdeaAPIgIRON
from Toolfunction.deleteObject import deleteObjectStr
from Toolfunction.TextConverter import ListChangeText
from Toolfunction.Loadquestion import LoadQuestion


#Propaty
member = ['A','B','C','D','E','F','G','H','I','J','K','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
member_response = []
useMember = 3
turn= 3
themes = ""

# 質問の設定
conversation_history = []
SystemPrompt = "あなたは優秀なサポーターです。目的は一つのテーマを様々な観点から見ることでそのテーマを分析すること。そのテーマをその観点からみたらどうなるかを教えてください。"

#SaveDatas
save_data = []
save_path = "../log/log.jsonl"

#議論の種使用したか?
use_first = 0
giron_all_texts = []
question = []

#時間計測
def print_do_time(start_time,option):
    end_time=time.time()
    print(option+"かかった時間{:.2f}".format(end_time-start_time))








def giron(themes):
    global use_first,member_response,member,giron_text,giron_all_texts
    giron_start_time = time.time()

    #議論の種
    rec_time_s = time.time()

    IdeaAPIgIRON.SetSystemPrompt("あなたはプロの議論者,カムスキーさんです。")
    giron_seed = deleteObjectStr(IdeaAPIgIRON.Outputs_custom(themes))
    print(giron_seed)

    print_do_time(rec_time_s,"gron_seed:")

    for i in range(turn):
            for m in range(useMember):
                member_response.append("")

                print(f"turn:{i},member:{m}")
                return_crithikl_think_time = time.time()

                #議論の種を使用したか
                if use_first == 0:
                    IdeaAPIgIRON.SetSystemPrompt("あなたはプロの議論者"+member[m]+"さんです。これからカムスキーさんから来た回答に対して反論してください。また反論ができない場合は別の視点から意見を述べてください。また論点は"+themes+"です")
                    member_response[m] = deleteObjectStr(IdeaAPIgIRON.Outputs_custom(giron_seed))
                    use_first = 1

                #最初の人にローテーションが回ってきたら?
                elif m-1 < 0:
                    IdeaAPIgIRON.SetSystemPrompt("あなたはプロの議論者"+member[m]+"さんです。"+"これから"+member[useMember-1]+"さんから来た回答に対して反論してください。また反論ができない場合は別の視点から意見を述べてください。また焦点は「"+themes+"」です")
                    member_response[m] = deleteObjectStr(IdeaAPIgIRON.Outputs_custom(member_response[useMember-1]))
                
                #通常のローテーション
                else:
                    IdeaAPIgIRON.SetSystemPrompt("あなたはプロの議論者"+member[m]+"さんです。"+"これから"+member[m-1]+"さんから来た回答に対して反論してください。また反論ができない場合は別の視点から意見を述べてください。また論点は"+themes+"です")
                    member_response[m] = deleteObjectStr(IdeaAPIgIRON.Outputs_custom(member_response[m-1]))
                
                #議事録作成
                giron_all_texts.append(member_response[m])

                print(f"{member[m]}さん:{member_response[m]}")

                print_do_time(return_crithikl_think_time,"議論の一人の時間:")
                IdeaAPIgIRON.PromptSave()

            IdeaAPIgIRON.SetSystemPrompt("あなたは情報を整理しより議論の質を高めるのが得意なプロの議論者,ハンジさんです。"+"これから渡す議事録より次に考えるべきこと教えてください。")
            giron_text = ListChangeText(giron_all_texts)
            giron_all_texts = []

            #議事録まとめ
            giron_text = ListChangeText(giron_all_texts)
            IdeaAPIgIRON.Reset()



    #議論の結論
    print_do_time(giron_start_time,"議論結論が出るまでの時間")
        

    IdeaAPIgIRON.SetSystemPrompt("あなたはプロの議論者"+member[m]+"さんです。"+"これから渡す議事録より結論を教えてください。")
    giron_end = deleteObjectStr(IdeaAPIgIRON.Outputs_custom(giron_text))
    print(f"結論:{giron_end}")

    IdeaAPIgIRON.Reset()