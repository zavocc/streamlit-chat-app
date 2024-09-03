import streamlit as st
class SideBar:
    def __init__(self):
        self.uploaded_file = None

    def sidebar(self, models):
        with st.sidebar:
            st.session_state.session_info.update({"model": st.selectbox('Select Model', models)})

            # Image upload as context
            self.camera_mode = st.toggle("Use Camera?", value=False)
            if self.camera_mode is False:
                self.uploaded_file = st.file_uploader("Jakey can read files, upload files to be added in context.", type=["png"], accept_multiple_files=True)
            else:
                self.uploaded_file = st.camera_input("Jakey can see your surroundings, take a photo to be added in context.")