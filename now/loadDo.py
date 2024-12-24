import sys
import os

# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# gironType のパスを追加
sys.path.append(os.path.join(current_dir, "gironType"))

#計測スタート
import time
all_do_start = time.time()

import gironType.earstProbe as earstProbe
from gironType.Toolfunction.Loadquestion import LoadSimgle
import sys



save_path = "./testPrompts/Log.jsonl"

themes_path = "./q.csv"
themes_list = LoadSimgle(themes_path)
# def PromptSave():
#         global save_data
#         if save_data == []:
#             print("[NotingSaveData]")
#         else:
#             with open(save_path,"a",encoding="utf8")as file:
#                 file.writelines(f"{line}\n" for line in save_data)
#             print("[Success Save]")
#             save_data = []


# #渡す過程で出てくるじゃまなブロックを削除する
# def deleteObjectStr(content:str):
#     deletes = ["<",">","sys","SYS","INST","[","]","/","s>"]
#     res = content
#     for i in deletes:
#         res = str(res).replace(i,"")
#     return res

# #list-text
# def list_change_text(content:list):
#     res = ""
#     for i in content:
#         res += i
#     return res

def print_do_time(start_time,option):
    end_time=time.time()
    print(option+"かかった時間{:.2f}".format(end_time-start_time))



#Auto Test Mode
# sysPrompt = ["あなたはプロの議論者Aさんです。","あなたはプロの議論者Bさんです。"]
themes = "コミュニケーションで必要なこと"


#Propaty
member = ['A','B','C','D','E','F','G','H','I','J','K','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
member_response = []
useMember = 3
turn= 3

print(f"推定処理時間:{((40 * useMember) * turn) /60} 分")

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

for t in themes_list:
    themes = t
    earstProbe.giron(themes=themes)


all_do_end = time.time()
print("全ての演算に使用した時間:{:.2f}".format(all_do_end-all_do_start))