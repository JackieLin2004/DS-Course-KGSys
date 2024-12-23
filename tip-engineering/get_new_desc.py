# -*- coding: utf-8 -*-

import csv
import json
from ChatGPT import ChatGPT
from tqdm import tqdm

def get_desc(concept):
    chatgpt = ChatGPT()
    prompt = f"""
        假设你现在是一个数据结构与算法课程的老师，我现在需要你帮我介绍一些关于数据结构和算法的概念。
        我会给你一个提示词，这个提示词是一个名词，表示数据结构与算法里面的一个专业名词。
        我需要你根据这个名词给出定义和解释。我大概是需要两个东西，一个是大致、浓缩的解释，另外一个是详细的解释。
        对于大致的、浓缩的解释，你只需要按照你的理解，给我一句简短的解释即可，我不做过多要求。
        但是对于详细的解释，你做出的回答我最后需要写进markdown文档，所以需要你给我以markdown的格式返回，并且要尽可能详细，有需要的地方可以用数学符号等来表达。如果用数学符号表达，我希望你给出的是详细的latex公式符号，因为这可能比传统的markdown符号会更好。比如log n应该表示为$log n$。
        另外对于详细的解释，你可以尽量多使用数学公式和文字同时表述，数学公式的话按照上面说的给我在markdown的latex公式。而如果你要给出示例代码的话，可以包括伪代码和真是代码，如果给出真实代码，请使用C++语言。
        比如如果给你的提示词是链表，那么你应该按照如下格式给回答：
        链表的大致解释是：链表是一种用于存储数据的数据结构，通过如链条一般的指针来连接元素。它的特点是插入与删除数据十分方便，但寻找与读取数据的表现欠佳。
        链表的详细解释是：链表是一种物理存储单元上非连续、非顺序的存储结构，数据元素的逻辑顺序是通过链表中的指针链接次序实现的。链表由一系列结点（链表中每一个元素称为结点）组成，结点可以在运行时动态生成。每个结点包括两个部分：一个是存储数据元素的数据域，另一个是存储下一个结点地址的指针域。 相比于线性表顺序结构，操作复杂。由于不必须按顺序存储，链表在插入的时候可以达到O(1)的复杂度，比另一种线性表顺序表快得多，但是查找一个节点或者访问特定编号的节点则需要O(n)的时间，而线性表和顺序表相应的时间复杂度分别是O(logn)和O(1)。
        以上就是回答的一个实例。那么现在我给你的提示词是“{concept}”，请按照如上要求给我回答，并且请用中文回答。
    """
    try:
        response = chatgpt.chat(prompt)
        return response["content"]
    except Exception as e:
        return f"获取描述失败：{e}"

concepts_list = []
with open('./all_concepts.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if row:
            concepts_list.append(row[0])

print(f"概念列表读取完成，共 {len(concepts_list)} 个概念。")

output_file = 'all_desc.json'

try:
    with open(output_file, 'r', encoding='utf-8') as f:
        all_desc = json.load(f)
    print(f"已加载 {len(all_desc)} 条已保存的记录。")
except (FileNotFoundError, json.JSONDecodeError):
    all_desc = []

processed_ids = {entry["id"] for entry in all_desc}

with open(output_file, 'w', encoding='utf-8') as f:
    for idx, concept in enumerate(tqdm(concepts_list, desc="Processing Concepts...", unit="concept")):
        if idx in processed_ids:
            continue

        response = get_desc(concept)
        if "大致解释是" in response and "详细解释是" in response:
            try:
                brief_desc = response.split("大致解释是：")[1].split('\n')[0].strip()
                detailed_desc = response.split("详细解释是：")[1].strip()
            except IndexError:
                brief_desc = "解析失败"
                detailed_desc = response
        else:
            brief_desc = "生成失败或格式错误"
            detailed_desc = response

        entry = {
            "id": idx,
            "name": concept,
            "brief_description": brief_desc,
            "detailed_description": detailed_desc
        }
        all_desc.append(entry)

        f.seek(0)
        json.dump(all_desc, f, ensure_ascii=False, indent=4)
        f.truncate()

print(f"所有概念处理完成，结果已保存到 {output_file}")
