# -*-coding: utf-8 -*-
from llm import call_openai
import json
from prompt import (
    SYSTEM_MESSAGE,
    ROLE_SETTING_PROMPT,
    BACKGROUND_PROMPT,
    POWER_PROMPT,
    WORLD_GENERATOR_PROMPT,
    CHAPTER_OUTLINE_PROMPT,
    NAME_PROMPT,
    VOLUME_SPLIT_PROMPT,
    CHAPTER_SPLIT_PROMPT,
)
from example import (
    EXAMPLE_ROLE,
    EXAMPLE_BACKGROUND,
    EXAMPLE_POWER,
    EXAMPLE_NAME,
    EXAMPLE_WORLD,
    EXAMPLE_VOLUMES,
    EXAMPLE_CHAPTERS,
)
from writer import Writer
from colorama import init, Fore, Style
init()
import guidance
import openai
openai.proxy = "http://127.0.0.1:7890"
openai.api_key = "sk-REDACTED"

guidance.llm = guidance.llms.OpenAI("gpt-4")

def get_role(role_description):
    print("======ROLE======")
    return call_openai([
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": ROLE_SETTING_PROMPT.format(role_description=role_description)}
    ])


def get_background(role):
    print("======BACKGROUND======")
    return call_openai([
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": BACKGROUND_PROMPT.format(role=role, background_description="中国佛教元素")}
    ])


def get_power(background):
    print("======POWER======")
    return call_openai([
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": POWER_PROMPT.format(background=background, power_descripiton="")}
    ])


def get_world(background, role, power):
    print("======WORLD======")
    return call_openai([
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": WORLD_GENERATOR_PROMPT.format(
            background=background,
            role=role,
            power=power,
            n=5,
            world_description="请在著名小说和漫画中挑选世界"
        )}
    ])


def get_name(background, role, power):
    print("======NAME======")
    return call_openai([
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": NAME_PROMPT.format(
            background=background,
            role=role,
            power=power,
        )}
    ])


def get_volumes(background, role, power, name, world):
    print("======VOLUNES======")
    return call_openai([
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": VOLUME_SPLIT_PROMPT.format(
            name=name,
            background=background,
            role=role,
            power=power,
            world=world
        )}
    ])


def get_chapters(background, role, power, name, world, volumes):
    print("======CHAPTERS======")
    for i in range(len(json.loads(volumes))):
        call_openai([
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": CHAPTER_SPLIT_PROMPT.format(
                name=name,
                background=background,
                role=role,
                power=power,
                world=world,
                volumes=volumes,
                volume_n=i+1,
                n=5
            )}
        ])


def get_chapter_outline(background, role, power, name, volumes, volume_num, chapter_num, last_chapter_summary, chapter_description, role_state):
    print("======CHAPTER_OUTLINE======")
    call_openai([
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": CHAPTER_OUTLINE_PROMPT.format(
            name=name,
            background=background,
            role=role,
            power=power,
            volumes=volumes,
            volume_num=volume_num,
            chapter_num=chapter_num,
            last_chapter_summary="这是第一章，没有上一章。" if volume_num == 1 and chapter_num == 1 else last_chapter_summary,
            chapter_description=chapter_description,
            role_state="小说刚刚开始，空白状态。" if volume_num == 1 and chapter_num == 1 else role_state
        )}
    ])


def main():
    # role = get_role(role_description="")
    # background = get_background(role=role)
    # power = get_power(background=background)
    # get_world(EXAMPLE_BACKGROUND, EXAMPLE_ROLE, EXAMPLE_POWER)
    # get_name(EXAMPLE_BACKGROUND, EXAMPLE_ROLE, EXAMPLE_POWER)
    # get_volumes(EXAMPLE_BACKGROUND, EXAMPLE_ROLE, EXAMPLE_POWER, EXAMPLE_NAME, EXAMPLE_WORLD)
    # get_chapters(EXAMPLE_BACKGROUND, EXAMPLE_ROLE, EXAMPLE_POWER, EXAMPLE_NAME, EXAMPLE_WORLD, EXAMPLE_VOLUMES)
    # get_chapter_outline(
    #     EXAMPLE_BACKGROUND,
    #     EXAMPLE_ROLE,
    #     EXAMPLE_POWER,
    #     EXAMPLE_NAME,
    #     EXAMPLE_VOLUMES,
    #     1,
    #     1,
    #     None,
    #     json.loads(EXAMPLE_CHAPTERS)[0][0],
    #     None
    # )
    writer = Writer(
        character=EXAMPLE_ROLE,
        world=EXAMPLE_WORLD,
        background=EXAMPLE_BACKGROUND,
        power=EXAMPLE_POWER,
        name=EXAMPLE_NAME,
        volumes=EXAMPLE_VOLUMES,
        chapters=EXAMPLE_CHAPTERS,
        work_dir="./work_dir"
    )
    writer.start(False)



if __name__ == "__main__":
    main()
