import streamlit as st
import csv
import os
import pandas as pd


def load_tasks():
    if os.path.exists("todo.csv"):
        df = pd.read_csv("todo.csv")

        # 🔥 Strip spaces from column names (important!)
        df.columns = df.columns.str.strip()

        # Ensure srno is int
        if "srno" in df.columns:
            df["srno"] = df["srno"].astype(int)

        return df
    else:
        return pd.DataFrame(columns=['srno','Task','Due Date','Category','Priority','Status'])

selected_val=st.sidebar.radio("choose:",['Home','Add Task','Edit Task','Show All Tasks','Completed Task','Pending Tasks'])

if selected_val=='Home':
    st.title("🗂️ To-Do List App")
    st.write("Organize your tasks, stay productive, and never miss a deadline!")

    st.write("""
    Welcome to your personal task manager.  
    With this app, you can:
    - ➕ Add new tasks with deadlines, categories, and priorities  
    - 📋 View all your tasks in one place  
    - ✅ Track what’s completed  
    - ⏳ Focus on what’s still pending  

    Start by using the navigation bar to add or view your tasks!
    """)
elif selected_val=='Add Task':
    st.title("Add a new task below:")
    task_title=st.text_input("Task Title:")
    deadline=st.date_input("Select Due Date:")
    category=st.selectbox("Category:",['Work','Study','Personal','Shopping'])
    priority=st.selectbox("Task Priority:",['High','Medium','Low'])
    status="Pending"

    if st.button("ADD TASK"):
        if not os.path.exists("todo.csv"):
            with open("todo.csv",'w',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['srno','Task','Due Date','Category','Priority','Status'])

        count = 1
        with open("todo.csv", "r") as f:
            reader = [row for row in csv.reader(f) if row]
            if len(reader) > 1:
                last_row = reader[-1]
                count = int(last_row[0]) + 1

        with open("todo.csv","a", newline='') as f:
            writer=csv.writer(f)
            writer.writerow([
                count,
                str(task_title),
                str(deadline),
                str(category),
                str(priority),
                str(status)
            ])

        st.success("✅ Task Added Successfully!")

        file="todo.csv"
        if file:
            df=pd.read_csv(file)
            st.dataframe(df.sort_values(by="srno",ascending=False))

elif selected_val=="Edit Task":
    st.title("✏️ Edit Task")
    st.write("Select a task and update its details below:")

    file="todo.csv"
    if os.path.exists(file):
        df = pd.read_csv(file)

        if not df.empty:
            srno = st.number_input("Enter Task ID (srno) to edit:", min_value=1, step=1)

            if srno in df["srno"].values:
                task_row = df[df["srno"] == srno].iloc[0]

                new_task_title = st.text_input("Task Title:", value=task_row["Task"])

                # convert string back to date
                from datetime import datetime
                try:
                    date_val = pd.to_datetime(task_row["Due Date"]).date()
                except:
                    date_val = None
                new_deadline = st.date_input("Select Due Date:", value=date_val)

                new_category = st.selectbox(
                    "Category:",
                    ['Work','Study','Personal','Shopping'],
                    index=['Work','Study','Personal','Shopping'].index(task_row["Category"])
                )

                new_priority = st.selectbox(
                    "Task Priority:",
                    ['High','Medium','Low'],
                    index=['High','Medium','Low'].index(task_row["Priority"])
                )

                new_status = st.selectbox(
                    "Status:",
                    ["Pending","Completed"],
                    index=["Pending","Completed"].index(task_row["Status"])
                )

                if st.button("Update Task"):
                    df.loc[df["srno"] == srno, ["Task", "Due Date", "Category", "Priority", "Status"]] = \
                        [new_task_title, str(new_deadline), new_category, new_priority, new_status]
                    df.to_csv(file, index=False)
                    st.success("✅ Task Updated Successfully!")
            else:
                st.warning("⚠️ No task found with this ID.")

elif selected_val=='Show All Tasks':
    st.title("📋 All Tasks")
    st.write("Here is the list of all tasks you’ve added:")

    df=load_tasks()
    if not df.empty:
        st.dataframe(df.sort_values(by="srno",ascending=False))
    else:
        st.info("No tasks found. Please add a task first.")


elif selected_val=='Completed Task':
    st.title("✅ Completed Tasks")
    st.write("Here are the tasks you have successfully completed:")

    df=load_tasks()
    completed_df = df[df["Status"] == "Completed"]

    if not completed_df.empty:
        st.dataframe(completed_df.sort_values(by="srno",ascending=False))
    else:
        st.info("No tasks completed yet. Keep going! 🚀")

elif selected_val=='Pending Tasks':
    st.title("🕒 Tasks Left To Do")
    st.write("Here are the tasks you still need to complete:")

    df=load_tasks()
    pending_tasks=df[df["Status"]=="Pending"]

    if not pending_tasks.empty:
        st.dataframe(pending_tasks.sort_values(by="srno",ascending=False))
    else:
        st.info("No Pending tasks yet.")