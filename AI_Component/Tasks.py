from crewai import Task
from AI_Component.Agents import *
from AI_Component.Tools import *


agents = Agents()

class Tasks:
    def __init__(self, input, lang):
        self.input=input
        self.lang=lang
    
    def general_search_task(self):
        return Task(
            description=f"Your task is to search for data and information about science education and STEM teaching based on the input: {self.input}, along with reference links. "
                         "You will provide your search results to the answer writer. "
                         "You will use the [WebSearch] tool.",
            expected_output="A comprehensive search result from various sources with their source links. "
                            "Use an easy-to-understand format for composing a comprehensive answer.",
            agent=agents.data_search(),
            tools=[WebSearch]
        )
    
    def general_answer_task(self):
        return Task(
            description="Your task is to: "
                        f"Answer the following science education and STEM teaching question: {self.input}. "
                        "Use the data that was searched previously. "
                        "Include reference links that support your answer from the provided information.",
            expected_output="Answer created in markdown format like a brief Wikipedia article. "
                            "Answer includes references that can be visited at the end. "
                            f"Answer MUST use the following language: {self.lang}",
            agent=agents.general_answer()
        )
