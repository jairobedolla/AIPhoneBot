###########
# Plan 1: Generate embeddings using OpenAI embedding models:
#       response = client.embeddings.create(input= query, model=text-embedding-3-small, user= current_user)
#       embeddings = [e['embedding'] for e in response['data']]
#      
# - Save the embeddings in a binary file with numpy:    
#       np.save('business_name.npy', embeddings)
#
# - Create a database for all users that will key on their name and contain binary file
#
# - For similarity search use cosine sim, because its easiest to computer:
#       np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))
# 
# - Find k most relevant results from embeddings w query
#       
# 
# ****THINGS TO CONSIDER
#  - Limitations on tokens for models (8191 token limit)
#       import tiktoken
#
#       def num_tokens_from_string(string: str, encoding_name: str) -> int:
#           """Returns the number of tokens in a text string."""
#           encoding = tiktoken.get_encoding(encoding_name)
#           num_tokens = len(encoding.encode(string))
#           return num_tokens
# 
#############
# Plan 2: Utilize the Weaviate library using Langchain. Already supports creating a multi tenacy db
#   with user specification in this format:
#
#       db_with_mt = WeaviateVectorStore.from_documents(
#           docs, embeddings, client=weaviate_client, tenant="Foo"
#       )
#       db_with_mt.similarity_search(query, tenant="Foo")
#
# - Stil need to generate embeddings with OpenAI (see above example)
#
#
#

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def generate_embedings(data, current_user):
    response = client.embeddings.create(input= data, model='text-embedding-3-small', user= current_user)
    embeddings = [e['embedding'] for e in response['data']]

    return embeddings