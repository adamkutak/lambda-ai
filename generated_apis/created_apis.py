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
