from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()
# OpenAI API Key Configuration
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Enhanced SEAMEO QIS Validator with Entity-based Detection
class QisValidator:
    def __init__(self):
        self.llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)
        self.is_qis_context = False
        self.fallback_active = False
        
        # Enhanced prompt for better context detection
        self.validator_prompt = PromptTemplate(
            input_variables=["question"],
            template=(
                "You are a validation agent for SEAMEO QIS topics. "
                "Determine if the following question is related to SEAMEO QIS's scope: "
                "quality improvement in science education, science teaching methodologies, "
                "assessment, evaluation, curriculum development, STEM education, "
                "or SEAMEO QIS organization itself.\n\n"
                "Be generous in interpretation - if it's remotely related to science education, "
                "STEM teaching, or educational improvement, consider it valid.\n\n"
                "Question: {question}\n\n"
                "Answer only with 'QIS_CONTEXT' if related, 'NOT_QIS' if not related."
            ),
        )
        
        # Create a chain using the newer LangChain approach
        self.validator_chain = self.validator_prompt | self.llm | StrOutputParser()
    
    def rule_based_fallback(self, question):
        """Rule-based fallback for common question patterns"""
        # More specific fallback patterns to avoid false positives
        fallback_patterns = [
            # Organization-specific patterns
            r'qis\b',
            r'seaqis\b',
            r'seameo\b',
            
            # Question patterns about the organization
            r'kegiatan\s+apa\s+aja',
            r'program(nya)?\s+apa',
            r'lokasi(nya)?\s+di\s+mana',
            r'tujuan(nya)?\s+apa',
            r'fokus(nya)?\s+ke\s+mana',
            r'apa\s+itu\s+(seameo|qis|seaqis)',
            r'what\s+is\s+(seameo|qis|seaqis)',
            r'what\s+are\s+the\s+activities\s+of\s+(seameo|qis|seaqis)',
            r'what\s+programs\s+(does|of)\s+(seameo|qis|seaqis)',
            r'where\s+is\s+(seameo|qis|seaqis)\s+located',
            r'what\s+is\s+the\s+purpose\s+of\s+(seameo|qis|seaqis)',
            r'what\s+is\s+the\s+focus\s+of\s+(seameo|qis|seaqis)',
            
            # Education-specific patterns with context
            r'science\s+(education|teaching|learning|curriculum)',
            r'stem\s+(education|teaching|learning|curriculum)',
            r'(teaching|learning)\s+science',
            r'(teaching|learning)\s+stem',
            r'curriculum\s+development\s+for\s+science',
            r'assessment\s+(in|for)\s+science',
            r'evaluation\s+(in|for)\s+science',
            r'quality\s+improvement\s+in\s+science'
        ]
        
        question_lower = question.lower()
        
        for pattern in fallback_patterns:
            if re.search(pattern, question_lower):
                self.fallback_active = True
                return True
                
        return False
    
    def validate(self, question):
        """Main validation function with entity detection and fallback"""
        try:
            # Primary validation through LLM using the newer invoke approach
            response = self.validator_chain.invoke({"question": question}).strip().upper()
            
            if "QIS_CONTEXT" in response:
                self.is_qis_context = True
                return True
            
            # Fallback to rule-based detection
            if self.rule_based_fallback(question):
                self.is_qis_context = True
                return True
                
            return False
            
        except Exception as e:
            # Emergency fallback - if anything fails, use rule-based only
            print(f"Validation error: {e}")
            return self.rule_based_fallback(question)

# Initialize global validator instance
qis_validator_instance = QisValidator()

# Legacy function for backward compatibility
def qis_validator(question):
    """Legacy validator function - now uses enhanced QisValidator"""
    return qis_validator_instance.validate(question)
