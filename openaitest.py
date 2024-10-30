from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client=OpenAI()

# A set of all the terms that can end the conversation. Set has O(1) lookup
EXIT_TERMS = {'bye', 'exit', 'quit'}

# Example of relevant info
RELEVANT_INFO = """ H20 Poke grill is is dedicated to serving the freshest ingredients and uniquely 
    crafted island flavors from Hawaii to create the perfect poké bowl. They are located at 13262 Jamboree Rd
    Irvine, CA 92602. Their hours are Monday through Sunday from 11AM to 9PM. A bowl of poke costs 14.99 with 2 protein choices or 16.99
    with 3 proteins. The proteins offered are, Ahi Tuna, Salmon, Albacore, Octopus, Shrimp, and Scallops. They also serve 
    crunch rolls for 8.95, california rolls for 6.95, and chicken hibachi for 13.95.
    """


#########
# Call on Chat-GPT to generate a response based on a templated prompt
# For future self - implement vector embedding to alleviate
#########

def generate_response(user_message):
    
    prompt = """
    You are a helpful assistant working at H20 Poke. This is some information about the business %s

    Respond concisely with the most accurate and relevant information.
    """ %RELEVANT_INFO

    response = client.chat.completions.create(
        model= 'gpt-4o-mini', 
        messages= [{
            "role": "user",
            "content": prompt}, 
            {
                "role": "user",
                "content": user_message
            }])

    print("AI: " + response.choices[0].message.content)
    return

if __name__ == '__main__':

    while True:
        user_message = input("Text: ")
        
        if user_message.lower() in EXIT_TERMS:
            break

        generate_response(user_message)



"""
Helper function for testing strings.

def testpythonstring():
    neword = "this is so dumbbbbbbb"

    thing = ""
    So this is going to be a test of how this works lets see if it does: %s
    "" %neword

    print(thing)


"""