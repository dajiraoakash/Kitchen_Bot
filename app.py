from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
import re
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

#os.environ["LANGCHAIN_TRACING_V2"]="true"
#os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

# prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", " you are an AI Assistant to help in cooking. please give 3-4 indian cuisines that can be made with the vegetables available with user."),
        ("user", "vegetables/ingredients: {question}")
    ]
)
vegetable_options = [
    "Potato", "Tomato", "Onion", "Carrot", "Spinach", "Cauliflower",
    "Bell Pepper", "Green Beans", "Peas", "Cucumber", "Eggplant",
    "Zucchini", "Mushroom", "Broccoli", "Cabbage","Spinach", "Dal","cluster beans"
]
def split_on_cuisine(text):
    # Custom splitting logic to identify and split cuisines
    pattern = r'(?<=\D)(?=\d)|(?<=\d)(?=\D)'
    split_text = re.split(pattern, text)
    # Further refine split logic to ensure proper division of cuisines
    cuisines = []
    temp_cuisine = ""
    for part in split_text:
        if part.strip().isdigit():
            if temp_cuisine:
                cuisines.append(temp_cuisine.strip())
            temp_cuisine = ""
        temp_cuisine += part
    if temp_cuisine:
        cuisines.append(temp_cuisine.strip())
    return cuisines
#streamlit
st.title(' Kitchenbot')
selected_vegetables = st.multiselect("Select the vegetables you have:", vegetable_options)

if selected_vegetables:
    input_text = ', '.join(selected_vegetables)

    llm = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo")
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    # Get the list of cuisines
    response = chain.invoke({'question': input_text})
    cuisines = split_on_cuisine(response)
      # Assumes response is a comma-separated list of cuisines
    cuisines = [cuisine.strip() for cuisine in cuisines]  # Clean up any extra whitespace

    # Display the list of cuisines and allow the user to select one
    selected_cuisine = st.selectbox("Select a cuisine for detailed recipe:", cuisines)

    if selected_cuisine:
        if st.button('Get Detailed Recipe'):
            detailed_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "You are an AI Assistant to help in cooking. Please provide detailed recipes with step-by-step instructions for the following Indian cuisine: {cuisine}."),
                    ("user", f"cuisine: {selected_cuisine}")
                ]
            )
            detailed_chain = detailed_prompt | llm | output_parser
            detailed_recipe = detailed_chain.invoke({'cuisine': selected_cuisine})
            st.write(detailed_recipe)

        if st.button('Get Nutritional Information'):
            nutrition_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "You are an AI Assistant to help in cooking. Please provide nutritional information for the following Indian cuisine: {cuisine}."),
                    ("user", f"cuisine: {selected_cuisine}")
                ]
            )
            nutrition_chain = nutrition_prompt | llm | output_parser
            nutrition_info = nutrition_chain.invoke({'cuisine': selected_cuisine})
            st.write(nutrition_info)

        if st.button('Generate Shopping List'):
            shopping_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "You are an AI Assistant to help in cooking. Please generate a shopping list for the following Indian cuisine: {cuisine}."),
                    ("user", f"cuisine: {selected_cuisine}")
                ]
            )
            shopping_chain = shopping_prompt | llm | output_parser
            shopping_list = shopping_chain.invoke({'cuisine': selected_cuisine})
            st.write(shopping_list)

        if st.button('Suggest Ingredient Substitutions'):
            substitution_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "You are an AI Assistant to help in cooking. Please suggest ingredient substitutions for the following Indian cuisine: {cuisine}."),
                    ("user", f"cuisine: {selected_cuisine}")
                ]
            )
            substitution_chain = substitution_prompt | llm | output_parser
            substitutions = substitution_chain.invoke({'cuisine': selected_cuisine})
            st.write(substitutions)
