import pandas as pd
import streamlit as st  # Import python packages
from snowflake.snowpark.context import get_active_session

session = get_active_session()  # Get the current credentials
pd.set_option("max_colwidth", None)
num_chunks = 3  # Num-chunks provided as context. Play with this to check how it affects your accuracy


def create_prompt(myquestion, rag):
    if rag == 1:
        cmd = """
         with results as
         (SELECT RELATIVE_PATH,
           VECTOR_COSINE_SIMILARITY(docs_chunks_table.chunk_vec,
                    SNOWFLAKE.CORTEX.EMBED_TEXT_768('e5-base-v2', ?)) as similarity,
           chunk
         from docs_chunks_table
         order by similarity desc
         limit ?)
         select chunk, relative_path from results 
         """

        df_context = session.sql(cmd, params=[myquestion, num_chunks]).to_pandas()

        context_lenght = len(df_context) - 1

        prompt_context = ""
        for i in range(0, context_lenght):
            prompt_context += df_context._get_value(i, "CHUNK")

        prompt_context = prompt_context.replace("'", "")
        relative_path = df_context._get_value(0, "RELATIVE_PATH")

        prompt = f"""
          'You are an expert assistance extracting information from context provided. 
           Answer the question based on the context. Be concise and do not hallucinate. 
           If you don´t have the information just say so.
          Context: {prompt_context}
          Question:  
           {myquestion} 
           Answer: '
           """
        cmd2 = f"select GET_PRESIGNED_URL(@docs, '{relative_path}', 360) as URL_LINK from directory(@docs)"
        df_url_link = session.sql(cmd2).to_pandas()
        url_link = df_url_link._get_value(0, "URL_LINK")

    else:
        prompt = f"""
         'Question:  
           {myquestion} 
           Answer: '
           """
        url_link = "None"
        relative_path = "None"

    return prompt, url_link, relative_path


def complete(myquestion, model_name, rag=1):
    prompt, url_link, relative_path = create_prompt(myquestion, rag)
    cmd = """
             select SNOWFLAKE.CORTEX.COMPLETE(?,?) as response
           """

    df_response = session.sql(cmd, params=[model_name, prompt]).collect()
    return df_response, url_link, relative_path


def display_response(question, model, rag=0):
    response, url_link, relative_path = complete(question, model, rag)
    res_text = response[0].RESPONSE
    st.markdown(res_text)
    if rag == 1:
        display_url = f"Link to [{relative_path}]({url_link}) that may be useful"
        st.markdown(display_url)


# Main code

st.title("Asking Questions to Your Own Documents with Snowflake Cortex:")
st.write(
    """You can ask questions and decide if you want to use your documents for context or allow the model to create their own response."""
)
st.write("This is the list of documents you already have:")
docs_available = session.sql("ls @docs").collect()
list_docs = []
for doc in docs_available:
    list_docs.append(doc["name"])
st.dataframe(list_docs)

# Here you can choose what LLM to use. Please note that they will have different cost & performance
model = st.sidebar.selectbox(
    "Select your model:",
    (
        "mixtral-8x7b",
        "snowflake-arctic",
        "mistral-large",
        "llama3-8b",
        "llama3-70b",
        "reka-flash",
        "mistral-7b",
        "llama2-70b-chat",
        "gemma-7b",
    ),
)

question = st.text_input(
    "Enter question",
    placeholder="Is there any special lubricant to be used with the premium bike?",
    label_visibility="collapsed",
)

rag = st.sidebar.checkbox("Use your own documents as context?")

print(rag)

if rag:
    use_rag = 1
else:
    use_rag = 0

if question:
    display_response(question, model, use_rag)
