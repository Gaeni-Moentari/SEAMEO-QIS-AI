from AI_Component.validator.validator import QisValidator, qis_validator

# Initialize the validator
validator = QisValidator()

# Note: Make sure you have the required packages installed:
# pip install langchain-core langchain-openai python-dotenv

# Test cases
test_cases = [
    # Clearly QIS-related questions
    "What are the best practices for teaching science in high school?",
    "How can I improve STEM education in my classroom?",
    "What is SEAMEO QIS?",
    "Tell me about quality improvement in science education",
    
    # Questions that should be caught by fallback
    "Apa program SEAQIS?",
    "Dimana lokasi SEAMEO QIS?",
    "What is the focus of QIS?",
    
    # Non-QIS questions
    "What is the weather like today?",
    "How do I cook pasta?",
    "Tell me about the latest smartphone"
]

# Test the class-based validator
print("Testing QisValidator class:")
for i, question in enumerate(test_cases):
    result = validator.validate(question)
    print(f"{i+1}. '{question}' -> {'QIS-related' if result else 'Not QIS-related'}")
    if result:
        print(f"   Fallback active: {validator.fallback_active}")
    print()

# Reset the validator state
validator = QisValidator()

# Test the legacy function
print("\nTesting legacy qis_validator function:")
for i, question in enumerate(test_cases):
    result = qis_validator(question)
    print(f"{i+1}. '{question}' -> {'QIS-related' if result else 'Not QIS-related'}")
    print()