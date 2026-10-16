# agent.py

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.tools import PythonREPLTool

from tools import (
    get_weather,
    convert_currency,
    get_current_time,
    set_reminder,
    get_reminders
)


def create_personal_agent():

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.5
    )

    tools = [
        get_weather,
        convert_currency,
        get_current_time,
        set_reminder,
        get_reminders,
        DuckDuckGoSearchRun(),
        PythonREPLTool()
    ]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""
        You are a Smart Personal Assistant.

        Rules:
        - Use weather tool for weather.
        - Use currency tool for conversion.
        - Use time tool for time.
        - Use reminder tool to store tasks.
        - Use search tool for latest information.
        - Always respond clearly and concisely.
        """
    )

    return agent