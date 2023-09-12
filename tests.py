from dotenv import load_dotenv
import openai
import os
from apisv2 import APIFunction

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")


def test_basic_1():
    repetition = 1
    build_result_list = []
    for i in range(repetition):
        api_function = APIFunction(
            "subtract_quantity",
            "/tests/set1/",
            {
                "item_id": "int",
                "status": "bool",
                "bought": "int",
            },
            {
                "item_id": "int",
                "quantity": "int",
            },
            "quantity is 100. If status is true, deduct bought from quantity.",
            test_cases=[
                {
                    "input": {
                        "item_id": 9478,
                        "status": True,
                        "bought": 99,
                    },
                    "output": {
                        "item_id": 9478,
                        "quantity": 1,
                    },
                },
                {
                    "input": {
                        "item_id": 1234,
                        "status": False,
                        "bought": 99,
                    },
                    "output": {
                        "item_id": 1234,
                        "quantity": 100,
                    },
                },
                {
                    "input": {
                        "item_id": 645609,
                        "status": True,
                        "bought": 105,
                    },
                    "output": {
                        "item_id": 645609,
                        "quantity": -5,
                    },
                },
            ],
        )

        _, result_message = api_function.create_api_function()
        print("-----0------")
        print(f"i: {i}")
        print(api_function.build_attempts)
        print(result_message)
        build_result_list.append(api_function.build_attempts)

    print(build_result_list)


def test_basic_2():
    repetition = 1
    build_result_list = []
    function_def = """take the logarithm of the sum of the ascii character values of the ability input.
The base of the log is 5 if ability starts with an 'h' and ends with a 't', otherwise its 10. 
After getting the logarithm, return it to the power of exponent. 
Use the math library in this function.
"""
    test_abilities = [
        "heartquiet".encode("ascii").decode("ascii"),
        "harpoon".encode("ascii").decode("ascii"),
    ]
    for i in range(repetition):
        api_function = APIFunction(
            "specific_power",
            "/tests/set2/",
            {
                "ability": "str",
                "exponent": "float",
            },
            {
                "result": "float",
            },
            function_def,
            test_cases=[
                {
                    "input": {
                        "ability": test_abilities[0],
                        "exponent": 2,
                    },
                    "output": {
                        "result": 18.854225346913122,
                    },
                },
                {
                    "input": {
                        "ability": test_abilities[1],
                        "exponent": 0.2,
                    },
                    "output": {
                        "result": 1.2356224461821987,
                    },
                },
            ],
        )

        _, result_message = api_function.create_api_function()
        print("-----0------")
        print(f"i: {i}")
        print(api_function.build_attempts)
        print(result_message)
        build_result_list.append(api_function.build_attempts)

    print(build_result_list)


def test_basic_3():
    repetition = 1
    build_result_list = []
    function_def = """use a monte carlo simulation to approximate the area of an elipse. The inputs are the height and width of the elipse.
Use numpy's matrix functionality to speed up computation time.
"""
    for i in range(repetition):
        api_function = APIFunction(
            "elipse_area_calc",
            "/tests/elipse_calc/",
            {
                "height": "float",
                "width": "float",
            },
            {
                "result": "float",
            },
            function_def,
            test_cases=[
                {
                    "input": {
                        "height": 5.2,
                        "width": 1.36,
                    },
                    "output": {
                        "result": 5.55434,
                    },
                },
                {
                    "input": {
                        "height": 60.2,
                        "width": 60.2,
                    },
                    "output": {
                        "result": 2846.31436,
                    },
                },
                {
                    "input": {
                        "height": 0.02,
                        "width": 10,
                    },
                    "output": {
                        "result": 0.15708,
                    },
                },
            ],
        )

        _, result_message = api_function.create_api_function()
        print("-----0------")
        print(f"i: {i}")
        print(api_function.build_attempts)
        print(result_message)
        build_result_list.append(api_function.build_attempts)

    print(build_result_list)
