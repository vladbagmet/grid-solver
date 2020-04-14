from enum import Enum


class MessageType(Enum):
    ServiceHealth = "service is up and running"
    FieldCreated = "mine field was successfully created"
    CellDiscovered = "cell was discovered"
    NotFound = "url not found"
    ValidationError = "validation error"
    IncorrectInput = "incorrect input data"
    RequestError = "request error"
    NotAllowed = "method not allowed"
    ServerError = "server error"
