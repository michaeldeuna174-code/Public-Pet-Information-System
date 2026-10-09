import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="Pet Information System", page_icon="🐾", layout="wide")

st.title("🐾 Public Pet Information System")
st.caption("Discover fun facts and browse adorable dog breeds in real-time.")
st.markdown("---")

# 1. API CALL: Kumuha ng Random Dog Trivia mula sa DogAPI.dog
def get_random_dog_fact():
    try:
        url = "https://dogapi.dog/api/v2/facts"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            fact_data = response.json()
            return fact_data["data"][0]["attributes"]["body"]
        return "Hindi makuha ang trivia sa ngayon."
    except Exception:
        return "Naka-offline ang API o walang internet connection."

# 2. API CALL: Kumuha ng Listahan ng Dog Breeds mula sa Dog CEO API
@st.cache_data
def get_all_breeds():
    try:
        url = "https://dog.ceo/api/breeds/list/all"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            breeds_dict = response.json()["message"]
            return list(breeds_dict.keys())
        return []
    except Exception:
        return []

# 3. API CALL: Kumuha ng Random Image batay sa napiling Breed
def get_breed_image(breed_name):
    try:
        url = f"https://dog.ceo/api/breed/{breed_name}/images/random"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()["message"]
        return None
    except Exception:
        return None


# --- STREAMLIT USER INTERFACE (UI) ---

# SECTION 1: Trivia Generator (Live API)
st.subheader("💡 Did You Know? (Live Pet Trivia)")
fact_text = get_random_dog_fact()
st.info(fact_text)

if st.button("🔄 Get Another Fact"):
    st.rerun()

st.markdown("---")

# SECTION 2: Breed & Picture Search (Live API)
st.subheader("🐕 Dog Breed Finder")

breeds_list = get_all_breeds()

if breeds_list:
    col1, col2 = st.columns([1, 2])

    with col1:
        selected_breed = st.selectbox(
            "Pumili ng Dog Breed:", 
            [b.capitalize() for b in breeds_list]
        )
        
        btn_search = st.button("Show Dog Picture")

    with col2:
        if selected_breed:
            breed_key = selected_breed.lower()
            image_url = get_breed_image(breed_key)
            
            st.write(f"**Selected Breed:** {selected_breed}")
            
            if image_url:
                st.image(image_url, caption=f"Live photo ng {selected_breed}", use_container_width=True)
            else:
                st.warning("Walang larawan na nahanap sa API.")
else:
    st.error("Hindi makakonekta sa Public Pet API. Siguraduhing may internet ka.")
