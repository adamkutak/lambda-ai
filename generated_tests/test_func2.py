from fastapi import FastAPI


# --xyz123--
app = FastAPI()

# --xyz123--


from fastapi import FastAPI

app = FastAPI()


@app.get("/tests/set2/")
async def test_func2(item_id: int, status: bool, bought: int):
    quantity = 100
    if status:
        quantity -= bought
    return {"item_id": item_id, "quantity": quantity}
