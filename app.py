import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

def getLLMResponse(form_input,email_sender,email_recipient,email_style):

    llm = AzureChatOpenAI(
    azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],       
    openai_api_key=st.secrets["AZURE_OPENAI_API_KEY"],
    openai_api_version="2024-06-01",
    model_name=st.secrets["AZURE_OPENAI_DEPLOYMENT"], 
    temperature=0.9
)

    template = """
    Write a email with {style} style and includes topic :{email_topic}.\n\nSender: {sender}\nRecipient: {recipient}
    \n\nEmail Text:
    
    """
    prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that writes professional emails."),
    ("human", template)
])

    response=llm.invoke(prompt.format(email_topic=form_input,
                                      sender=email_sender,
                                      recipient=email_recipient,
                                      style=email_style
                                      )
                        )
    print(response.content)

    return response.content

st.set_page_config(page_title="Generate Emails",
                    page_icon='📧',
                    layout='centered',
                    initial_sidebar_state='collapsed')
st.header("Generate Emails 📧")

form_input = st.text_area('Enter the email topic', height=275)
col1, col2, col3 = st.columns([10, 10, 5])
with col1:
    email_sender = st.text_input('Sender Name')
with col2:
    email_recipient = st.text_input('Recipient Name')
with col3:
    email_style = st.selectbox('Writing Style',
                                    ('Formal', 'Appreciating', 'Not Satisfied', 'Neutral'),
                                       index=0)


submit = st.button("Generate")

if submit:
    st.write(getLLMResponse(form_input,email_sender,email_recipient,email_style))
