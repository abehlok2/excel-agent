import os
import dotenv
import autogen
from autogen import AssistantAgent, UserProxyAgent
from configs.configs import palm_config_list, gpt_4_05, gpt_3_05


def term_msg(message):
    if "TERMINATE" in message["content"].upper():
        return True,
    else:
        return False


def term_msg_unsure(message):
    if "UNSURE" in message["content"].upper():
        return True,
    else:
        return False


user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin, oversees operations.",
    human_input_mode="TERMINATE",
    is_termination_msg=term_msg,
)

assistant = autogen.AssistantAgent(
    name="Assistant",
    llm_config={
        "config_list": palm_config_list,
        "seed": 32,
        "request_timeout": 120,
    },
    max_consecutive_auto_reply=3,
    human_input_mode="NEVER",
)

document_parser = autogen.AssistantAgent(
    name="Documentation_parser",
    llm_config={
        "model": "gpt-3.5-turbo-16k",
        "seed": 32,
        "request_timeout": 120,
    },
    human_input_mode="NEVER",
    system_message="""You are a documentation parsing AI. When provided documentation in the form of PDFs, MD files, URLs, etc. you will parse the documentation, summarizing the contents internally as you progress. Use the contents to provide additional insight to the group when attempting to solve questions for which the documentation is directly relevant."""
)

system_manipulator = autogen.UserProxyAgent(
    name="File_system_manipulator",
    max_consecutive_auto_reply=5,
    llm_config={
        "config_list": palm_config_list,
        "seed": 32,
        "request_timeout": 120,
    },
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": r"C:\users\abehl\projects", "use_docker": False},
    system_message="You are a Local System Manipulator. Utilize python and shell scripts and commands to perform local tasks. Execute code to accomplish the goals laid out by the ADMIN. \n\n You must **ONLY** respond with code executions. If you are unsure or unable to execute or suspect major problems with the code, respond with 'UNSURE' "
)

documentation_group_chat = autogen.GroupChat(
    agents=[user_proxy, system_manipulator, assistant, document_parser],
    admin_name="Admin",
    max_round=5
)

post_documentation_coder = autogen.AssistantAgent(
    name="Post-Documentation-Coder",
    llm_config=gpt_4_05,
    max_consecutive_auto_reply=5,
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False,
                           "work_dir": r"C:\users\abehl\downloads"}
)

manager = autogen.GroupChatManager(
    groupchat=documentation_group_chat,
    name="Coordinator",
    human_input_mode="TERMINATE",
    is_termination_msg=term_msg_unsure,
    system_message="You are the coordinator for a group of LLM-based AI agents. They will be attempting to carry out tasks as indicated by the USER (controls the admin user proxy). Interpret requests and responses and relay them appropriately to the next agent as necessary."
)


def query_group(query: str):
    messages = [
        {
            "role": "user",
            "content": query,

        }
    ]


def main():
    manager.run_chat(sender=user_proxy, config=documentation_group_chat)

    return


if __name__ == "__main__":
    main()
