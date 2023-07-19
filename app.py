#required dis
import os 
import streamlit as st 
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import GooglePalm 
from langchain.memory import ConversationBufferWindowMemory

#env 
palm_api = os.environ.get('palm_api')


def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please start the email with a Subject and warm introduction. Add the introduction if you need to. 
    
    Below is the email, tone, and dialect:

    TONE: {tone}

    DIALECT: {dialect}

    EMAIL: {email}

    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=template,
    output="answer"
)
email_memory = ConversationBufferWindowMemory(memory_key='chat_history', window_size=5)

def load_LLM(api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your PALM_KEY is set as an environment variable
    llm = GooglePalm(temperature=0.5, google_api_key=api_key)
    return llm


# App framework
st.set_page_config("Email Fixer", page_icon="🦜")
st.header("Email Fixer")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Often professionals would like to improve their emails, but don't have the skills to do so. \n\n This tool \
                will help you improve your email skills by converting your emails into a more professional format. This tool \
                is powered by [LangChain](https://langchain.com/) and made by \
                [@shubharthaksangharsha](https://in.linkedin.com/in/shubharthaksangharsha). \n\n View Source Code on [Github](https://github.com/shubharthaksangharsha/email-fixer/blob/main/app.py)")

with col2:
    st.image(image='TweetScreenshot.png', width=500, caption='https://twitter.com/DannyRichman/status/1598254671591723008')

st.markdown("## Enter Your Email To Convert")

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your email to have?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))

def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "Sally I am starts work at yours monday from dave"

st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Converted Email:")

if email_input:
    llm = load_LLM(api_key=palm_api)

    llm_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    output = llm_chain.run({
        'tone': option_tone,
        'dialect': option_dialect,
        'email': email_input
    })
    # memory.chat_memory.add_message(output)
    st.write(output)

# with st.expander('Mail History'): 
#     st.write(email_memory.buffer)

