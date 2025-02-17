import streamlit as st
import json

st.title("🌱 Ultimate Drag-and-Drop Garden Planner")

# User chooses grid size dynamically
grid_size = st.slider("Select Grid Size:", min_value=5, max_value=15, value=10, step=1)

# Initialize session state for saved garden
if "garden_layout" not in st.session_state:
    st.session_state["garden_layout"] = {}

# Plant list
plants = ["🥕 Carrot", "🍅 Tomato", "🌽 Corn", "🥬 Lettuce", "🧅 Onion", "🥔 Potato", "🫑 Bell Pepper", 
          "🌶️ Chili", "🍆 Eggplant", "🥒 Cucumber", "🥦 Broccoli", "🥗 Spinach", "🥜 Peanuts", "🫘 Beans", 
          "🌱 Peas", "🎃 Pumpkin", "🍠 Sweet Potato", "🥬 Cabbage", "🍓 Strawberry", "🍉 Watermelon", 
          "🍌 Banana", "🍎 Apple", "🍊 Orange", "🍍 Pineapple", "🍋 Lemon", "🍑 Peach", "🍐 Pear", 
          "🍇 Grapes", "🥭 Mango", "🫐 Blueberry", "🥥 Coconut", "🌿 Basil", "🌱 Mint", "🌿 Cilantro", 
          "🪴 Parsley", "🌿 Thyme", "🌿 Oregano", "🧄 Garlic", "🧂 Dill", "🫚 Ginger", "🍵 Chamomile", 
          "🍁 Sage", "🍃 Bay Leaf", "🌼 Lavender"]

# HTML + JavaScript for Drag-and-Drop Grid
html_code = f"""
<style>
    .garden-container {{
        border: 5px solid #8B4513;
        background-color: #deb887;
        padding: 10px;
        display: inline-block;
    }}
    .grid-container {{
        display: grid;
        grid-template-columns: repeat({grid_size}, 50px);
        grid-template-rows: repeat({grid_size}, 50px);
        gap: 2px;
        background-color: #ddd;
        padding: 10px;
    }}
    .grid-item {{
        width: 50px;
        height: 50px;
        background-color: white;
        border: 1px solid black;
        text-align: center;
        font-size: 18px;
        user-select: none;
    }}
    .draggable {{
        width: 50px;
        height: 50px;
        background-color: lightgreen;
        cursor: grab;
        border: 2px solid green;
        text-align: center;
        line-height: 50px;
    }}
</style>

<div>
    <h3>🌿 Drag a plant into the garden:</h3>
    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
        {"".join(f'<div id="{plant}" class="draggable" draggable="true" ondragstart="drag(event)">{plant}</div>' for plant in plants)}
    </div>
</div>

<div class="garden-container">
    <h3 style="text-align: center;">🪴 Garden Bed</h3>
    <div class="grid-container" id="garden-grid">
        {"".join(f'<div class="grid-item" id="cell-{i}" ondrop="drop(event, {i})" ondragover="allowDrop(event)"></div>' for i in range(grid_size**2))}
    </div>
</div>

<button onclick="saveGarden()">💾 Save Layout</button>
<button onclick="loadGarden()">🔄 Load Layout</button>

<script>
function allowDrop(event) {{
    event.preventDefault();
}}

function drag(event) {{
    event.dataTransfer.setData("text", event.target.id);
}}

function drop(event, cellId) {{
    event.preventDefault();
    var data = event.dataTransfer.getData("text");
    var draggedElement = document.getElementById(data);
    var clonedElement = draggedElement.cloneNode(true);
    clonedElement.removeAttribute("id");
    event.target.innerHTML = "";
    event.target.appendChild(clonedElement);

    // Save to localStorage
    var gardenData = JSON.parse(localStorage.getItem("garden")) || {{}};
    gardenData[cellId] = data;
    localStorage.setItem("garden", JSON.stringify(gardenData));

    fetch('/save_garden', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(gardenData)
    }});
}}

function saveGarden() {{
    alert("Garden layout saved! 💾");
}}

function loadGarden() {{
    fetch('/load_garden')
    .then(response => response.json())
    .then(gardenData => {{
        for (const [cellId, plant] of Object.entries(gardenData)) {{
            let cell = document.getElementById("cell-" + cellId);
            if (cell) {{
                cell.innerHTML = '<div class="draggable">' + plant + '</div>';
            }}
        }}
    }});
}}
</script>
"""

# Save and Load Functions
def save_garden_layout():
    with open("garden_layout.json", "w") as f:
        json.dump(st.session_state["garden_layout"], f)

def load_garden_layout():
    try:
        with open("garden_layout.json", "r") as f:
            st.session_state["garden_layout"] = json.load(f)
    except FileNotFoundError:
        st.session_state["garden_layout"] = {}

# API Endpoint for Saving Garden
if st.button("Save Layout 💾"):
    save_garden_layout()
    st.success("Garden layout saved!")

# API Endpoint for Loading Garden
if st.button("Load Layout 🔄"):
    load_garden_layout()
    st.success("Garden layout loaded!")

# Render the HTML
st.components.v1.html(html_code, height=900)
