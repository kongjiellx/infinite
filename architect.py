# -*-coding: utf-8 -*-

from guidance_prompt import (
    CHARACTER_SETTING_PROMPT,
    WORLD_GENERATOR_PROMPT,
    NAME_PROMPT,
)
from example import (
    EXAMPLE_BACKGROUND,
)
import json
from utils import print_stream_and_return_program
import guidance
import openai
openai.proxy = "http://127.0.0.1:7890"
openai.api_key = "sk-REDACTED"
from colorama import Fore, Style
guidance.llm = guidance.llms.OpenAI("gpt-4")


class Architect(object):
    def __init__(self, character_desc, worlds_desc, background, world_num):
        self.character = self.gen_character(character_desc)
        self.worlds = json.loads(self.gen_worlds(worlds_desc=worlds_desc, background=background, n=world_num))
        self.name = self.gen_name(background)

    @staticmethod
    def gen_character(character_desc):
        program = guidance(
            CHARACTER_SETTING_PROMPT,
            stream=True
        )
        stream = program(character_desc=character_desc)
        state = print_stream_and_return_program(stream, lambda s: s.get("character", ""), Fore.CYAN)
        return state["character"]

    @staticmethod
    def gen_name(background):
        program = guidance(
            NAME_PROMPT,
            stream=True,
        )
        stream = program(background=background)
        state = print_stream_and_return_program(stream, lambda s: s.get("name", ""), Fore.CYAN)
        return state["name"]

    @staticmethod
    def gen_worlds(worlds_desc, background, n):
        program = guidance(
            WORLD_GENERATOR_PROMPT,
            stream=True
        )
        stream = program(background=background, worlds_desc=worlds_desc, n=n)
        state = print_stream_and_return_program(stream, lambda s: s.get("worlds", ""), Fore.CYAN)
        return state["worlds"]


if __name__ == "__main__":
    a = Architect("", "从著名漫画、影视作品中选择", EXAMPLE_BACKGROUND, 5)
