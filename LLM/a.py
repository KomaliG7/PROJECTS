from autogen import ConversableAgent,UserProxyAgent
llm_config={
    "model":"deepseek-r1:1.5b",
    "base_url":"http://localhost:11434/v1",
    "api_key":"ollama",
    "timeout":120
}
codebuddy=ConversableAgent(
    name="codebuddy",
    llm_config=llm_config,
    system_message="I'm at your service master,Let me clear ctitical doubt arised in your intelligent brain!!!"
)
user=UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=0,
    code_execution_config={"use_docker":False},
    is_termination_msg=lambda msg:exit in msg.get("content",'').lower()
)
if __name__=="__main__":
    print("lets start the conversation")
    while True:
        user_msg = input("enter")
        if user_msg.strip().lower()=="exit":
            print("Conversation terminated. See you next time!")
            break
        user.initiate_chat(codebuddy,message=user_msg)