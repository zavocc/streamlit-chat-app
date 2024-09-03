import inspect
class ExcerptsOpenAISlash:
    def __init__(self, state):
        self.state = state

    def reset(self):
        self.state.session_info["chat_history"] = []
        return "<terminate>"

    def files(self):
        self.state.session_info["chat_history"].append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I need help with uploading files"
                    }
                ]
            }
        )

        self.state.session_info["chat_history"].append(
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": inspect.cleandoc(
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

        return "<terminate>"