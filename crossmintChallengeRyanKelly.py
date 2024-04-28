from typing import Tuple as T, Dict, List as L

Z = int


def phase1():
    for row, column in phase1XCoords():
        createPolyanets(row, column)


def phase1XCoords():
    from itertools import chain

    downSlope = zip(range(2, 9), range(2, 9))
    upSlope = zip(range(8, 1, -1), range(2, 9))
    return list(set(chain(downSlope, upSlope)))


def createPolyanets(row: Z, column: Z) -> None:
    createEntity("polyanets", row, column)


def createSoloons(row: Z, column: Z, color: str) -> None:
    createEntity("soloons", row, column, trait={"color": validateSoloonsColor(color)})


def validateSoloonsColor(color: str) -> str:
    c = color.lower()
    if c != "blue" and c != "red" and c != "purple" and c != "white":
        raise Exception(f"Invalid soloons color '{c}'?")
    return c


def createComeths(row: Z, column: Z, direction: str) -> None:
    createEntity("comeths", row, column, trait={"direction": validateComethsDirection(direction)})


def validateComethsDirection(direction: str) -> str:
    d = direction.lower()
    if d != "up" and d != "down" and d != "right" and d != "left":
        raise Exception(f"Invalid comeths direction '{d}'?")
    return d


def createEntity(entityType: str, row: Z, column: Z, trait: Dict = {}) -> None:
    import requests

    url = createUrl(entityType)
    postData = {"candidateId": candidateId(), "row": row, "column": column}
    postData.update(trait)
    sleepFor429()
    r = requests.post(url, data=postData)
    print(f"{url=} {postData=} {r=}")


def sleepFor429():
    from time import sleep

    sleep(5)


def createUrl(entityType: str) -> str:
    entityType = validateEntityType(entityType)
    return baseUrl() + entityType


def validateEntityType(entityType: str) -> str:
    e = entityType.lower()
    if e != "polyanets" and e != "soloons" and e != "comeths":
        raise Exception(f"Invalid entity type '{e}'?")
    return e


def baseUrl() -> str:
    return "https://challenge.crossmint.io/api/"


def candidateId() -> str:
    return "1c4f30de-ed58-4112-903e-18f11ac6bd64"


def parseGoalMap() -> L[L[str]]:
    import json

    r = goalMap()
    goal = json.loads(r.text)["goal"]
    return goal


def goalMap() -> str:
    import requests

    url = goalMapUrl()
    r = requests.get(url)
    print(f"goalMap {url=} {r=}\n")
    print(r.text)
    return r


def goalMapUrl() -> str:
    return baseUrl() + "map/" + candidateId() + "/goal"


def phase2():
    goal = parseGoalMap()
    for row, rowEntities in enumerate(goal):
        for column, entity in enumerate(rowEntities):
            e = entity.lower()
            print(f"{row=} {column=} {e=}")
            if e == "space":
                continue
            elif e == "polyanet":
                createPolyanets(row, column)
            elif "cometh" in e:
                direction = parseGoalComethDirection(e)
                createComeths(row, column, direction)
            elif "soloon" in e:
                color = parseGoalSoloonColor(e)
                createSoloons(row, column, color)
            else:
                raise Exception(f"Unhandled goal entity '{e}'? {row=} {column=}")


def parseGoalComethDirection(e) -> str:
    direction, cometh = e.split("_")
    if cometh != "cometh":
        raise Exception(f"Something looks wrong with cometh goal str '{e}'? Doesn't have 'cometh' as second word?")
    if direction not in ["up", "down", "left", "right"]:
        raise Exception(f"Cometh goal str '{e}' doesn't have expected direction?")
    return direction


def parseGoalSoloonColor(e) -> str:
    color, soloon = e.split("_")
    if soloon != "soloon":
        raise Exception(f"Something looks wrong with soloon goal str '{e}'? Doesn't have 'soloon' as second word?")
    if color not in ["blue", "red", "purple", "white"]:
        raise Exception(f"Soloon goal str '{e}' doesn't have expected color?")
    return color


if __name__ == "__main__":
    # phase1()
    # goalMap()
    phase2()
