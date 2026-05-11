# -*-coding: utf-8 -*-

import json
from guidance_prompt import (
    SUMMARY_PROMPT,
    WRITER_PROMPT,
    CHAPTER_OUTLINE_PROMPT,
    VOLUME_OUTLINE_PROMPT,
    OUTLINE_PROMPT,
)
from example import EXAMPLE_BACKGROUND
import guidance
import os
from colorama import Fore, Style
from utils import print_stream_and_return_program
from architect import Architect


def get_last(category, field, ctx):
    if category == "volume":
        if len(ctx["volumes"]) >= 2:
            return ctx["volumes"][-2][field]
        else:
            return None
    elif category == "chapter":
        if len(ctx["volumes"][-1]["chapters"]) >= 2:
            return ctx["volumes"][-1]["chapters"][-2][field]
        elif len(ctx["volumes"]) >= 2:
            return ctx["volumes"][-2]["chapters"][-1][field]
        else:
            return None
    elif category == "paragraph":
        if len(ctx["volumes"][-1]["chapters"][-1]["paragraphs"]) >= 2:
            return ctx["volumes"][-1]["chapters"][-1]["paragraphs"][-2][field]
        elif len(ctx["volumes"][-1]["chapters"]) >= 2:
            return ctx["volumes"][-1]["chapters"][-2]["paragraphs"][-1][field]
        elif len(ctx["volumes"]) >= 2:
            return ctx["volumes"][-2]["chapters"][-1]["paragraphs"][-1][field]
        else:
            return None

class Writer(object):
    def __init__(self, architect, background, work_dir):
        self.work_dir = work_dir
        os.system(f"mkdir -p {work_dir}")
        os.system(f"rm {work_dir}/main.txt")
        self.character = architect.character
        self.worlds = architect.worlds
        self.background = background
        self.name = architect.name
        self.ctx = None

    def write_file(self, text):
        with open(f"{self.work_dir}/main.txt", "a") as fwp:
            fwp.write(text)

    def write_outline(self):
        outline_program = guidance(
            OUTLINE_PROMPT,
            stream=True,
        )
        executed = outline_program(
            name=self.name,
            background=self.background,
            character=self.character,
            worlds=self.worlds,
        )
        print(f"{Fore.LIGHTGREEN_EX}【小说总纲】：{Style.RESET_ALL}")
        executed = print_stream_and_return_program(executed, lambda s: s.get("outline", ""), Fore.LIGHTGREEN_EX)
        return json.loads(executed["outline"])

    def write_volume_outline(self, ctx, volume_ctx):
        print(f"{Fore.WHITE}【新的一卷开始写作】：{volume_ctx['intro']['name']}{Style.RESET_ALL}")
        outline_program = guidance(
            VOLUME_OUTLINE_PROMPT,
            stream=True,
        )
        last_volume_summary = get_last("volume", "summary", ctx)
        executed = outline_program(
            name=self.name,
            background=self.background,
            character=self.character,
            outline=ctx['outline'],
            last_volume_summary=last_volume_summary if last_volume_summary else "这是第一卷，没有上一卷。",
            n=volume_ctx['intro']['name']
        )
        print(f"{Fore.WHITE}【本卷大纲】：{Style.RESET_ALL}")
        executed = print_stream_and_return_program(executed, lambda s: s.get("volume_outline", ""), Fore.WHITE)
        return json.loads(executed['volume_outline'])

    def write_volume(self, ctx, volume_ctx):
        self.write_file("\n" + volume_ctx["intro"]["name"] + "\n")
        outline = self.write_volume_outline(ctx, volume_ctx)
        volume_ctx["outline"] = outline
        volume_ctx["chapters"] = []
        for chapter in outline:
            chapter_ctx = {"intro": chapter}
            volume_ctx["chapters"].append(chapter_ctx)
            self.write_chapter(ctx, volume_ctx, chapter_ctx)

    def write_chapter_outline(self, ctx, volume_ctx, chapter_ctx):
        self.write_file("\n" + chapter_ctx["intro"]["name"] + "\n")
        print(f"{Fore.YELLOW}"
              f"【新章节开始写作】：{chapter_ctx['intro']['name']}\n"
              f"【章节简介】：{chapter_ctx['intro']['desc']}"
              f"{Style.RESET_ALL}"
        )
        outline_program = guidance(
            CHAPTER_OUTLINE_PROMPT,
            stream=True,
        )
        last_chapter_summary = get_last("chapter", "summary", ctx)
        last_character_outline = get_last("chapter", "outline", ctx)
        executed = outline_program(
            name=self.name,
            background=self.background,
            character=self.character,
            volumes=ctx['outline'],
            volume_num=volume_ctx["intro"]["name"],
            chapter_num=chapter_ctx["intro"]["name"],
            last_chapter_summary=last_chapter_summary if last_chapter_summary else "这是第一章，没有上一章。",
            chapter_intro=chapter_ctx['intro']['desc'],
            character_state=last_character_outline["character_state"] if last_character_outline else {}
        )
        print(f"{Fore.YELLOW}【本章大纲】：{Style.RESET_ALL}")
        executed = print_stream_and_return_program(executed, lambda s: s.get("outline", ""), Fore.YELLOW)
        return json.loads(executed["outline"])

    def write_chapter(self, ctx, volume_ctx, chapter_ctx):
        outline = self.write_chapter_outline(ctx, volume_ctx, chapter_ctx)
        chapter_ctx["outline"] = outline
        chapter_ctx["paragraphs"] = []
        finish_flag = False
        while not finish_flag:
            paragraph_ctx = {}
            chapter_ctx["paragraphs"].append(paragraph_ctx)
            paragraph = json.loads(self.write_paragraph(ctx, volume_ctx, chapter_ctx).replace("['", '["').replace(",'", ',"').replace("']", '"]').replace('";\n', '",\n').replace("\n\n'],", '",'))
            finish_flag = paragraph["finish"]
            summary = self.write_paragraph_summary(ctx, volume_ctx, chapter_ctx, paragraph)
            paragraph_ctx["summary"] = summary
            paragraph_ctx.update(**paragraph)
            self.write_file(paragraph["content"])
        chapter_ctx["summary"] = summary
        print(f"{Fore.YELLOW}"
              f"【章节完结】：{chapter_ctx['intro']['name']}\n"
              f"【本章总结】：{summary}"
              f"{Style.RESET_ALL}"
        )

    def write_paragraph(self, ctx, volume_ctx, chapter_ctx):
        print(f"{Fore.GREEN}"
              f"【新段落开始写作】：{volume_ctx['intro']['name']}，{chapter_ctx['intro']['name']}，第{len(chapter_ctx['paragraphs'])}段\n"
              f"{Style.RESET_ALL}"
              )

        paragraph_program = guidance(
            WRITER_PROMPT,
            stream=True
        )
        last_chapter_summary = get_last("chapter", "summary", ctx)
        last_paragraph_character_state = get_last("paragraph", "character_state", ctx)
        executed = paragraph_program(
            name=self.name,
            background=self.background,
            character=self.character,
            volumes=ctx["outline"],
            volume_num=volume_ctx["intro"]["name"],
            chapter_num=chapter_ctx["intro"]["name"],
            chapter_outline=chapter_ctx["outline"],
            chapter_summary=chapter_ctx["paragraphs"][-2]["summary"] if len(chapter_ctx["paragraphs"]) >= 2 else "这是第一段，没有前情提要。",
            last_chapter_summary=last_chapter_summary if last_chapter_summary else "这是第一章，没有上一章。",
            character_state=last_paragraph_character_state if last_paragraph_character_state else {},
        )
        executed = print_stream_and_return_program(executed, lambda s: s.get("paragraph", ""), Fore.GREEN)
        return executed["paragraph"]

    def write_paragraph_summary(self, ctx, volume_ctx, chapter_ctx, paragraph):
        new_character_state = paragraph["character_state"]
        summary_program = guidance(
            SUMMARY_PROMPT,
            stream=True
        )
        last_paragraph_character_state = get_last("paragraph", "character_state", ctx)
        executed = summary_program(
            name=self.name,
            background=self.background,
            character=self.character,
            volumes=ctx["outline"],
            volume_num=volume_ctx["intro"]["name"],
            chapter_num=chapter_ctx["intro"]["name"],
            chapter_summary=chapter_ctx["paragraphs"][-2]["summary"] if len(chapter_ctx["paragraphs"]) >= 2 else "这是第一段，没有前情提要。",
            old_character_state=last_paragraph_character_state if last_paragraph_character_state else {},
            new_paragraph=paragraph["content"],
            new_character_state=new_character_state,
            stream=True,
        )
        executed = print_stream_and_return_program(executed, lambda s: s.get("summary", ""), Fore.RED)
        return executed["summary"]

    def write(self):
        outline = self.write_outline()
        ctx = {"outline": outline, "volumes": []}
        for volume in outline:
            volume_ctx = {"intro": volume}
            ctx["volumes"].append(volume_ctx)
            self.write_volume(ctx, volume_ctx)


if __name__ == "__main__":
    architect = Architect("", "从著名漫画、影视作品中选择", EXAMPLE_BACKGROUND, 5)
    writer = Writer(architect=architect, background=EXAMPLE_BACKGROUND, work_dir="./work_dir")
    writer.write()