# -*-coding: utf-8 -*-

CHARACTER_SETTING_PROMPT = """
{{#system~}}
你是一个网络小说作家，正在创作一部无限流小说。
{{~/system}}

{{#user~}}
请提供一个主角的角色设定，应该仅包括姓名、年龄、性别、性格、职业、知识储备、价值观/道德观、人际关系、家世背景。
请使用最简洁的表述，使用关键词而不是大段叙述。
有以下要求：
{{character_desc}}
{{~/user}}

{{#assistant~}}
{{gen 'character' temperature=0 max_tokens=500}}
{{~/assistant}}
"""

WORLD_GENERATOR_PROMPT = """
{{#system~}}
你是一个网络小说作家，正在创作一部无限流小说。
{{~/system}}

{{#user~}}
这部小说的世界观如下：
{{background}}
------
接下来，请你生成{{n}}个平行世界，供主角进行探索，请注意生成的世界与背景世界观不要太过违和。还有以下要求：
{{worlds_desc}}
请按照json格式进行输出，例如：
[
    {"name": "火影世界", "description": "这个世界遍布着无数岛屿和宝藏……"},
    {"name": "进击的巨人", "description": "这个世界被巨大的墙壁包围……"}
]
{{~/user}}

{{#assistant~}}
{{gen 'worlds' temperature=0.9 max_tokens=3000}}
{{~/assistant}}
"""

NAME_PROMPT = """
{{#system~}}
你是一个网络小说作家，正在创作一部无限流小说。
{{~/system}}

{{#user~}}
这部小说的世界观如下：
{{background}}
======
接下来，请你给小说起一个名字，要和前面的基本设定相关，但是要隐晦、有深意一点。请直接输出小说名，不要带任何标点符号，也不要进行任何解释说明。
{{~/user}}

{{#assistant~}}
{{gen 'name' temperature=0.9 max_tokens=10}}
{{~/assistant}}
"""

OUTLINE_PROMPT = """
{{#system~}}
你是一个网络小说作家，正在创作一部无限流小说。
{{~/system}}

{{#user~}}
小说名：{{name}}
世界观：
{{background}}
------
主角信息：
{{character}}
------
小说将涉及的世界设定：
{{worlds}}
======
请你基于上述信息，给整部小说创作一个大纲。要新奇、引人入胜，1000字左右。
按照json格式进行输出，例如：
[
    {"name": "第一卷：初试火灵", "desc": "主角第一次看到火灵……"},
    {"name": "第二卷：元素之力", "desc": "主角向着元山出发……"}
]
{{~/user}}

{{#assistant~}}
{{gen 'outline' temperature=0.9 max_tokens=3000}}
{{~/assistant}}
"""

VOLUME_OUTLINE_PROMPT = """
{{#system~}}
你是一个网络小说作家，正在创作一部无限流小说。
{{~/system}}

{{#user~}}
小说名：{{name}}
世界观：
{{background}}
------
主角信息：
{{character}}
------
小说总纲：
{{outline}}
======
这是上一卷的总结：
{{last_volume_summary}}
接下来请给{{n}}写一个1000字左右的大纲。
注意：每卷的内容将多达数万乃至十万字，请保证你的大纲能够撑起这么多的内容量。
请注意每一卷的背景故事设定，可以在此基础上多进行一些有特色的深入创作。
按照json格式进行输出，例如：
[
    {"name": "第一章：初试火灵", "desc": "主角第一次看到火灵……"},
    {"name": "第二章：元素之力", "desc": "主角向着元山出发……"}
]
{{~/user}}

{{#assistant~}}
{{gen 'volume_outline' temperature=0.9 max_tokens=3000}}
{{~/assistant}}
"""

CHAPTER_OUTLINE_PROMPT = """
{{#system~}}
你是一个网络小说作家，正在创作一部无限流小说。
{{~/system}}

{{#user~}}
小说名：
{{name}}
世界观：
{{background}}
------
主角信息：
{{character}}
------
小说各卷内容简介：
{{volumes}}
======
接下来，需要为{{volume_num}}、{{chapter_num}}写一个大纲。
这是上一章的提要：
{{last_chapter_summary}}
这是你此前为本章所写的简介：
{{chapter_intro}}
这是主角进入本章时的状态：
{{character_state}}
需要包括以下部分：
1. 创作构思：请写出你创作本章时的主要创意点，你将以何种手法、剧情来吸引读者。
2. 主要事件：请列出本章中的主要事件，包括：
    2.1 主角获取道具、装备、境界提升、结识伙伴等涉及主角状态更新的事件
    2.2 对情节发展起重要作用的事件。（此类事件不要超过3个）
3. 本章结束时主角状态，应该包括当前的境界(realm)、持有的装备(equipment)、技能(skill)、物品(item)、系统积分(system_score)、同行伙伴(partner)
注意，本章的剧情需要与本卷以及上一章的剧情衔接恰当。
注意，所有主角状态变化都必须在主要事件中列出。
按照json格式输出，例如：
{
    "idea": "主角发现众佛居然是由人类假扮的，通过巨大冲击吸引读者……",
    "main_event": ["主角在长河边发现金刚甲装备", "主角通过击杀通天神，领悟斗圣8层境界", "xx之父被xxx所杀"],
    "character_state": {
        "equipment": ["金刚甲", "血饮刀"],
        "skill": ["初级治愈术", "长天一刺"],
        "system_score": 2313,
        "item": ["金疮药", "回天膏*2"],
        "realm": "通幽境",
        "partner": ["小狗", "子墨", "召唤物小云"]
    }
}
{{~/user}}

{{#assistant~}}
{{gen 'outline' temperature=0 max_tokens=3000}}
{{~/assistant}}
"""

SUMMARY_PROMPT = """
{{#system~}}
你是一个网络小说作家，正在创作一部无限流小说。
{{~/system}}

{{#user~}}
小说名：
{{name}}
世界观：
{{background}}
------
主角信息：
{{character}}
------
小说各卷内容简介：
{{volumes}}
======
你正在创作{{volume_num}}、{{chapter_num}}。
这是本章的前情提要：
{{chapter_summary}}
这是主角之前的状态：
{{old_character_state}}
这是新的故事进展：
{{new_paragraph}}
这是主角当前的状态：
{{new_character_state}}
======
请你综合上述3部分内容，写一个新的章节总结，有以下要求：
1. 在前情提要的基础上进行续写。
2. 如果主角状态发生了变化，新的总结应该包含状态变化相关的剧情
3. 总结使用最简练的语言
4. 输出应该是一段话，不要有任何解释
{{~/user}}

{{#assistant~}}
{{gen 'summary' temperature=0 max_tokens=3000}}
{{~/assistant}}
"""

WRITER_PROMPT = """
{{#system~}}
你是一个网络小说作家，正在创作一部无限流小说。
{{~/system}}

{{#user~}}
小说名：
{{name}}
世界观：
{{background}}
------
主角信息：
{{character}}
------
小说各卷内容简介：
{{volumes}}
======
你正在创作{{volume_num}}、{{chapter_num}}。
这是你之前为本章列出的提纲：
{{chapter_outline}}
注意：这里的character_state是本章完成时的主角状态，不是当前主角状态。
这是本章的前情提要：
{{chapter_summary}}
这是上一章的提要：
{{last_chapter_summary}}
这是主角当前的状态：
{{character_state}}
======
请你在上述信息基础上继续进行创作，有以下要求：
1. 你本次只需要创作一段内容，不需要完成整个章节。
2. 输出应该包括以下几个部分：
    2.1 创作构思：简单写下你的创作思路，本段内容的闪光点和吸引读者的地方
    2.2 正文：你写作的小说正文，正文不能少于500字。
    2.3 更新后的主角状态：应该包括当前的境界(realm)、持有的装备(equipment)、技能(skill)、物品(item)、系统积分(system_score)、同行伙伴(partner)
    2.4 本章是否完结：按照本章提纲的要求，本章是否已经完成了创作。注意：当章节创作完成时，当前主角状态与纲要中规划的主角状态应该是一致的。 
注意，请尽量多引入一些变化和转折，记住你是在写小说，吸引读者、恰当的情节进展速度、创造冲突是写一部好小说的必要条件。
按照json格式输出，例如：
{
    "idea": "主角发现众佛居然是由人类假扮的，通过巨大冲击吸引读者……",
    "content": "……",
    "character_state": {
        "equipment": ["金刚甲", "血饮刀"],
        "skill": ["初级治愈术", "长天一刺"],
        "system_score": 2313,
        "item": ["金疮药", "回天膏*2"],
        "realm": "通幽境",
        "partner": ["小狗", "子墨", "召唤物小云"]
    },
    "finish": false
}
请确保你的输出可以被json.loads()处理，在content内如果需要换行请使用"\\n"。
{{~/user}}

{{#assistant~}}
{{gen 'paragraph' temperature=1 max_tokens=3000}}
{{~/assistant}}
"""