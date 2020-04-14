import trafaret as t

UUID4_LENGTH = 36


EXISTING_MINE_FIELD = t.Dict(
    {
        t.Key("x"): t.Int(),
        t.Key("y"): t.Int()
    }
)
NEW_MINE_FIELD = t.Dict(
    {
        t.Key("horizontalFieldSize"): t.Int(),
        t.Key("verticalFieldSize"): t.Int(),
        t.Key("mines"): t.Int(),
        t.Key("discoverableRadius"): t.Int(),
        t.Key("openedCells"): t.Int()
    }
)
MINE_FIELD_ID = t.String(min_length=UUID4_LENGTH, max_length=UUID4_LENGTH)
