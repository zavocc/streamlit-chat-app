from systemprompt import SYSTEM_PROMPT
import streamlit as st
import base64
import openai

st.title('Jakey AI')

# session state containg model and chat history
if "session_info" not in st.session_state:
    st.session_state.session_info = {
        "model": None,
        "chat_history": []
    }

# dropdown for model selection
_models = [
    "gpt-4o-2024-08-06",
    "gpt-4o-mini",
    "gpt-4-turbo-2024-04-09"
]

st.session_state.session_info.update({"model": st.selectbox('Select Model', _models)})

# Initiate client
_client = openai.Client()

# Image upload as context
_camera_mode = st.toggle("Use Camera?", value=False)
if _camera_mode is False:
    uploaded_file = st.file_uploader("Jakey can read files, upload files to be added in context.", type=["png"], accept_multiple_files=True)
else:
    uploaded_file = st.camera_input("Jakey can see your surroundings, take a photo to be added in context.")

# User prompt
_prompt = st.chat_input("Ask me anything, use /reset to reset chat history", max_chars=4096)
if _prompt:
    if _prompt.startswith("/reset"):
        st.session_state.session_info["chat_history"] = []
    elif _prompt.startswith("/files"):
        # Send assistant message
        st.session_state.session_info["chat_history"].append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Hey I need help how to upload my files"
                    }
                ]
            }
        )

        st.session_state.session_info["chat_history"].append(
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": __import__("inspect").cleandoc(
                                """Hey there! I see you need help with uploading files.
                                
                                ### How to upload files
                                You can upload your files by clicking the "Browse files" button.
                                You can attach upto 8 images and it will be added as part of the context.

                                ### How your data is processed
                                Attachment data is stored and processed within you, the sent data is not stored or processed by us.
                                Please read the OpenAI Privacy Policy for more information how your data is processed in API side.
                                
                                During your chat session, you can add or remove files as needed without the need to reset your conversation.    """
                            )
                    }
                ]
            }
        )
    else:
        # Append user prompt to chat history
        st.session_state.session_info["chat_history"].append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": _prompt
                }
            ]
        })

        # If image is uploaded, append image to chat history
        _image_data = []
        if uploaded_file and not _camera_mode:
            for _files in uploaded_file:
                # Max files is 8
                if len(_image_data) >= 8:
                    st.write("Max files is 8! Please remove some files.")
                    break

                _image_data += [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64.b64encode(_files.getvalue()).decode('utf-8')}",
                                },
                            },
                        ],
                    }
                ]
        elif uploaded_file and _camera_mode:
            _image_data = [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64.b64encode(uploaded_file.getvalue()).decode('utf-8')}",
                                },
                            },
                        ],
                    }
                ]

        # Get response from OpenAI
        _response = _client.chat.completions.create(
                model=st.session_state.session_info["model"],
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": SYSTEM_PROMPT
                            }
                        ]
                    },
                ] + st.session_state.session_info["chat_history"] + _image_data,
                temperature=1,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={
                    "type": "text"
                }
            )

        # Append response to chat history
        st.session_state.session_info["chat_history"].append(
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": _response.choices[0].message.content
                    }
                ]
            }
        )

# Display chat history from session state, if not empty
if st.session_state.session_info["chat_history"]:
    for message in st.session_state.session_info["chat_history"]:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"][0]["text"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"][0]["text"])