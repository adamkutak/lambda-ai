from fastapi import FastAPI


# --xyz123--
app = FastAPI()

# --xyz123--


@app.get("/tests/set1/")
def test_func(item_id: int, status: bool, sold: int):
    if status:
        quantity = 2 * sold
    else:
        quantity = 5 * sold
    return {"item_id": item_id, "quantity": quantity}


@app.get("/tests/set2/")
def test_func_2(item_id: int, status: bool, bought: int):
    quantity = 100
    if status:
        quantity -= bought
    return {"item_id": item_id, "quantity": quantity}
