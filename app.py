import streamlit as st
import json
import random
import base64

# Page configuration
st.set_page_config(page_title="BikeBot Pro", page_icon="🏍️", layout="centered")

# Helper function to set background
def set_bg(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64_encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Customizing chat bubbles */
    [data-testid="stChatMessage"] {{
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 10px;
    }}
    /* Customizing Sidebar */
    [data-testid="stSidebar"] {{
        background-color: rgba(0, 0, 0, 0.7);
    }}
    /* Text colors */
    h1, h2, h3, p, span, li {{
        color: white !important;
    }}
    .stMarkdown p {{
        font-size: 1.1rem;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Sidebar for customization
with st.sidebar:
    st.title("🛠️ Customization")
    bg_choice = st.selectbox(
        "Choose Background",
        ["Dark Garage", "Mountain Road", "Abstract Speed", "Default Dark"]
    )
    
    bg_map = {
        "Dark Garage": "bg_dark_garage.jpg",
        "Mountain Road": "bg_mountain_road.jpg",
        "Abstract Speed": "bg_abstract_speed.jpg",
        "Default Dark": None
    }
    
    selected_bg = bg_map[bg_choice]
    if selected_bg:
        try:
            set_bg(selected_bg)
        except FileNotFoundError:
            st.warning(f"Background image {selected_bg} not found. Please ensure it's in the same directory.")
    else:
        st.markdown("<style>.stApp { background-color: #0E1117; }</style>", unsafe_allow_html=True)

    st.markdown("---")
    st.write("### About BikeBot")
    st.write("Your ultimate motorcycle companion. Ask me anything about bike specs, prices, and more!")

# Load data
@st.cache_data
def load_data():
    try:
        with open("bike.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"bikes": []}

data = load_data()

# Chatbot Logic (Same as original)
off_topic_reply = [
    "I am a Bike Information Chatbot only.",
    "Please ask questions related to motorcycles.",
    "Try asking about KTM, Yamaha, BMW, Kawasaki, Ducati, Honda, Suzuki etc.",
    "Example:\n• Tell me about Hayabusa\n• Price of BMW S1000RR\n• Mileage of Yamaha R15 V4"
]

parameters = {
    "engine": "engine_cc", "power": "power_hp", "horsepower": "power_hp",
    "torque": "torque_nm", "mileage": "mileage_kmpl", "price": "price_inr",
    "top speed": "top_speed_kmph", "speed": "top_speed_kmph", "fuel tank": "fuel_tank_l",
    "weight": "weight_kg", "seat height": "seat_height_mm", "ground clearance": "ground_clearance_mm",
    "wheelbase": "wheelbase_mm", "transmission": "transmission", "cooling": "cooling",
    "abs": "abs", "traction": "traction_control", "quick shifter": "quick_shifter",
    "ride modes": "ride_modes", "headlight": "headlight", "console": "console",
    "bluetooth": "bluetooth", "navigation": "navigation", "launch year": "launch_year",
    "emission": "emission", "rating": "rating", "country": "country",
    "color": "colors", "colour": "colors", "service": "service_interval_km",
    "warranty": "warranty_years"
}

def find_bike(text):
    for bike in data.get("bikes", []):
        if bike["name"].lower() in text.lower():
            return bike
    return None

def get_all_details(bike):
    response = f"### 🏍️ {bike['name']}\n"
    response += "---"
    for key, value in bike.items():
        if key == "name" or key == "image": continue
        if isinstance(value, list): value = ", ".join(map(str, value))
        response += f"\n**{key.replace('_',' ').title()}** : {value}"
    return response

def get_parameter_response(bike, user_input):
    for keyword, field in parameters.items():
        if keyword in user_input.lower():
            value = bike.get(field, "Not Available")
            if isinstance(value, list): value = ", ".join(map(str, value))
            response = f"### 🏍️ {bike['name']}\n---\n**{keyword.title()}** : {value}"
            return response
    return None

def process_response(user_input):
    bike = find_bike(user_input)
    if bike:
        param_resp = get_parameter_response(bike, user_input)
        return param_resp if param_resp else get_all_details(bike)
    return random.choice(off_topic_reply)

# Streamlit UI
st.title("🏍️ BikeBot Pro")
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask about a bike..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = process_response(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
