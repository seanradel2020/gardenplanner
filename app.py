import streamlit as st
import plotly.express as px
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.title('Hello, Streamlit!')
st.write('Welcome to your first Streamlit app.')

def gantt():


    df = pd.DataFrame([
        dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Resource="Alex"),
        dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Resource="Alex"),
        dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Resource="Max")
    ])

    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource")
    fig.update_yaxes(autorange="reversed")

    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        st.plotly_chart(fig, theme=None)


#Grid
def grid():
    data = pd.DataFrame({
        "Plant": ["🥕 Carrot", "🌽 Corn", "🍅 Tomato", "🥬 Lettuce"],
        "Row": [1, 2, 3, 4],
        "Column": [1, 2, 3, 4]
    })

    # Configure grid with draggable rows
    builder = GridOptionsBuilder.from_dataframe(data)
    builder.configure_default_column(resizable=True, editable=True)
    builder.configure_grid_options(rowDragManaged=True)  # Enable row dragging

    st.title("🌱 Drag-and-Drop Garden Planner")

    # Create Ag-Grid with row drag enabled
    grid_response = AgGrid(data, gridOptions=builder.build(), height=300)

    st.write("Updated Garden Layout:")
    st.dataframe(grid_response["data"]) # Show updated grid data

gantt()
grid()
