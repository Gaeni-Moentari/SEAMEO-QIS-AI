from crewai import Crew, Process
from AI_Component.Agents import *
from AI_Component.Tasks import *
from AI_Component.Llms import *

class QisCrew:
    def __init__(self, input, lang):
        self.input = input
        self.lang = lang
        self.tasks = Tasks(self.input,self.lang)
        self.agents = Agents()

    def generalCrew(self):
        task = self.tasks
        agent = self.agents
        return Crew(
            tasks=[task.general_search_task(),task.general_answer_task()],
            agents=[agent.data_search(),agent.general_answer()],
            process=Process.sequential,
            manager_llm=openai
    )
