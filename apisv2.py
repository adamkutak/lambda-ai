# TODO: this is a placeholder to replace the original make_api function.
# I want to make it more modular and components based.
# generating, validating, testing, and adding it to the master api file
# should be independent steps
def make_api_v2(
    name: str,
    path: str,
    inputs: dict,
    outputs: dict,
    functionality: str,
) -> str:
    # generate the new api function:
        # generate the decorator and definition without AI, just templates.
        # create the function by passing in the definition, decorator, and functionality
        # check if the function works in python
            # firstly, making sure it can run.
            # secondly, testing the test cases for validity
            # if there are issues, we pass this back to the AI to retry making the function
            # this is all done in a loop until we have the correct function working
        #FUTURE: external APIs will be needed. if the AI decides to use an external API as part of its 
        #        generated function, it will ask the user to generate an API key for a specific product!

    # Test new API function:
        # adding additional AI based verification:
            # ask AI for potential issues with the function..?
            # IDEA: use langchain agents to create fake data to test on the API?
            # ask AI if this function is a suspected hacker attempt? (trying to access sensitive info)

    # Add new API function to the existing list:
        # better way than just appending to one python file? 
        # how do we deploy the new endpoint?
            # just run the server with the updated master file
            # or, some kind of compartmentalized approach so each endpoint can be run independently?