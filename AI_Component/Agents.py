from crewai import Agent
from AI_Component.Llms import *

class Agents :
    def __init__(self):
        # Define llm here llm list can be seen on Llms.py
        self.llm = openai
        self.verbose = True

    def data_search(self):
        return Agent(
            role="Data Researcher and Retriever in SciMentor SEAMEO QIS",
            goal="Research and retrieve data about the given topics related to Science Education and STEM Teaching",
            backstory="You are an expert in searching information related to science education, STEM methodologies, and scientific concepts for more than 15 years. "
                      "You previously worked as a researcher in science education and curriculum development, making it easy for you to find reliable scientific and pedagogical information.",
            allow_delegation=False,
            verbose=self.verbose,
            llm=self.llm
        )
    
    def general_answer(self):
        return Agent(
            role="Science Education Instructor",
            goal="Provide answers and educational materials for science education and STEM teaching questions",
            backstory="You are an experienced science educator and writer who specializes in making complex scientific concepts easy to understand for students and teachers. "
                      "You have a gift for explaining science topics in simple, engaging ways that make learning science enjoyable and accessible for everyone.",
            allow_delegation=False,
            llm=self.llm,
            verbose=self.verbose
        )
