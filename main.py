import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from blenderApi import (
    get_all_devices,
    get_gpus_devices,
    get_cpus_devices,
    get_device_types,
    get_top_all_devices,
)

app = FastAPI()

origins = [
    "http://localhost:5173/",
    "localhost:5173/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/getall")
async def get_all():
    return get_all_devices()


@app.get("/getgpus")
async def get_gpus():
    return get_gpus_devices()


@app.get("/getcpus")
async def get_cpus():
    return get_cpus_devices()


@app.get("/getdevicetypes")
async def get_types():
    return get_device_types()


@app.get("/gettopdevices")
async def get_top():
    return get_top_all_devices()


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
