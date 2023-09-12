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
# automatically pip install the requirements. - DONE


# TODO:
# Use Chain of thought reasoning for more complex functions. Break them down into smaller components


# TODO (MAJOR STEPS):
# create a virtual environment to containerize the application? - Ask Dad about this one.
# Build a tool that lets you upload external interface documentation with the necessary API keys.
# - Generated functions can then incorporate these API's
# Add support for making databases, to create stateful APIs.
# use GPT-4 eventually for far better performance.
