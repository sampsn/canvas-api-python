import os

from fastapi import FastAPI
from dotenv import load_dotenv
import requests

import models

app = FastAPI()

load_dotenv()

access_key = os.getenv("ACCESS_TOKEN")

base_url = "https://dixietech.instructure.com/api/v1"

headers: dict[str, str] = {"Authorization": f"Bearer {access_key}"}

response = requests.get(url=f"{base_url}/courses", headers=headers)
r_json = response.json()
# resp: dict = {
#     "id": r_json[0]["id"],
#     "name": r_json[0]["name"],
# }

resp = models.Course(id=r_json[0]["id"], name=r_json[0]["name"])

print(resp)


@app.get("/courses")
async def get_courses() -> list[models.Course]:
    resp = requests.get(url=f"{base_url}/courses")
    r_json = resp.json()

    return [models.Course(**course) for course in r_json]


@app.get("/discussions/{course_id}")
async def get_discussion(course_id: int) -> list:
    resp = requests.get(
        url=f"{base_url}/courses/{course_id}/discussion_topics", headers=headers
    )
    r_json = resp.json()

    return [models.Discussion(**discussion) for discussion in r_json]
