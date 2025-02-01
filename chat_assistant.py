import sqlite3
import gradio as gr
from tabulate import tabulate

# Path to SQLite database
db_path = "/Users/shivanishrivastava/Desktop/project/company.db"

# Function to map user input to SQL queries
def convert_to_sql(user_query):
    user_query = user_query.lower()

    # Query 1: Show all employees in the specified department
    if "all employees in the" in user_query and "department" in user_query:
        department = user_query.split("in the")[1].split("department")[0].strip()
        return f"SELECT * FROM Employees WHERE Department = '{department}';"

    # Query 2: Who is the manager of the specified department (assuming manager is an employee)
    elif "manager of the" in user_query and "department" in user_query:
        department = user_query.split("manager of the")[1].split("department")[0].strip()
        return f"SELECT Name FROM Employees WHERE Department = '{department}' LIMIT 1;"

    # Query 3: List all employees hired after the specified date
    elif "hired after" in user_query:
        date = user_query.split("hired after")[1].strip()
        return f"SELECT * FROM Employees WHERE Hire_Date > '{date}';"

    # Query 4: Total salary expense for a department
    elif "total salary expense for the" in user_query and "department" in user_query:
        department = user_query.split("for the")[1].split("department")[0].strip()
        return f"SELECT SUM(Salary) AS Total_Salary_Expense FROM Employees WHERE Department = '{department}';"
    
    # Default query: If no matching query found
    else:
        return None

# Function to execute SQL query
def execute_sql_query(sql_query):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        
        col_names = [desc[0] for desc in cursor.description]
        conn.close()
        
        if rows:  # Check if any data is fetched
            return tabulate(rows, headers=col_names, tablefmt="pretty")
        else:
            return "No data found matching your query."
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio interface function
def sql_query_interface(user_query):
    sql_query = convert_to_sql(user_query)
    
    if sql_query:
        result = execute_sql_query(sql_query)
        return f"Generated SQL Query:\n{sql_query}\n\nResult:\n{result}"
    else:
        return "Sorry, I don't understand that query. Try asking about employees, salaries, or hire dates."

# Create Gradio interface
iface = gr.Interface(fn=sql_query_interface,
                     inputs=gr.Textbox(label="Ask me a question"),
                     outputs="text",
                     live=True,
                     title="SQLite Chat Assistant",
                     description="Ask questions related to employees, departments, or salaries in your company database.")

# Launch the Gradio interface
iface.launch() 