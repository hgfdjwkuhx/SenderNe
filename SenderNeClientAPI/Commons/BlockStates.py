



class BlockedStatu:

    Blocked = "blocked"
    JustAdd = "just_add"
    Unknown = "unknown"
    Running = "running"

    BlockedStates_List = [
        Blocked,
        JustAdd,
        Running,
        Unknown
    ]

    BLOCKED_STATUS_CHOICE = (
        (Blocked , "blocked"),
        (JustAdd, "just_add"),
        (Running, "running"),
        (Unknown, "unknown"),
    )

