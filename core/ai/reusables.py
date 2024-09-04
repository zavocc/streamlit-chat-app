import streamlit as st
class SideBar:
    def __init__(self):
        self.max_tokens = 1024
        self.temperature = 0
        self.top_p = 0.95
        self.uploaded_file = None


    def sidebar(self, provider, models):
        with st.sidebar:
            st.session_state[f"session_info_{provider}"].update({"model": st.selectbox('Select Model', models)})

            # Image upload as context
            self.camera_mode = st.toggle("Use Camera?", value=False)
            if self.camera_mode is False:
                self.uploaded_file = st.file_uploader("Jakey can read files, upload files to be added in context.", type=["png"], accept_multiple_files=True)
            else:
                self.uploaded_file = st.camera_input("Jakey can see your surroundings, take a photo to be added in context.")

            with st.expander("Advanced settings"):
                st.write("CHANGING SETTINGS MAY PRODUCE UNEXPECTED RESULTS")
                self.max_tokens = st.number_input("Max output tokens", min_value=100, max_value=8192, step=1, value=1024)
                self.temperature = st.number_input("Temperature", min_value=0.0, max_value=2.0, step=0.01, value=0.0)
                self.top_p = st.number_input("top_p (EXPERIMENTAL)", min_value=0.10, max_value=1.0, step=0.05, value=0.95)

