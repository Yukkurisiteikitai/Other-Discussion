import os
import torch
from transformers import AutoTokenizer
from peft import AutoPeftModelForCausalLM
import time
import random
import Loadquestion
import json

# Hugging Faceのトークンを設定
from huggingface_hub import login
hf_token = "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"
login(hf_token)
os.environ["HF_TOKEN"] = hf_token

# モデルの設定
adpt_path = "./model/BadMargeModel"
# repo_id = "elyza/Llama-3-ELYZA-JP-8B"
repo_id = "elyza/Llama-3-ELYZA-JP-8B"


# モデルの読み込み
try:
    model = AutoPeftModelForCausalLM.from_pretrained(
        pretrained_model_name_or_path=adpt_path,
        local_files_only=True,
        device_map="auto",  # 自動的にデバイスを割り当て
        torch_dtype=torch.float16,
        load_in_4bit=True  # 4bit量子化
    )
except EOFError:
    print("failure-Model-Load")
try:
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=repo_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
except EOFError:
    print("failure-Load-Tokenizer")
tokenizer.chat_template = "<s>[INST] <<sys>>{system_prompt}<</sys>>{user_message} [/INST] {assistant_message}</s>"

print("[Success]-Tokenizer-Model-Load")

# 質問の設定
QuestionCSVpath = "seePointANDtheme.csv"
seePoints, themes = Loadquestion.LoadQuestion(QuestionCSVpath)
conversation_history = []
# SystemPrompt = "あなたは問題点を指摘するのが得意なアドバイザーです。今回は箇条書きで回答アドバイスしてください。また箇条書きは3つまでとなります。"
SystemPrompt = "あなたは優秀なサポーターです。目的は一つのテーマを様々な観点から見ることでそのテーマを分析すること。そのテーマをその観点からみたらどうなるかを教えてください。"

#SaveDatas
save_data = []
# save_path = "./testPrompts/RecToPrompts.jsonl"
save_path = "./testPrompts/Log.jsonl"

def AddSaveDataInfo(systemPrompt:str,qestion:str,answer:str):
    # return    {
    #     "messages":[
    #         {'"SystemPrompt"'+':"'+systemPrompt+'"'},
    #         {"question"+':"'+qestion+'"'},
    #         {'"answer"'+':"'+answer+'"'}
    #     ]
    # }
    # return    {
    #     "messages":[
    #         {"SystemPrompt"+":"+systemPrompt},
    #         {"question"+":"+qestion},
    #         {"answer"+":"+answer}
    #     ]
    # }
    return    {
        "messages":[
            {'SystemPrompt":"'+''+systemPrompt},
            {'question":"'+qestion},
            {'answer":"'+answer}
        ]
    }

def Reset():
    conversation_history = []
    conversation_history.append({"role": "user", "content": SystemPrompt})

def SetSystemPrompt(input_sys:str):
    global SystemPrompt
    conversation_history = []
    SystemPrompt = input_sys
    conversation_history.append({"role": "user", "content": SystemPrompt})
def ProgramSetSystemPrompt(prompt):
    global SystemPrompt
    conversation_history = []
    SystemPrompt = prompt
    conversation_history.append({"role": "system", "content": SystemPrompt})


Reset()

# def Outputs_custom(input_user :str):
#     global save_data
#     # print(f"SystemPrompt{SystemPrompt}")#test
#     user_input = input_user    
#     prompt = "<s>[INST] <<sys>>{system_prompt}<</sys>>{user_message} [/INST]</s>".format(
#         system_prompt=SystemPrompt,
#         user_input=input_user
#     )
#     # conversation_history.append({"role": "user", "content": user_input})
#     # prompt = tokenizer.apply_chat_template(
#     #     conversation=conversation_history,
#     #     tokenize=False,
#     #     add_generation_prompt=True
#     # )
#     model_inputs = tokenizer(prompt, return_tensors="pt", padding=True).to("cuda")
#     with torch.cuda.amp.autocast():  # 混合精度を使用してメモリを節約
#         generated_ids = model.generate(
#             model_inputs.input_ids,
#             attention_mask=model_inputs.attention_mask,
#             max_new_tokens=300
#         )
#     generated_ids = [
#         output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
#     ]
#     response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
#     conversation_history.append({"role": "assistant", "content": response})
#     torch.cuda.empty_cache()

#     response_temp = ""
#     response_temp = response
#     save = AddSaveDataInfo(SystemPrompt,user_input,response_temp)
#     save_data.append(str(save).replace("'",'"'))

#     return response
def Outputs_custom(input_user: str):
    global save_data, SystemPrompt, conversation_history

    # プロンプトの準備
    prompt = """<s>[INST] <<SYS>>{system}<</SYS>>{user}[/INST] """.format(system=SystemPrompt,user=input_user)
    print(f"プロンプト:{prompt}")

    # 推論の実行
    token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
    with torch.no_grad():
        output_ids = model.generate(
            token_ids.to(model.device),
            do_sample=True,
            temperature=0.5,
            max_new_tokens=256,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    response = tokenizer.decode(output_ids.tolist()[0][token_ids.size(1) :], skip_special_tokens=True)
    

    torch.cuda.empty_cache()

    response_temp = response

    # 保存データの準備
    save = AddSaveDataInfo(SystemPrompt, input_user, response_temp)
    save_data.append(str(save).replace("'", '"'))

    return response


# print(Outputs_custom("jfweioというテーマについて客観的観点からアドバイスしてください"))
save_path = "./testPrompts/giron.jsonl"
def PromptSave():
    global save_data,save_path
    if save_data == []:
        print("[NotingSaveData]")
    else:
        with open(save_path,"a",encoding="utf8")as file:
            file.writelines(f"{line}\n" for line in save_data)
        print("[Success Save]")
        save_data = []
    # save_data = []

# print("回答を終了させていただきました")