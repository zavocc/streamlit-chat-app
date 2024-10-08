from core.ai.excerpts.openai import ExcerptsSlash
from core.ai.reusables import SideBar
import streamlit as st
import base64
import json
import yaml
import openai

st.set_page_config(
    page_title="OpenAI GPT-4",
    page_icon="🧠",
)

# session state containg model and chat history
if "session_info_openai" not in st.session_state:
    st.session_state["session_info_openai"] = {
        "model": None,
        "chat_history": []
    }

# Initiate system prompt
with open("data/assistants.yaml", "r") as _sysprompt:
    system_prompt = yaml.safe_load(_sysprompt)

# Sidebar
_sb = SideBar()
_sb.sidebar(provider="openai", models=[
            "gpt-4o-2024-08-06",
            "gpt-4o-mini",
            "gpt-4-turbo-2024-04-09"
            ])

# Display chat history from session state, if not empty
if len(st.session_state["session_info_openai"]["chat_history"]) > 0:
    for message in st.session_state["session_info_openai"]["chat_history"]:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"][0]["text"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"][0]["text"])

# Initiate client
_client = openai.Client()

# User prompt
_prompt = st.chat_input("Ask me anything, use /reset to reset chat history", max_chars=4096)  

if _prompt:
    if _prompt.startswith("/"):
        # Excerpts
        _excerpts = ExcerptsSlash(provider="openai", state=st.session_state)
        __command = _prompt.split(" ")[0].replace("/","")

        # Execute
        if hasattr(_excerpts, __command):
            __result = _excerpts.__getattribute__(__command)()
            if __result == "<terminate>":
                st.rerun()

    # Append user prompt to chat history
    st.session_state["session_info_openai"]["chat_history"].append({
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
    if _sb.uploaded_file and not _sb.camera_mode:
        for _files in _sb.uploaded_file:
            # Max files is 8
            if len(_image_data) >= 8:
                st.toast("Max files is 8! Please remove some files.")
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
    elif _sb.uploaded_file and _sb.camera_mode:
        _image_data = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64.b64encode(_sb.uploaded_file.getvalue()).decode('utf-8')}",
                            },
                        },
                    ],
                }
            ]
        
    # Send message through UI
    with st.chat_message("user"):
        st.markdown(_prompt)

    # Get response from OpenAI
    _response = _client.chat.completions.create(
            model=st.session_state["session_info_openai"]["model"],
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": system_prompt["openai"]["system_prompt"]
                        }
                    ]
                },
            ] + st.session_state["session_info_openai"]["chat_history"] + _image_data + st.session_state["session_info_openai"]["chat_history"] ,
            temperature=_sb.temperature,
            max_tokens=_sb.max_tokens,
            top_p=_sb.top_p,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "text"
            }
        )
    
    # Send message through UI
    with st.chat_message("assistant"):
        st.markdown(_response.choices[0].message.content)

    # Append response to chat history
    st.session_state["session_info_openai"]["chat_history"].append(
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

# Post chat controls
with st.sidebar:
    # Export conversation as JSON
    if len(st.session_state["session_info_openai"]["chat_history"]) > 0:
        _jsonized = json.dumps(st.session_state["session_info_openai"]["chat_history"], indent=4)
        st.write("Export conversation as JSON")
        st.download_button(
            label="Export conversation",
            data=_jsonized,
            file_name="chat_history.json",
            mime="application/json"
        )

