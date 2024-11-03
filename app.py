import streamlit as st
import pandas as pd
import os
from datetime import datetime
from SimplerLLM.language.llm import LLM, LLMProvider

# Initialize the LLM instance
llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-3.5-turbo")

# Load tasks from a file
def load_tasks():
    if os.path.exists('tasks.csv'):
        return pd.read_csv('tasks.csv')
    return pd.DataFrame(columns=['Task', 'Description', 'Deadline', 'Priority'])

# Save tasks to a file
def save_tasks(tasks):
    tasks.to_csv('tasks.csv', index=False)

# Add a task
def add_task(task, description, deadline, priority):
    tasks = load_tasks()
    new_task = pd.DataFrame({'Task': [task], 'Description': [description], 'Deadline': [deadline], 'Priority': [priority]})
    tasks = pd.concat([tasks, new_task], ignore_index=True)
    save_tasks(tasks)

# Generate task recommendations
def generate_recommendation():
    tasks = load_tasks()
    task_list = tasks['Task'].tolist()
    
    if not task_list:
        return "No tasks available to generate recommendations."
    
    task_list_str = ', '.join(task_list)
    prompt = f"Given the following tasks: {task_list_str}, please suggest additional useful tasks that could enhance productivity."
    
    # Correctly call generate_response with prompt
    return llm_instance.generate_response(prompt=prompt)

# Streamlit UI
st.title("AI-Powered Task Planner")
st.markdown("Organize your tasks efficiently and get smart recommendations.")

# Add Task Section
with st.form(key='add_task_form'):
    task = st.text_input("Task Title")
    description = st.text_area("Description")
    deadline = st.date_input("Deadline", datetime.today())
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submit_button = st.form_submit_button("Add Task")
    
    if submit_button:
        add_task(task, description, deadline, priority)
        st.success(f'Task "{task}" added!')

# Show Tasks
tasks = load_tasks()
if not tasks.empty:
    st.subheader("Your Tasks")
    st.dataframe(tasks)

# Get Recommendations
if st.button("Get Task Recommendations"):
    recommendation = generate_recommendation()
    st.subheader("Recommendations")
    st.write(recommendation)
