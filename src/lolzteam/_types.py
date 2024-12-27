from __future__ import annotations

from typing import Literal, Mapping, Any

JsonType = Mapping[str, Any]

UserType = Literal["me"]
UserOrderType = Literal[
    "natural",
    "follow_date",
    "follow_date_reverse"
]

PostOrderType = Literal[
    "natural",
    "natural_reverse",
    "post_likes",
    "post_likes_reverse"
]
ConversationOrderType = Literal["natural", "natural_reverse"]
ConversationDeleteType = Literal["delete", "delete_ignore"]

ReplyGroupType = Literal[0, 2, 21, 22, 23, 23, 60, 351]

ArbitrageTransferType = Literal["safe", "notsafe"]

ContestType = Literal["by_finish_date", "by_needed_members"]
ContestPrizeType = Literal["money", "upgrades"]
ContestPrizeDataUpgradeType = Literal[1, 6, 12, 14, 17, 19]
ContestLengthOptionType = Literal["minutes", "hours", "days"]

GeneralOrderType = Literal["natural", "list"]
