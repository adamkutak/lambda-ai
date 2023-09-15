# COMPLETE:
# Check for valid python code: use black formatting, seems to work perfectly (also added running the python code once over)
# JSON returning: seems to work fine 99%? Very occasional we get weird errors with "incorrect delimiter" or similar.
# - seems like the error handling can fix it though.
# Create fastAPI function definition via templates. Don't generate it with AI.
# - this half works. We generate the definition/decorator and give it to the AI.
# turn some repetitive code into callable functions and add more class structure - (v1 DONE!)
# test reliability, find more possible errors that can arise and patch them - (Done for now??)
# JSON errors: implement 1-shot preprompting to improve performance - DONE, seems perfect.
# If we fail to create the function, the code should try again starting from scratch (new message history) - DONE
# automatically pip install the requirements. - DONE (builds requirements file for APIEnv)


# TODO:
# # Add support for making databases, to create stateful APIs (v1 in progress)
# minor: validating the json in the validate_and_test_function is sort of wierd
# - if we ever want to preprocess the ai output, we can't (or have to do it in 2 places)
# minor: figure out how to import the execute_sql call, we don't want to have to copy it into the api_file.
# minor: DB should be attached to APIEnvironment? Not the API function.
# - an Env can only have 1 db, but right now the API functions in the env could all point to different DBs.
# Use Chain of thought reasoning for more complex functions. Break them down into smaller components
# one-shot preprompting WITH databases (and then with chain of thought reasoning as well)


# TODO (MAJOR STEPS):
# auto-testing: can we make testing easier for the user? Especially when DB's are involved
# - get the AI to generate tests, or at least write some rows to the sql DB to test the api functions with the DB.
# - without this, the user has to know whats in the DB ahead of time, makes things much harder to test for non-technical user.
# create a virtual environment to containerize the application? - Ask Dad about this one.
# - some form of containerization/compartmentalization
# Build a tool that lets you upload external interface documentation with the necessary API keys.
# - Generated functions can then incorporate these API's
# use GPT-4 eventually for far better performance.
# telemetry/logging of actions taken.
