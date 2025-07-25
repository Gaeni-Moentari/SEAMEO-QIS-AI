from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from crewai import Agent, Task, Crew, Process
from AI_Component.Agents import Agents
from AI_Component.Tasks import Tasks
from AI_Component.Llms import openai
from AI_Component.Tools import WebSearch
from dotenv import load_dotenv
import os
import re

load_dotenv()
# OpenAI API Key Configuration
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Global flag for SEAQIS context
is_seaqis_context = False

# 1. Entity-based Validation Agent
class ValidationAgent:
    def __init__(self):
        # Prompt Template for SEAQIS validation
        self.validator_prompt = PromptTemplate(
            input_variables=["question"],
            template=(
                "Is the following question related to SEAMEO QIS topics (quality improvement in science education, "
                "science teaching methodologies, assessment, evaluation, curriculum development, or any other "
                "SEAMEO QIS related topics)? Answer only with 'yes' or 'no'.\n\n"
                "Question: {question}\n"
            ),
        )
        
        # LLM integration for validation
        self.llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)
        self.validator_chain = LLMChain(llm=self.llm, prompt=self.validator_prompt)
    
    def validate(self, question):
        """Validate if the question is related to SEAMEO QIS topics"""
        global is_seaqis_context
        
        response = self.validator_chain.run(question=question).strip().lower()
        is_seaqis_context = (response == "yes")
        
        return is_seaqis_context

# 2. Rule-based Fallback
def rule_based_fallback(question):
    """Apply rule-based fallback if Validation Agent cannot recognize context"""
    global is_seaqis_context
    
    # If context is already set to True by the validation agent, no need for fallback
    if is_seaqis_context:
        return is_seaqis_context
    
    # Keywords that might indicate SEAQIS-related questions
    fallback_keywords = [
        "apa programnya", "program apa", "kegiatannya apa", "kegiatan apa", 
        "dimana lokasinya", "lokasi", "fokusnya apa", "fokus", 
        "apa itu SEAQIS", "apa itu QIS", "SEAMEO QIS", "QIS", "SEAQIS"
    ]
    
    # Check if any of the fallback keywords are in the question
    question_lower = question.lower()
    for keyword in fallback_keywords:
        if keyword.lower() in question_lower:
            is_seaqis_context = True
            return True
    
    return False

# 3. Injection Context to Main Prompt
def inject_context(question):
    """Inject context to the main prompt if SEAQIS context is detected"""
    global is_seaqis_context
    
    if is_seaqis_context:
        return "User is asking about SEAMEO QIS. Provide a concise and friendly explanation based on SEAQIS data. " + question
    
    return question

# 4. Refactored Agent Chain
class SeaqisAgents(Agents):
    def __init__(self):
        super().__init__()
    
    def validation_agent(self):
        """Create a validation agent for SEAQIS context detection"""
        return Agent(
            role="Validation Agent - SEAQIS",
            goal="Validate if user questions are related to SEAMEO QIS topics",
            backstory="You are an expert in identifying questions related to SEAMEO QIS topics. "
                      "You have extensive knowledge about quality improvement in science education, "
                      "science teaching methodologies, assessment, evaluation, and curriculum development.",
            allow_delegation=False,
            verbose=self.verbose,
            llm=self.llm
        )
    
    def research_agent_seaqis(self):
        """Create a research agent specialized in SEAQIS topics"""
        return Agent(
            role="Research Agent - SEAQIS",
            goal="Research and provide comprehensive information about SEAMEO QIS topics",
            backstory="You are a specialized researcher in SEAMEO QIS topics with extensive knowledge about "
                      "quality improvement in science education, science teaching methodologies, assessment, "
                      "evaluation, and curriculum development. You provide accurate and detailed information "
                      "about SEAMEO QIS programs, activities, and initiatives.",
            allow_delegation=False,
            verbose=self.verbose,
            llm=self.llm
        )

class SeaqisTasks(Tasks):
    def __init__(self, input, lang):
        super().__init__(input, lang)
        self.seaqis_agents = SeaqisAgents()
    
    def validation_task(self):
        """Create a task for validating if questions are related to SEAMEO QIS"""
        return Task(
            description=f"Your task is to validate if the following question is related to SEAMEO QIS topics: {self.input}. "
                        "Determine if it's about quality improvement in science education, science teaching methodologies, "
                        "assessment, evaluation, curriculum development, or any other SEAMEO QIS related topics.",
            expected_output="A simple 'yes' or 'no' answer indicating if the question is related to SEAMEO QIS topics.",
            agent=self.seaqis_agents.validation_agent()
        )
    
    def research_task_seaqis(self):
        """Create a research task specialized in SEAQIS topics"""
        return Task(
            description=f"Your task is to research and provide comprehensive information about the following SEAMEO QIS topic: {self.input}. "
                        "Focus on quality improvement in science education, science teaching methodologies, assessment, "
                        "evaluation, curriculum development, or any other relevant SEAMEO QIS information.",
            expected_output="Comprehensive research results about the SEAMEO QIS topic with relevant details and sources.",
            agent=self.seaqis_agents.research_agent_seaqis(),
            tools=[WebSearch]
        )

class QisAgentChain:
    def __init__(self, input, lang):
        self.input = input
        self.lang = lang
        self.validation_agent = ValidationAgent()
        self.tasks = SeaqisTasks(input, lang)
        self.agents = SeaqisAgents()
    
    def process_question(self):
        """Process the question through the SEAMEO QIS agent chain"""
        # Step 1: Validate if the question is related to SEAMEO QIS
        is_valid = self.validation_agent.validate(self.input)
        
        # Step 2: Apply rule-based fallback if needed
        if not is_valid:
            is_valid = rule_based_fallback(self.input)
        
        # Step 3: If valid, inject context and process through the agent chain
        if is_valid:
            # Inject context to the main prompt
            enhanced_input = inject_context(self.input)
            
            # Create a new Tasks instance with the enhanced input
            enhanced_tasks = SeaqisTasks(enhanced_input, self.lang)
            
            # Create and run the crew
            crew = Crew(
                tasks=[enhanced_tasks.research_task_seaqis(), enhanced_tasks.general_answer_task()],
                agents=[self.agents.research_agent_seaqis(), self.agents.general_answer()],
                process=Process.sequential,
                manager_llm=openai
            )
            
            return crew.kickoff()
        
        # If not valid, return None to indicate that the question is not related to SEAMEO QIS
        return None

# Function to check if a question is related to SEAMEO QIS
def is_seaqis_question(question):
    """Check if a question is related to SEAMEO QIS using the validation agent and fallback rules"""
    validation_agent = ValidationAgent()
    
    # Step 1: Validate using the validation agent
    is_valid = validation_agent.validate(question)
    
    # Step 2: Apply rule-based fallback if needed
    if not is_valid:
        is_valid = rule_based_fallback(question)
    
    return is_valid