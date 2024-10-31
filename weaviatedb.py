import weaviate
import os

from dotenv import load_dotenv

from weaviate.classes.tenants import Tenant

from langchain_weaviate.vectorstores import VectorStore
from langchain_openai import OpenAIEmbeddings

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()

api_key= os.getenv("OPENAI_API_KEY")
client = weaviate.connect_to_local()
embeddings = embeddings = OpenAIEmbeddings()

def close_client():
    client.close()

def replace_tenant_data(collection_name= "TextFiles", user_id="H20Poke", filepath="/Users/jairobedolla/funprojects/AIPhoneBot/H2OPoke.txt"):
    clear_tenant_data(collection_name, user_id)
    add_data_to_table(collection_name, user_id, filepath)

def clear_tenant_data(collection_name= "TextFiles", user_id="H20Poke"):
    vs = client.collections.get(collection_name)
    vs.tenants.remove(user_id) # Removing clears all the data
    vs.tenants.create(user_id)

def add_tenant_to_table(collection_name= "TextFiles", user_id="H20Poke"):
    textfiles = client.collections.get(collection_name)
    textfiles.tenants.create(user_id)

def add_data_to_table(collection_name= "TextFiles", user_id="H20Poke", filepath="/Users/jairobedolla/funprojects/AIPhoneBot/H2OPoke.txt"):
    textfiles = client.collections.get(collection_name)
    tenant = textfiles.with_tenant(user_id)

    loader = TextLoader(filepath)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)

    for doc in docs:
        tenant.data.insert(
            properties={
                "content": doc.page_content
            }
        )

def get_context_for_query(collection_name, user_id, query):
    textfiles = client.collections.get(collection_name)
    tenant = textfiles.with_tenant(user_id)
    response = tenant.query.near_text(
        query=query,
        limit=3
    )
    return response
    

def create_text_schema():
    collection_name = "TextFiles"

    if client.collections.exists(collection_name):  # In case we've created this collection before
        client.collections.delete(collection_name)

    client.collections.create(
        name = collection_name,
        vectorizer_config= weaviate.classes.config.Configure.Vectorizer.text2vec_openai(),
        properties=[
            weaviate.classes.config.Property(
                name="content",
                data_type=weaviate.classes.config.DataType.TEXT,
            )
        ],
        multi_tenancy_config=weaviate.classes.config.Configure.multi_tenancy(enabled=True)
    )
         

def create_json_schema():
    collection_name = "QAEntries"

    if client.collections.exists(collection_name):  # In case we've created this collection before
        client.collections.delete(collection_name)

    client.collections.create(
        name = collection_name,
        vectorizer_config= weaviate.classes.config.Configure.Vectorizer.text2vec_openai(),
        properties=[
            weaviate.classes.config.Property(
                name="question",
                data_type=weaviate.classes.config.DataType.TEXT,
            ),
            weaviate.classes.config.Property(
                name="answer",
                data_type=weaviate.classes.config.DataType.TEXT,
            ),
            weaviate.classes.config.Property(
                name="category",
                data_type=weaviate.classes.config.DataType.TEXT,
            )

        ],
        multi_tenancy_config=weaviate.classes.config.Configure.multi_tenancy(enabled=True)
    )
    faq_schema = {
        "class": "FAQ",
        "description": "A class to store FAQ entries from a JSON file with vector embeddings.",
        "properties": [
            {
                "name": "category",
                "dataType": ["string"],
                "description": "The category or topic of the FAQ entry.",
            },
            {
                "name": "question",
                "dataType": ["text"],
                "description": "The question part of the FAQ entry.",
            },
            {
                "name": "answer",
                "dataType": ["text"],
                "description": "The answer part of the FAQ entry.",
            },
        ],
        "vectorizer": "text2vec-openai",
        "multiTenancyConfig": {
            "enabled": True
        }
    }
    client.schema.create_class(faq_schema)
    print("FAQ schema created.")



if __name__ == '__main__':
    replace_tenant_data()

    client.close()

"""
multi_collection = client.collections.get("TextFiles")
    query = input("text: ")
    context = get_context_for_query("TextFiles", "H20Poke", query)

    for o in context.objects:
        print(o.properties.get("content"))

# Get a list of tenants
    tenants = multi_collection.tenants.get()

    # Iterate through tenants
    for tenant_name in tenants.keys():
        print(tenant_name)
        # Iterate through objects within each tenant
        for item in multi_collection.with_tenant(tenant_name).iterator():
            print(f"{tenant_name}: {item.properties}")
    client.close()
try:
    # Check if the connection is successful
    if client.is_live():
        print("Weaviate is live and ready!")
    else:
        print("Failed to connect to Weaviate.")
finally:
    # Ensure that the connection is closed to avoid resource warnings
    client.close()
    print("Weaviate connection closed.")
"""