from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Dict, Protocol

if TYPE_CHECKING:
    from niquests._typing import BodyType, AsyncBodyType

    from ._types import (
        JsonType,
        UserType,
        UserOrderType,
        PostOrderType,
        ConversationOrderType,
        ConversationDeleteType,
        ReplyGroupType,
        ArbitrageTransferType,
        ContestType,
        ContestPrizeType,
        ContestPrizeDataUpgradeType,
        ContestLengthOptionType,
        GeneralOrderType,
    ) 


def _one_or_none(value: bool | None) -> str | None:
    return "1" if value else None


def _true_or_none(value: bool | None) -> str | None:
    return "true" if value else None


# TODO: Исправить подсказку типов методов (pyright + ruff)
#       Например, Dict[str, Any] -> QueryParamType
class SyncClientProtocol(Protocol):
    def get(
        self,
        url: str,
        *,
        params: Dict[str, Any] | None = None,
    ) -> JsonType: ...

    def post(
        self,
        url: str,
        *,
        files: Dict[str, Any] | None = None,
        data: BodyType | AsyncBodyType | None = None,
        params: Dict[str, Any] | None = None,
    ) -> JsonType: ...

    def delete(
        self,
        url: str,
        *,
        params: Dict[str, Any] | None = None,
    ) -> JsonType: ...

    def put(
        self,
        url: str,
        *,
        data: BodyType | AsyncBodyType | None = None,
        params: Dict[str, Any] | None = None,
    ) -> JsonType: ...


class SyncCategoriesMixin(SyncClientProtocol):
    def get_categories(
        self,
        *,
        parent_category_id: int | None = None,
        parent_forum_id: int | None = None,
        order: GeneralOrderType | None = None,
    ) -> JsonType:
        """
        List of all categories in the system.

        Required scopes:
            read

        Args:
            parent_category_id (int):
                Id of parent category. If exists, filter categories
                that are direct children of that category.
            parent_forum_id (int):
                Id of parent forum. If exists, filter categories that
                are direct children of that forum.
            order (str):
                Ordering of forums. Must be one of the following:
                - "natural"
                - "list"

        Returns:
            JsonType
        """
        params = {
            "parent_category_id": parent_category_id,
            "parent_forum_id": parent_forum_id,
            "order": order,
        }
        return self.get("/categories", params=params)

    def get_category(self, category_id: int) -> JsonType:
        """
        Detail information of a category.

        Required scopes:
            read
        
        Args:
            category_id (int):
                Id of category.

        Returns:
            JsonType
        """
        return self.get(f"/categories/{category_id}")


class SyncForumsMixin(SyncClientProtocol):
    def get_forums(
        self,
        *,
        parent_category_id: int | None = None,
        parent_forum_id: int | None = None,
        order: GeneralOrderType | None = None,
    ) -> JsonType:
        """
        List of all forums in the system.

        Required scopes:
            read
        
        Args:
            parent_category_id (int):
                Id of parent category. If exists, filter forums that
                are direct children of that category.
            parent_forum_id (int):
                Id of parent forum. If exists, filter forums that are
                direct children of that forum.
            order (str):
                Ordering of forums. Must be one of the following:
                - "natural"
                - "list"

        Returns:
            JsonType
        """
        params = {
            "parent_category_id": parent_category_id,
            "parent_forum_id": parent_forum_id,
            "order": order,
        }
        return self.get("/forums", params=params)

    def get_forum(self, forum_id: int) -> JsonType:
        """
        Detail information of a forum.

        Required scopes:
            read

        Args:
            forum_id (int):
                Id of forum.

        Returns:
            JsonType
        """
        return self.get(f"/forums/{forum_id}")

    def get_followers(self, forum_id: int) -> JsonType:
        """
        List of a forumus followers. For privacy reason, only the
        current user will be included in the list (if the user follows
        the specified forum).

        Required scopes:
            read

        Args:
            forum_id (int):
                Id of forum.

        Returns:
            JsonType
        """
        return self.get(f"/forums/{forum_id}/followers")

    def get_followed_forums(self, *, total: bool | None = None) -> JsonType:
        """
        List of followed forums by current user.

        Required scopes:
            read

        Args:
            total (bool):
                If included in the request, only the forum count is
                returned as `forums_total`.

        Returns:
            JsonType
        """
        params = {"total": _true_or_none(total)}
        return self.get("/forums/followed", params=params)

    def follow_forum(
        self,
        forum_id: int,
        *,
        post: bool | None = None,
        alert: bool | None = None,
        email: bool | None = None,
        prefix_ids: List[int] | None = None,
        minimal_contest_amount: int | None = None,
    ) -> JsonType:
        """
        Follow a forum.

        Required scopes:
            post

        Args:
            forum_id (int):
                Id of forum.
            post (bool):
                Whether to receive notification for post `True` or just
                thread `False`.
            alert (bool):
                Whether to receive notification as alert.
            email (bool):
                Whether to receive notification as email.
            prefix_ids (list[int]):
                Prefix ids.
            minimal_contest_amount (int, >= 0):
                Minimal contest amount. (Only for 766 forumId)

        Returns:
            JsonType
        """
        data = {
            "post": int(post) if post else None,
            "alert": int(alert) if alert else None,
            "email": int(email) if email else None,
            "prefix_ids": prefix_ids,
            "minimal_contest_amount": minimal_contest_amount,
        }
        return self.post(f"/forums/{forum_id}/followers", data=data)

    def unfollow_forum(self, forum_id: int) -> JsonType:
        """
        Unfollow a forum.

        Required scopes:
            post

        Args:
            forum_id (int):
                Id of forum.

        Returns:
            JsonType
        """
        return self.post(f"/forums/{forum_id}/followers")


class SyncPagesMixin(SyncClientProtocol):
    def get_pages(
        self,
        *,
        parent_page_id: int | None = None,
        order: GeneralOrderType | None = None,
    ) -> JsonType:
        """
        List of all pages in the system.

        Required scopes:
            read

        Args:
            parent_page_id (int):
                Id of parent page. If exists, filter pages that are
                direct children of that page.
            order (str):
                Ordering of forums. Must be one of the following:
                - "natural"
                - "list"

        Returns:
            JsonType
        """
        params = {"parent_page_id": parent_page_id, "order": order}
        return self.get("/pages", params=params)

    def get_page(self, page_id: int) -> JsonType:
        """
        Detail information of a page.

        Required scopes:
            read

        Args:
            page_id (int):
                Id of page.

        Returns:
            JsonType
        """
        return self.get(f"/pages/{page_id}")


class SyncNavigationMixin(SyncClientProtocol):
    def get_navigation(self, *, parent: int | None = None) -> JsonType:
        """
        List of navigation elements within the system.

        Required scopes:
            read

        Args:
            parent (int):
                Id of parent element. If exists, filter elements that
                are direct children of that element.

        Returns:
            JsonType
        """
        params = {"parent": parent}
        return self.get("/navigation", params=params)


class SyncThreadsMixin(SyncClientProtocol):
    def get_threads(
        self,
        *,
        forum_id: int | None = None,
        creator_user_id: int | None = None,
        sticky: bool | None = None,
        thread_prefix_id: int | None = None,
        thread_tag_id: int | None = None,
        page: int | None = None,
        limit: int | None = None,
        order: GeneralOrderType | None = None,
    ) -> JsonType:
        """
        List of threads in a forum (with pagination).

        Required scopes:
            read

        Args:
            forum_id (int):
                Id of the containing forum. Can be skipped if
                `thread_ids` set.
            creator_user_id (int):
                Filter to get only threads created by the specified
                user.
            sticky (bool):
                Filter to get only sticky `sticky=True` or non-sticky
                `sticky=False` threads. By default, all threads will be
                included and sticky ones will be at the top of the
                result on the first page. In mixed mode, sticky threads
                are not counted towards threads_total and does not
                affect pagination.
            thread_prefix_id (int):
                Filter to get only threads with the specified prefix.
            thread_tag_id (int):
                Filter to get only threads with the specified tag.
            page (int):
                Page number of threads.
            limit (int):
                Number of threads in a page.
            order (str):
                Ordering of forums. Must be one of the following:
                - "natural"
                - "list"

        Returns:
            JsonType
        """
        params = {
            "forum_id": forum_id,
            "creator_user_id": creator_user_id,
            "sticky": int(sticky) if sticky else None,
            "thread_prefix_id": thread_prefix_id,
            "thread_tag_id": thread_tag_id,
            "page": page,
            "limit": limit,
            "order": order,
        }
        return self.get("/threads", params=params)

    def get_thread(self, thread_id: int) -> JsonType:
        """
        Detail information of a thread.

        Required scopes:
            read

        Args:
            thread_id (int):
                Id of thread.

        Returns:
            JsonType
        """
        return self.get(f"/threads/{thread_id}")

    def create_thread(
        self,
        forum_id: int,
        title: str,
        post_body: str,
        *,
        title_en: str | None = None,
        prefix_ids: List[int]| None = None,
        tags: List[str] | None = None,
        hide_contacts: bool | None = None,
        allow_ask_hidden_content: bool | None = None,
        reply_group: ReplyGroupType | None = None,
        comment_ignore_group: bool | None = None,
        dont_alert_followers: bool | None = None,
        watch_thread_state: bool | None = None,
        watch_thread: bool | None = None,
        watch_thread_email: bool | None = None,
    ) -> JsonType:
        """
        Create a new thread.

        Required scopes:
            post

        Args:
            forum_id (int):
                Id of the target forum.
            title (str):
                Thread title. Can be skipped if title_en set.
            post_body (str):
                Content of the new thread.
            title_en (str):
                Thread english title. Can be skipped if title set.
            prefix_ids (list[int]):
                Prefix ids.
            tags (list[str])
                Thread tags.
            hide_contacts (bool):
                Hide contacts.
            allow_ask_hidden_content (bool):
                Allow ask hidden content.
            reply_group (int, defaults to 2):
                Allow to reply only users with chosen or higher group.
                - 0: Only staff members and curators can reply in
                thread.
                - 2: Everyone can reply in thread.
                - 21: Local and higher can reply in thread.
                - 22: Resident or higher can reply in thread.
                - 23: Expert or higher can reply in thread.
                - 60: Guru and higher can reply in thread.
                - 351: Artificial Intelligence and higher can reply in
                thread.

            comment_ignore_group (bool):
                Allow commenting if user canut post in thread.
            dont_alert_followers (bool):
                Don't alert followers about thread creation.
            watch_thread_state (bool):
                Watch thread state.
            watch_thread (bool):
                Receive forum notifications of new posts in this thread.
                To receive notifications `watch_thread_state` must
                be "True"
            watch_thread_email (bool):
                Receive email notifications of new posts in this thread.
                To receive notifications `watch_thread_state`
                must be "1"

        Returns:
            JsonType
        """
        data = {"post_body": post_body}
        params = {
            "forum_id": forum_id,
            "title": title,
            "title_en": title_en,
            "prefix_id[]": prefix_ids,
            "tags": tags,
            "hide_contacts": hide_contacts,
            "allow_ask_hidden_content": allow_ask_hidden_content,
            "reply_group": reply_group,
            "comment_ignore_gruop": comment_ignore_group,
            "dont_alert_followers": dont_alert_followers,
            "watch_thread_state": _one_or_none(watch_thread_state),
            "watch_thread": _one_or_none(watch_thread),
            "watch_thread_email": _one_or_none(watch_thread_email),
        }
        return self.post("/threads", data=data, params=params)

    def create_contest(
        self,
        title: str,
        post_body: str,
        require_like_upgrade: int,
        require_total_like_count: int,
        contest_type: ContestType = "by_finish_date",
        prize_type: ContestPrizeType = "money",
        *,
        title_en: str | None = None,
        length_value: int | None = None,
        length_option: ContestLengthOptionType | None = None,
        needed_members: int | None = None,
        count_winners: int | None = None,
        prize_data_money: float | None = None,
        is_money_places: bool | None = None,
        prize_data_places: List[float] | None = None,
        prize_data_upgrade: ContestPrizeDataUpgradeType | None = None,
        secret_answer: str | None = None,
        tags: List[str] | None = None,
        reply_group: ReplyGroupType | None = None,
        comment_ignore_group: bool | None = None,
        dont_alert_followers: bool | None = None,
        hide_contacts: bool | None = None,
        allow_ask_hidden_content: bool | None = None,
        watch_thread_state: bool | None = None,
        watch_thread: bool | None = None,
        watch_thread_email: bool | None = None,
    ) -> JsonType:
        """
        Create a new contest.

        Required scopes:
            post

        Args:
            title (str):
                Thread title. Can be skipped if title_en set.
            post_body (str):
                Content of the new contest.
            require_like_count (int):
                Sympathies for this week.
            require_total_like_count (int):
                Symapthies for all time.
            contest_type (str, defaults to `by_finih_date`):
                Contest type.
            prize_type (str):
                Prize type.
            title_en (str):
                Thread english title. Can be skipped if title set.
            length_value (int, >= 1):
                Giveaway duration value. The maximum duration is 3 days.
                Required if `contest_type` is `by_finish_date`.
            length_option (str):
                Giveaway duration type. The maximum duration is 3 days.
                Required if `contest_type` is `by_finish_date`.
            needed_members (int):
                Max member count. Required if `contest_type`
                is `by_needed_members`.
            count_winners (int, 1 to 100):
                Winner count (prize count). Optional if
                `prize_type` is money.
            prize_data_money (float):
                How much money will each winner receive.
                Optional if `prize_type` is money.
            is_money_places (bool):
                Enable the distribution of money prizes by places.
                Optional if `prize_type` is money.
            prize_data_places (list[float]):
                How much money will receive each place.
                Required if `is_money_places` is 1.
            prize_data_upgrade (int):
                Which upgrade will each winner receive. 
                Required if `prize_type` is upgrades.
                - 1: Supreme - 3 months.
                - 6: Legend - 12 months.
                - 12: AntiPublic.One Plus subscription - 1 month.
                - 14: Uniq - lifetime.
                - 17: 18+ Photo leaks - 6 months.
                - 19: Auto giveaway participation - 1 month.
            secret_answer (str):
                Secret answer of your account.
            tags (list[str]):
                Thread tags.
            reply_group (int, defaults to 2):
                Allow to reply only users with chosen or higher group.
                - 0: Only staff members and curators can reply
                in thread.
                - 2: Everyone can reply in thread.
                - 21: Local and higher can reply in thread.
                - 22: Resident or higher can reply in thread.
                - 23: Expert or higher can reply in thread.
                - 60: Guru and higher can reply in thread.
                - 351: Artificial Intelligence and higher can reply
                in thread.
            comment_ignore_group (bool):
                Allow commenting if user can't post in thread.
            dont_alert_followers (bool):
                Don't alert followers about thread creation.
            hide_contacts (bool):
                Hide contacts.
            allow_ask_hidden_content (bool):
                Allow ask hidden content.
            watch_thread_state (bool):
                Watch thread state.
            watch_thread (bool):
                Receive forum notifications of new posts in this thread.
                To receive notifications `watch_thread_state`
                must be "True".
            watch_thread_email (bool):
                Receive email notifications of new posts in this thread.
                To receive notifications `watch_thread_state`
                must be "True".

        Returns:
            JsonType
        """
        data = {"post_body": post_body}
        params = {
            "title": title,
            "contest_type": contest_type,
            "prize_type": prize_type,
            "require_like_upgrade": require_like_upgrade,
            "require_total_like_count": require_total_like_count,
            "title_en": title_en,
            "length_value": length_value,
            "length_option": length_option,
            "needed_members": needed_members,
            "count_winners": count_winners,
            "prize_data_money": prize_data_money,
            "is_money_places": _one_or_none(is_money_places),
            "prize_data_places[]": prize_data_places,
            "prize_data_upgrade": prize_data_upgrade,
            "secret_answer": secret_answer,
            "tags": tags,
            "reply_group": reply_group,
            "comment_ignore_group": comment_ignore_group,
            "dont_alert_followers": dont_alert_followers,
            "hide_contacts": hide_contacts,
            "allow_ask_hidden_content": allow_ask_hidden_content,
            "watch_thread_state": _one_or_none(watch_thread_state),
            "watch_thread": _one_or_none(watch_thread),
            "watch_thread_email": _one_or_none(watch_thread_email),
        }
        return self.post("/contest", data=data, params=params)

    def create_arbitrage(
        self,
        as_responder: str,
        as_amount: float,
        post_body: str,
        as_is_market_deal: bool = True,
        transfer_type: ArbitrageTransferType = "safe",
        *,
        as_market_item_id: int | None = None,
        as_data: str | None = None,
        currency: str | None = None,
        as_funds_receipt: str | None = None,
        as_tg_login_screenshot: str | None = None,
        tags: List[str] | None = None,
        hide_contacts: bool | None = None,
        allow_ask_hidden_content: bool | None = None,
        reply_group: ReplyGroupType | None = None,
        comment_ignore_group: bool | None = None,
        dont_alert_followers: bool | None = None,
        watch_thread_state: bool | None = None,
        watch_thread: bool | None = None,
        watch_thread_email: bool | None = None,
    ) -> JsonType:
        """
        Create a Arbitrage.

        Required scopes:
            post

        Args:
            as_responder (str):
                To whom the complaint is filed. Specify a nickname or
                a link to the profile.
            as_amount (int):
                Indicate the amount by which the responder deceived you.
            post_body (str):
                You should describe what's happened.
                - describe the situation in a nutshell. If you wish,
                you can describe the situation in more detail using the
                "Spoiler" function.
                - attach screenshots of correspondence. You must upload
                to the site Imgur - for convenience, use Ctrl + V when
                uploading screenshots to the album.
                - other evidence;
                - notify the respondent about the complaint you created,
                familiarize him with hidden content
                Describe the situation in as much detail as possible.
            as_is_market_deal (bool):
                Did you buy account on the market?
            transfer_type (str):
                The transaction took place through a guarantor or there
                was a transfer to the market with a hold?
                Required if `as_is_market_deal` is 0.
            as_market_item_id (int):
                Item id.
                Required if `as_is_market_deal` is 1.
            as_data (str):
                Contacts and wallets of the responder.
                Specify the known data about the responder (Skype,
                Vkontakte, Qiwi, WebMoney, etc.), if any.
                Optional if `as_is_market_deal` is 0.
            currency (str):
                Currency of Arbitrage.
            as_funds_receipt (str):
                Funds transfer recipient.
                Upload a receipt for the transfer of funds, use the
                "View receipt" button in your wallet. Must be uploaded
                to Imgur. Write "no" if you have not paid.
                Required if `as_is_market_deal` is 0.
            as_tg_login_screenshot (str):
                Screenshot showing the respondent's Telegram login.
                If the correspondence was conducted in Telegram, upload
                a screenshot that will display the respondent's Telegram
                login against the background of your dialogue.
                The screenshot must be uploaded to Imgur. If the
                correspondence was conducted elsewhere, write "no".
            tags (list[str]):
                Thread tags.
            hide_contacts (bool):
                Hide contacts.
            allow_ask_hidden_content (bool):
                Allow ask hidden content.
            reply_group (int, defaults to 2):
                Allow to reply only users with chosen or higher group.
                - 0: Only staff members and curators can reply
                in thread.
                - 2: Everyone can reply in thread.
                - 21: Local and higher can reply in thread.
                - 22: Resident or higher can reply in thread.
                - 23: Expert or higher can reply in thread.
                - 60: Guru and higher can reply in thread.
                - 351: Artificial Intelligence and higher can reply
                in thread.
            comment_ignore_group (bool):
                Allow commenting if user can't post in thread.
            dont_alert_followers (bool):
                Don't alert followers about thread creation.
            watch_thread_state (bool):
                Watch thread state.
            watch_thread (bool):
                Receive forum notifications of new posts in this thread.
                To receive notifications watch_thread_state
                must be "True"
            watch_thread_email (bool):
                Receive email notifications of new posts in this thread.
                To receive notifications watch_thread_state
                must be "True"

        Returns:
            JsonType
        """
        data = {"post_body": post_body}
        params = {
            "as_responder": as_responder,
            "as_is_market_deal": as_is_market_deal,
            "as_amount": as_amount,
            "transfer_type": transfer_type,
            "as_market_item_id": as_market_item_id,
            "as_data": as_data,
            "currency": currency,
            "as_funds_receipt": as_funds_receipt,
            "as_tg_login_screenshot": as_tg_login_screenshot,
            "tags": tags,
            "reply_group": reply_group,
            "comment_ignore_group": comment_ignore_group,
            "dont_alert_followers": dont_alert_followers,
            "hide_contacts": hide_contacts,
            "allow_ask_hidden_content": allow_ask_hidden_content,
            "watch_thread_state": _one_or_none(watch_thread_state),
            "watch_thread": _one_or_none(watch_thread),
            "watch_thread_email": _one_or_none(watch_thread_email),
        }
        return self.post("/claims", data=data, params=params)

    def edit_thread(
        self,
        thread_id: int,
        *,
        title: str | None = None,
        title_en: str | None = None,
        prefix_ids: List[str] | None = None,
        tags: List[str] | None = None,
        hide_contacts: bool | None = None,
        allow_ask_hidden_content: bool | None = None,
        reply_group: ReplyGroupType | None = None,
        comment_ignore_group: bool | None = None,
    ) -> JsonType:
        """
        Edit a thread.

        Required scopes:
            post

        Args:
            thread_id (int):
                Id of thread.
            title (str):
                Thread title.
            title_en (str):
                Thread title english.
            prefix_ids (list[int]):
                Prefix ids. Set "0" to remove all thread prefixes.
            tags (list[str]):
                Thread tags.
            discussion_open (bool):
                Discussion state.
            hide_contacts (bool):
                Hide contacts.
            allow_ask_hidden_content (bool):
                Allow ask hidden content.
            reply_group (int):
                Allow to reply only users with chosen or higher group.
                - 0: Only staff members and curators can reply in
                thread.
                - 2: Everyone can reply in thread.
                - 21: Local and higher can reply in thread.
                - 22: Resident or higher can reply in thread.
                - 23: Expert or higher can reply in thread.
                - 60: Guru and higher can reply in thread.
                - 351: Artificial Intelligence and higher can reply in
                thread.
            comment_ignore_group (bool):
                Allow commenting if user can't post in thread.

        Returns:
            JsonType
        """
        params = {
            "title": title,
            "title_en": title_en,
            "prefix_id[]": prefix_ids,
            "tags": tags,
            "hide_contacts": hide_contacts,
            "allow_ask_hidden_content": allow_ask_hidden_content,
            "reply_group": reply_group,
            "comment_ignore_group": comment_ignore_group,
        }
        return self.put(f"/threads/{thread_id}", params=params)

    def delete_thread(
        self,
        thread_id: int,
        *,
        reason: str | None = None,
    ) -> JsonType:
        """
        Delete a thread.

        Required scopes:
            post

        Args:
            thread_id (int):
                Id of thread.
            reason (str):
                Reason of the thread removal.

        Returns:
            JsonType
        """
        params = {"reason": reason}
        return self.delete(f"/threads/{thread_id}", params=params)

    def bump_thread(self, thread_id: int) -> JsonType:
        """
        Bump a thread.

        Required scopes:
            post

        Args:
            thread_id (int):
                Id of thread.

        Returns:
            JsonType
        """
        return self.post(f"/threads/{thread_id}/bump")

    def move_thread(
        self,
        thread_id: int,
        node_id: str,
        *,
        title: str | None = None,
        title_en: str | None = None,
        prefix_ids: List[str] | None = None,
        apply_thread_prefix: bool | None = None,
        send_alert: bool | None = None,
    ) -> JsonType:
        """
        Move a thread to another forum.

        Required scopes:
            post
        
        Args:
            thread_id (int):
                Id of thread.
            node_id (str):
                Forum id.
            title (str):
                Thread title.
            title_en (str):
                Thread title english.
            prefix_ids (list[int]): of integers
                Prefix ids. Set "0" to remove all thread prefixes.
            apply_thread_prefix (int):
                Apply thread prefix.
            send_alert (bool):
                Send a notification to users who are followed to target
                node.

        Returns:
            JsonType
        """
        params = {
            "node_id": node_id,
            "title": title,
            "title_en": title_en,
            "prefix_id[]": prefix_ids,
            "apply_thread_prefix": _one_or_none(apply_thread_prefix),
            "send_alert": send_alert,
        }
        return self.post(f"/threads/{thread_id}/move", params=params)

    def get_thread_followers(self, thread_id: int) -> JsonType:
        """
        List of a thread's followers. For privacy reason, only the
        current user will be included in the list.

        Required scopes:
            read

        Args:
            thread_id (int):
                Id of thread.

        Returns:
            JsonType
        """
        return self.get(f"/threads/{thread_id}/followers")

    def get_followed_threads(self, *, total: bool | None = None) -> JsonType:
        """
        List of followed threads by current user.

        Required scopes:
            read

        Args:
            total (bool):
                If included in the request, only the thread count is
                returned as `threads_total`.

        Returns:
            JsonType
        """
        params = {"total": _true_or_none(total)}
        return self.get("/threads/followed", params=params)

    def follow_thread(
        self,
        thread_id: int,
        *,
        email: bool | None = None,
    ) -> JsonType:
        """
        Follow a thread.

        Required scopes:
            post

        Args:
            threadId (int):
                Id of thread.
            email (int):
                Whether to receive notification as email.

        Returns:
            JsonType
        """
        params = {"email": _one_or_none(email)}
        return self.post(f"/threads/{thread_id}/followers", params=params)

    def unfollow_thread(self, thread_id: int) -> JsonType:
        """
        Unfollow a thread.

        Required scopes:
            post

        Args:
            thread_id (int):
                Id of thread.

        Returns:
            JsonType
        """
        return self.delete(f"/threads/{thread_id}/followers")

    def get_navigation_elements(self, thread_id: int) -> JsonType:
        """
        List of navigation elements to reach the specified thread.

        Required scopes:
            read

        Args:
            thread_id (int):
                Id of thread.

        Returns:
            JsonType
        """
        return self.get(f"/threads/{thread_id}/navigation")

    def get_poll(self, thread_id: int) -> JsonType:
        """
        Detail information of a poll.

        Required scopes:
            read

        Args:
            thread_id (int):
                Id of thread.

        Returns:
            JsonType
        """
        return self.get(f"/threads/{thread_id}/poll")

    def vote_poll(
        self,
        thread_id: int,
        *,
        response_id: int | None = None,
        response_ids: List[int] | None = None,
    ) -> JsonType:
        """
        Vote on a thread poll.
        
        Required scopes:
            post

        Args:
            thread_id (int):
                Id of thread.
            response_id (int):
                The id of the response to vote for. Can be skipped if
                response_ids set.
            response_ids (list[int]):
                An array of ids of responses (if the poll allows
                multiple choices).

        Returns:
            JsonType
        """
        params = {
            "response_id": response_id,
            "response_ids[]": response_ids
        }
        return self.post(f"/threads/{thread_id}/poll/votes", params=params)

    def get_unread_threads(
        self,
        *,
        limit: int | None = None,
        forum_id: int | None = None,
        data_limit: int | None = None,
    ) -> JsonType:
        """
        List of unread threads (must be logged in).

        Required scopes:
            read

        Args:
            limit (int):
                Maximum number of result threads. The limit may get
                decreased if the value is too large (depending on the
                system configuration).
            forum_id (int):
                Id of the container forum to search for threads. Child
                forums of the specified forum will be included in the
                search.
            data_limit (int, defaults to 20):
                Number of thread data to be returned.

        Returns:
            JsonType
        """
        params = {
            "limit": limit,
            "forum_id": forum_id,
            "data_limit": data_limit,
        }
        return self.get("/threads/new", params=params)

    def get_recent_threads(
        self,
        *,
        days: int | None = None,
        limit: int | None = None,
        forum_id: int | None = None,
        data_limit: int | None = None,
    ) -> JsonType:
        """
        List of recent threads.

        Required scopes:
            read

        Args:
            days (int):
                Maximum number of days to search for threads.
            limit (int):
                Maximum number of result threads. The limit may get
                decreased if the value is too large.
            forum_id (int):
                Id of the container forum to search for threads. Child
                forums of the specified forum will be included in the search.
            data_limit (int, defaults to 20):
                Number of thread data to be returned.

        Returns:
            JsonType
        """
        params = {
            "days": days,
            "limit": limit,
            "forum_id": forum_id,
            "data_limit": data_limit,
        }
        return self.get("/threads/recent", params=params)


class SyncPostsMixin(SyncClientProtocol):
    def get_post_comments(
        self,
        post_id: int, 
        *,
        before: int | None = None,
        before_comment: int | None = None,
    ) -> JsonType:
        """
        List of post comments in a thread.

        Required scopes:
            read

        Args:
            post_id (int):
                Id of post.
            before (int):
                The time in milliseconds (e.g. 1652177794083) before
                last comment date.
            before_comment (int):
                Comment id to get older comments.

        Returns:
            JsonType
        """
        params = {"before": before, "before_comment": before_comment}
        return self.get(f"/posts/{post_id}/comments", params=params)

    def create_post_comment(self, post_id: int, comment_body: str) -> JsonType:
        """
        Create a new post comment.

        Required scopes:
            post

        Args:
            post_id (int):
                Id of post.
            comment_body (str):
                Content of the new post comment.

        Returns:
            JsonType
        """
        data = {"comment_body": comment_body}
        return self.post(f"/posts/{post_id}/comments", data=data)

    def get_posts(
        self,
        thread_id: int,
        *,
        page_of_post_id: int | None = None,
        page: int | None = None,
        limit: int | None = None,
        order: PostOrderType| None = None,
    ) -> JsonType:
        """
        List of posts in a thread (with pagination).

        Required scopes:
            read

        Args:
            thread_id (int):
                Id of the containing thread.
            page_of_post_id (int):
                Id of a post, posts that are in the same page with the
                specified post will be returned. thread_id may be
                skipped.
            page (int):
                Page number of posts.
            limit (int):
                Number of posts in a page. Default value depends on
                the system configuration.
            order (str):
                Ordering of posts. Must be one of the following:
                - "natural"
                - "natural_reverse"
                - "post_likes"
                - "post_likes_reverse"

        Returns:
            JsonType
        """
        params = {
            "thread_id": thread_id,
            "page_of_post_id": page_of_post_id,
            "page": page,
            "limit": limit,
            "order": order,
        }
        return self.get("/posts", params=params)

    def get_post(self, post_id: int) -> JsonType:
        """
        Detail information of a post.

        Required scopes:
            read

        Args:
            post_id (int):
                Id of post.

        Returns:
            JsonType
        """
        return self.get(f"/posts/{post_id}")

    def create_post(
        self,
        thread_id: int,
        post_body: int,
        *,
        quote_post_id: str | None = None,
    ) -> JsonType:
        """
        Create a new post.

        Required scopes:
            post

        Args:
            thread_id (int):
                Id of the target thread.
            post_body (str):
                Content of the new post.
            quote_post_id (int):
                Id of the quote post. It's possible to skip thread_id
                if this parameter is provided. An extra check is
                performed if both parameters exist and does not match.

        Returns:
            JsonType
        """
        data = {"post_body": post_body}
        params = {
            "thread_id": thread_id,
            "quote_post_id": quote_post_id
        }
        return self.post("/posts", data=data, params=params)

    def edit_post(self, post_id: int, post_body: str) -> JsonType:
        """
        Edit a post.

        Required scopes:
            post

        Args:
            post_id (int):
                Id of post.
            post_body (str):
                Content of the post.

        Returns:
            JsonType
        """
        data = {"post_body": post_body}
        return self.put(f"/posts/{post_id}", data=data)

    def delete_post(
        self,
        post_id: int,
        *,
        reason: str | None = None,
    ) -> JsonType:
        """
        Delete a post.

        Required scopes:
            post

        Args:
            post_id (int):
                Id of post.
            reason (str):
                Reason of the post removal.

        Returns:
            JsonType
        """
        params = {"reason": reason}
        return self.delete(f"/posts/{post_id}", params=params)

    def get_post_likes(
        self,
        post_id: int,
        *,
        page: int | None = None,
        limit: int | None = None,
    ) -> JsonType:
        """
        List of users who liked a post.

        Required scopes:
            read

        Args:
            post_id (int):
                Id of post.
            page (int):
                Page number of users.
            limit (int):
                Number of users in a page. Default value depends on the
                system configuration.

        Returns:
            JsonType
        """
        params = {"page": page, "limit": limit}
        return self.get(f"/posts/{post_id}/likes", params=params)

    def like_post(self, post_id: int) -> JsonType:
        """
        Like a post.

        Required scopes:
            post

        Args:
            post_id (int):
                Id of post.

        Returns:
            JsonType
        """
        return self.post(f"/posts/{post_id}/likes")

    def unlike_post(self, post_id: int) -> JsonType:
        """
        Unlike a post.

        Required scopes:
            post

        Args:
            post_id (int):
                Id of post.

        Returns:
            JsonType
        """
        return self.delete(f"/posts/{post_id}/likes")

    def report_post(self, post_id: int, message: str) -> JsonType:
        """
        Report a post.

        Required scopes:
            post

        Args:
            post_id (int):
                Id of post.
            message (str):
                Reason of the report.

        Returns:
            JsonType
        """
        params = {"message": message}
        return self.post(f"/posts/{post_id}/report", params=params)


class SyncUsersMixin(SyncClientProtocol):
    def upload_avatar(
        self,
        user_id: int | UserType,
        filepath: str
    ) -> JsonType:
        """
        Upload avatar for a user.

        Required scopes:
            post

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.
            filepath (str):
                The filepath of the avatar image.

        Returns:
            JsonType
        """
        files = {"avatar": (open(filepath, "rb"))}
        return self.post(f"/users/{user_id}/avatar", files=files)

    def crop_avatar(
        self,
        user_id: int | UserType,
        crop: int,
        *,
        x: int | None = None,
        y: int | None = None,
    ) -> JsonType:
        """
        Crop avatar for a user.

        Required scopes:
            post

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.
            crop (int, >= 16):
                Selection size.
            x (int, defaults to 0):
                The starting point of the selection by width.
            y (int, defaults to 0):
                The starting point of the selection by height.

        Returns:
            JsonType
        """
        params = {"x": x, "y": y, "crop": crop}
        return self.post(f"/users/{user_id}/avatar/crop", params=params)

    def delete_avatar(self, user_id: int | UserType) -> JsonType:
        """
        Delete avatar for a user.

        Required scopes:
            post

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.

        Returns:
            JsonType
        """
        return self.delete(f"/users/{user_id}/avatar")

    def upload_background(
        self,
        user_id: int | UserType,
        filepath: str,
        crop: int,
        *,
        x: int | None = None,
        y: int | None = None,
    ) -> JsonType:
        """
        Upload background for a user.

        Required scopes:
            post

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.
            filepath (str):
                The filepath of the background image.
            crop (int, >= 100):
                Selection size.
            x (int, defaults to 0):
                The starting point of the selection by width.
            y (int, defaults to 0):
                The starting point of the selection by height.

        Returns:
            JsonType
        """
        files = {"background": (open(filepath, "rb"))}
        params = {"x": x, "y": y, "crop": crop}
        return self.post(
            f"/users/{user_id}/background", files=files, params=params
        )

    def delete_background(self, user_id: int | UserType) -> JsonType:
        """
        Delete background for a user.

        Required scopes:
            post

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.

        Returns:
            JsonType
        """
        return self.delete(f"/users/{user_id}/background")

    def crop_background(
        self,
        user_id: int | UserType,
        crop: int,
        *,
        x: int | None = None,
        y: int | None = None,
    ) -> JsonType:
        """
        Crop background for a user.

        Required scopes:
            post

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.
            crop (int, >= 100):
                Selection size.
            x (int, defaults to 0):
                The starting point of the selection by width.
            y (int, defaults to 0):
                The starting point of the selection by height.
            
        """
        params = {"x": x, "y": y, "crop": crop}
        return self.post(f"/users/{user_id}/background/crop", params=params)

    def get_users(
        self,
        *,
        page: int | None = None,
        limit: int | None = None,
    ) -> JsonType:
        """
        List of users (with pagination).

        Required scopes:
            read

        Args:
            page (int):
                Page number of users.
            limit (int):
                Number of users in a page.

        Returns:
            JsonType
        """
        params = {"page": page, "limit": limit}
        return self.get("/users", params=params)

    def get_user_fields(self) -> JsonType:
        """
        List of user fields.

        Required scopes:
            read

        Returns:
            JsonType
        """
        return self.get("/users/fields")

    def find_users(
        self,
        *,
        username: str | None = None,
        user_email: str | None = None,
        custom_fields: str | None = None,
        location: str | None = None,
        occupation: str | None = None,
        homepage: str | None = None,
        _4: str | None = None,
        lztInnovationLink: str | None = None,
        lztInnovation20Link: str | None = None,
        lztInnovation30Link: str | None = None,
        scamURL: str | None = None,
        maecenasValue: str | None = None,
        telegram: str | None = None,
        vk: str | None = None,
        steam: str | None = None,
        jabber: str | None = None,
        lztDeposit: str | None = None,
        ban_reason: str | None = None,
    ) -> JsonType:
        """
        List of users filtered by username, email or custom fields.

        Required scopes:
            read

        Args:
            username (str):
                Username to filter. Usernames start with the query will
                be returned.
            user_email (str):
                Email to filter. Requires admincp scope.
            custom_fields (str):
                Custom fields to filter.
                Example: `custom_fields[telegram]=telegramLogin`.
            location (str):
                User location field.
            occupation (str):
                User occupation field.
            homepage (str):
                User homepage field.
            _4 (str):
                User strerests field.
            lztInnovationLink (str):
                User thread link for "innovator" trophy.
            lztInnovation20Link (str):
                User thread link for "innovator 2.0" trophy.
            lztInnovation30Link (str):
                User thread link for "innovator 3.0" trophy.
            scamURL (str):
                User scam url field.
            maecenasValue (str):
                User maecenas value field.
            telegram (str):
                User telegram field.
            vk (str):
                User vk field.
            steam (str):
                User steam field.
            jabber (str):
                User jabber field.
            lztDeposit (str):
                User lztDeposit field.
            ban_reason (str):
                User ban_reason field.

        Returns:
            JsonType
        """
        params = {
            "username": username,
            "user_email": user_email,
            "custom_fields": custom_fields,
            "custom_fields[location]": location,
            "custom_fields[occupation]": occupation,
            "custom_fields[homepage]": homepage,
            "custom_fields[]]_4": _4,
            "custom_fields[lztInnovationLink]": lztInnovationLink,
            "custom_fields[lztInnovation20Link]": lztInnovation20Link,
            "custom_fields[lztInnovation30Link]": lztInnovation30Link,
            "custom_fields[scamURL]": scamURL,
            "custom_fields[maecenasValue]": maecenasValue,
            "custom_fields[telegram]": telegram,
            "custom_fields[vk]": vk,
            "custom_fields[steam]": steam,
            "custom_fields[jabber]": jabber,
            "custom_fields[lztDeposit]": lztDeposit,
            "custom_fields[ban_reason]": ban_reason,
        }
        return self.get("/users/find", params=params)

    def get_user(self, user_id: int | UserType) -> JsonType:
        """
        Detail information of a user.

        Required scopes:
            read
            basic

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.

        Returns:
            JsonType
        """
        return self.get(f"/users/{user_id}")

    def edit_user(
        self,
        user_id,
        *,
        user_title: str | None = None,
        primary_group_id: int | None = None,
        secondary_group_ids: List[int] | None = None,
        display_group_id: int | None = None,
        user_dob_day: int | None = None,
        user_dob_month: int | None = None,
        user_dob_year: int | None = None,
        location: str | None = None,
        occupation: str | None = None,
        homepage: str | None = None,
        _4: str | None = None,
        lztInnovationLink: str | None = None,
        lztInnovation20Link: str | None = None,
        lztInnovation30Link: str | None = None,
        telegram: str | None = None,
        vk: str | None = None,
        discord: str | None = None,
        steam: str | None = None,
        jabber: str | None = None,
    ) -> JsonType:
        """
        Edit a user.

        Required scopes:
            post

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.
            user_title (str):
                New custom title of the user.
            primary_group_id (int):
                Id of new primary group. (Require admincp scope)
            secondary_group_ids (list[int]): of integers
                Array of ids of new secondary groups. (Require admincp
                scope)
            display_group_id (int):
                Id of group you want to display.
            user_dob_day (int):
                Your date of birth (day).
            user_dob_month (int):
                Your date of birth (month).
            user_dob_year (int):
                Your date of birth (year).
            location (str):
                Your location.
            occupation (str):
                Your occupation.
            homepage (str):
                Your homepage.
            _4 (str):
                Your strerests.
            lztInnovationLink (str):
                Thread link for "innovator" trophy.
            lztInnovation20Link (str):
                Thread link for "innovator 2.0" trophy.
            lztInnovation30Link (str):
                Thread link for "innovator 3.0" trophy.
            telegram (str):
                Your telegram.
            vk (str):
                Your vk.
            discord (str):
                Your discord.
            steam (str):
                Your steam.
            jabber (str):
                Your jabber.

        Returns:
            JsonType
        """
        params = {
            "user_title": user_title,
            "primary_group_id": primary_group_id,
            "secondary_group_ids": secondary_group_ids,
            "display_group_id": display_group_id,
            "user_dob_day": user_dob_day,
            "user_dob_month": user_dob_month,
            "user_dob_year": user_dob_year,
            "fields[location]": location,
            "fields[occupation]": occupation,
            "fields[homepage]": homepage,
            "fields[_4]": _4,
            "fields[lztInnovationLink]": lztInnovationLink,
            "fields[lztInnovation20Link]": lztInnovation20Link,
            "fields[lztInnovation30Link]": lztInnovation30Link,
            "fields[telegram]": telegram,
            "fields[vk]": vk,
            "fields[discord]": discord,
            "fields[steam]": steam,
            "fields[jabber]": jabber,
        }
        return self.put(f"/users/{user_id}", params=params)

    def get_user_followers(
        self,
        user_id: int | UserType,
        *,
        order: UserOrderType | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> JsonType:
        """
        List of a user's followers.

        Required scopes:
            read

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.
            order (str):
                Ordering of followers.
            page (int):
                Page number of followers.
            limit (int):
                Number of followers in a page.

        Returns:
            JsonType
        """
        params = {"order": order, "page": page, "limit": limit}
        return self.get(f"/users/{user_id}/followers", params=params)

    def get_followed_users_by_user(
        self,
        user_id: int | UserType,
        *,
        order: UserOrderType | None = None,
        page: int | None = None,
        limit: int | None = None,
    ):
        """
        List of users whom are followed by a user.

        Required scopes:
            read

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.
            order (str):
                Ordering of followers.
            page (int):
                Page number of followers.
            limit (int):
                Number of followers in a page.

        Returns:
            JsonType
        """
        params = {"order": order, "page": page, "limit": limit}
        return self.get(f"/users/{user_id}/followings", params=params)

    def follow_user(self, user_id: int | UserType) -> JsonType:
        """
        Follow a user.

        Required scopes:
            post

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.

        Returns:
            JsonType
        """
        return self.post(f"/users/{user_id}/followers")

    def unfollow_user(self, user_id: int | UserType) -> JsonType:
        """
        Unfollow a user.

        Required scopes:
            post

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.

        Returns:
            JsonType
        """
        return self.delete(f"/users/{user_id}/followers")

    def get_ignored_users(self, *, total: bool | None = None) -> JsonType:
        """
        List of ignored users of current user.

        Required scopes:
            read
            
        Args:
            total (bool):
                If included in the request, only the user count is
                returned as `users_total`.

        Returns:
            JsonType
        """
        params = {"total": _true_or_none(total)}
        return self.get("/users/ignored", params=params)

    def ignore_user(self, user_id: int | UserType) -> JsonType:
        """
        Ignore a user.

        Required scopes:
            post

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.

        Returns:
            JsonType
        """
        return self.post(f"/users/{user_id}/ignore")

    def unignore_user(self, user_id: int | UserType) -> JsonType:
        """
        Stop ignoring a user.

        Required scopes:
            post
           
        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.

        Returns:
            JsonType
        """
        return self.delete(f"/users/{user_id}/ignore")

    def get_contests(
        self,
        user_id: int | UserType,
        *,
        page: int | None = None,
        limit: int | None = None,
    ) -> JsonType:
        """
        List of contents created by user (with pagination).

        Required scopes:
            read

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.
            page (int):
                Page number of followers.
            limit (int):
                Number of followers in a page.

        Returns:
            JsonType
        """
        params = {"page": page, "limit": limit}
        return self.get(f"/users/{user_id}/timeline", params=params)


class SyncProfilePostsMixin(SyncClientProtocol):
    def get_profile_post_comments(
        self,
        profile_post_id: int,
        *,
        before: int | None = None,
        limit: int | None = None,
    ) -> JsonType:
        """
        List of comments of a profile post.

        Required scopes:
            read

        Args:
            profile_post_id (int):
                Id of profile post.
            before (int):
                Date to get older comments. Please note that this entry
                point does not support the page parameter but it still
                does support limit.
            limit (int):
                Number of profile posts in a page.

        Returns:
            JsonType
        """
        params = {"before": before, "limit": limit}
        return self.get(
            f"/profile-posts/{profile_post_id}/comments", params=params
        )

    def get_profile_post_comment(
        self,
        profile_post_id: int,
        comment_id: int,
    ) -> JsonType:
        """
        Detail information of a profile post comment.

        Required scopes:
            read

        Args:
            profile_post_id (int):
                Id of profile post.
            comment_id (int):
                Id of profile post comment.

        Returns:
            JsonType
        """
        return self.get(
            f"/profile-posts/{profile_post_id}/comments/{comment_id}"
        )

    def create_profile_post_comment(
        self,
        profile_post_id: int,
        comment_body: str,
    ) -> JsonType:
        """
        Create a new profile post comment.

        Required scopes:
            post

        Args:
            profile_post_id (int):
                Id of profile post.
            comment_body (str):
                Content of the new profile post comment.

        Returns:
            JsonType            
        """
        data = {"comment_body": comment_body}
        return self.post(
            f"/profile-posts/{profile_post_id}/comments", data=data
        )

    def get_profile_posts(
        self,
        user_id: int | UserType,
        *,
        page: int | None = None,
        limit: int | None = None,
    ) -> JsonType:
        """
        List of profile posts (with pagination).

        Required scopes:
            read

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.
            page (int):
                Page number of users.
            limit (int):
                Number of contents in a page.

        Returns:
            JsonType
        """
        params = {"page": page, "limit": limit}
        return self.get(f"/users/{user_id}", params=params)

    def get_profile_post(self, profile_post_id: int) -> JsonType:
        """
        Detail information of a profile post.

        Required scopes:
            read

        Args:
            profile_post_id (int):
                Id of profile post.

        Returns:
            JsonType
        """
        return self.get(f"/profile-posts/{profile_post_id}")

    def create_profile_post(
        self,
        user_id: int | UserType,
        post_body: str,
    ) -> JsonType:
        """
        Create a new profile post on a user timeline.

        Required scopes:
            post

        Args:
            user_id (int | str):
                Id of user.
                User shortlink. Use "me" to interact with your own
                profile.
            post_body (str):
                Content of the new profile post.

        Returns:
            JsonType
        """
        data = {"post_body": post_body}
        params = {"user_id": user_id}
        return self.post("/profile-posts", data=data, params=params)

    def edit_profile_post(
        self,
        profile_post_id: int,
        post_body: str,
    ) -> JsonType:
        """
        Edit a profile post.

        Required scopes:
            post

        Args:
            profile_post_id (int):
                Id of profile post.
            post_body (str):
                New content of the profile post.

        Returns:
            JsonType
        """
        data = {"post_body": post_body}
        return self.put(f"/profile-posts/{profile_post_id}", data=data)

    def delete_profile_post(
        self,
        profile_post_id: int,
        *,
        reason: str | None = None,
    ) -> JsonType:
        """
        Delete a profile post.

        Required scopes:
            post

        Args:
            profile_post_id (int):
                Id of profile post.
            reason (str):
                Reason of the profile post removal.

        Returns:
            JsonType
        """
        params = {"reason": reason}
        return self.delete(f"/profile-posts/{profile_post_id}", params=params)

    def get_profile_post_likes(self, profile_post_id: int) -> JsonType:
        """
        List of users who liked a profile post.

        Required scopes:
            read

        Args:
            profile_post_id (int):
                Id of profile post.
        
        Returns:
            JsonType
        """
        return self.get(f"/profile-posts/{profile_post_id}/likes")

    def like_profile_post(self, profile_post_id: int) -> JsonType:
        """
        Like a profile post.

        Required scopes:
            post

        Args:
            profile_post_id (int):
                Id of profile post.

        Returns:
            JsonType
        """
        return self.post(f"/profile-posts/{profile_post_id}/likes")

    def unlike_profile_post(self, profile_post_id: int) -> JsonType:
        """
        Unlike a profile post.

        Required scopes:
            post

        Args:
            profile_post_id (int):
                Id of profile post.

        Returns:
            JsonType
        """
        return self.delete(f"/profile-posts/{profile_post_id}/likes")

    def report_profile_post(
        self,
        profile_post_id: int,
        message: str,
    ) -> JsonType:
        """
        Report a profile post.

        Required scopes:
            post

        Args:
            profile_post_id (int):
                Id of profile post.
            message (str):
                Reason of the report.

        Returns:
            JsonType
        """
        params = {"message": message}
        return self.post(
            f"/profile-posts/{profile_post_id}/report", params=params
        )


class SyncConversationsMixin(SyncClientProtocol):
    def get_conversation_messages(
        self,
        conversation_id: int,
        *,
        page: int | None = None,
        limit: int | None = None,
        order: ConversationOrderType | None = None,
        before: int | None = None,
        after: int | None = None,
    ) -> JsonType:
        """
        List of messages in a conversation (with pagination).

        Required scopes:
            read
            conversate

        Args:
            conversation_id (int):
                Id of needed conversation.
            page (int):
                Page number of messages.
            limit (int):
                Number of messages in a page.
            order (str):
                Ordering of messages.
            before (int):
                Date to get older messages.
            after (int):
                Date to get newer messages.

        Returns:
            JsonType
        """
        params = {
            "conversation_id": conversation_id,
            "page": page,
            "limit": limit,
            "order": order,
            "before": before,
            "after": after,
        }
        return self.get("/conversation-messages", params=params)

    def get_conversation_message(self, message_id: int) -> JsonType:
        """
        Detail information of a message.

        Required scopes:
            read
            conversate

        Args:
            message_id (int):
                Id of message.

        Returns:
            JsonType
        """
        return self.get(f"/conversation-messages/{message_id}")

    def create_conversation_message(
        self,
        conversation_id: int,
        message_body: str,
    ) -> JsonType:
        """
        Create a new conversation message.

        Required scopes:
            post
            conversate

        Args:
            conversation_id (int):
                Id of needed conversation.
            message_body (str):
                Content of the new message.

        Returns:
            JsonType
        """
        data = {"message_body": message_body}
        return self.post(
            f"/conversation-messages/{conversation_id}", data=data
        )

    def edit_conversation_message(
        self,
        message_id: int,
        message_body: str,
    ) -> JsonType:
        """
        Edit a message.

        Required scopes:
            post
            conversate

        Args:
            messageId (int):
                Id of message.
            message_body (str):
                New content of the message.

        Returns:
            JsonType
        """
        data = {"message_body": message_body}
        return self.put(f"/conversation-messages/{message_id}", data=data)

    def get_conversations(
        self,
        *,
        page: int | None = None,
        limit: int | None = None,
    ) -> JsonType:
        """
        List of conversations (with pagination).

        Required scopes:
            read
            conversate

        Args:
            page (int):
                Page number of conversations.
            limit (int):
                Number of conversations in a page.

        Returns:
            JsonType
        """
        params = {"page": page, "limit": limit}
        return self.get("/conversations", params=params)

    def get_conversation(self, conversation_id: int) -> JsonType:
        """
        Detail information of a conversation.

        Required scopes:
            read
            conversate

        Args:
            conversation_id (int):
                Id of conversation

        Returns:
            JsonType
        """
        return self.get(f"/conversation/{conversation_id}")

    def create_conversation(
        self,
        title: str,
        message_body: str,
        is_group: bool = False,
        *,
        recipient_id: int | None = None,
        recipients: List[str] | None = None,
        open_invite: bool | None = None,
        conversation_locked: bool | None = None,
        allow_edit_messages: bool | None = None,
    ):
        """
        Create a new conversation.

        Required scopes:
            post
            conversate

        Args:
            title (str):
                The title of new conversation.
                Required if `is_group=true`.
            message_body (str):
                Message. Required if `is_group=false`.
            is_group (bool, defaults to `False`):
                Is group. Set `false `if personal conversation, or set
                `true `if group.
            recipient_id (int):
                Id of recipient. Required if `is_group=false`.
            recipients (list[str]):
                List of recipients username's. Max recipients count is
                10 (Separated by comma). Required if `is_group=true`.
            open_invite (bool):
                Open invite.
            conversation_locked (bool):
                Is conversation locked.
            allow_edit_messages (bool):
                Allow edit messages.

        Returns:
            JsonType
        """
        data = {"message_body": message_body}
        params = {
            "title": title,
            "is_group": is_group,
            "recipient_id": recipient_id,
            "recipients": recipients,
            "open_invite": open_invite,
            "conversation_locked": conversation_locked,
            "allow_edit_messages": allow_edit_messages,
        }
        return self.post("/conversation", data=data, params=params)

    def leave_conversation(
        self,
        conversation_id: int,
        delete_type: ConversationDeleteType,
    ) -> JsonType:
        """
        Leave the conversation.

        Required scopes:
            post
            conversate

        Args:
            conversation_id (int):
                Id of conversation.
            delete_type (str):
                Deletion type. Must be one of the following:
                - "delete"
                - "delete_ignore"

        Returns:
            JsonType
        """
        params = {"delete_type": delete_type}
        return self.delete(f"/conversations/{conversation_id}", params=params)


class SyncNotificationsMixin(SyncClientProtocol):
    def get_notifications(self) -> JsonType:
        """
        List of notifications (both read and unread).

        Required scopes:
            read

        Returns:
            JsonType
        """
        return self.get("/notifications")

    def get_notification(self, notification_id: int) -> JsonType:
        """
        Get associated content of notification. The response depends
        on the content type.

        Required scopes:
            read

        Args:
            notification_id (int):
                Id of notification.

        Returns:
            JsonType
        """
        return self.get(f"/notifications/{notification_id}")

    def mark_notification_read(
        self,
        *,
        notification_id: int | None = None,
    ) -> JsonType:
        """
        Mark single notification or all existing notifications read.

        Required scopes:
            post

        Args:
            notification_id (int):
                If notification_id is omitted, it's mark all existing
                notifications as read.

        Returns:
            JsonType
        """
        params = {"notification_id": notification_id}
        return self.post("/notifications/read", params=params)


class SyncContentTaggingMixin(SyncClientProtocol):
    def get_popular_tags(self) -> JsonType:
        """
        List of popular tags (no pagination).

        Required scopes:
            read

        Returns:
            JsonType
        """
        return self.get("/tags")

    def get_tags(
        self,
        *,
        page: int | None = None,
        limit: int | None = None,
    ) -> JsonType:
        """
        List of tags.

        Required scopes:
            read

        Args:
            page (int):
                Page number of tags list.
            limit (int):
                Number of results in a page.

        Returns:
            JsonType
        """
        params = {"page": page, "limit": limit}
        return self.get("/tags/list", params=params)

    def get_tagged_content(
        self,
        tag_id: int,
        *,
        page: int | None = None,
        limit: int | None = None,
    ) -> JsonType:
        """
        List of tagged contents.

        Required scopes:
            read

        Args:
            tagId (int):
                Id of tag.
            page (int):
                Page number of tagged contents.
            limit (int):
                Number of tagged contents in a page.

        Returns:
            JsonType
        """
        params = {"page": page, "limit": limit}
        return self.get(f"/tags/{tag_id}", params=params)

    def get_filtered_content(self, tag: str) -> JsonType:
        """
        Filtered list of tags.

        Required scopes:
            read

        Args:
            tag (str):
                tag to filter. Tags start with the query will be
                returned.

        Returns:
            JsonType
        """
        params = {"tag": tag}
        return self.get("/tags/find", params=params)


class SyncSearchingMixin(SyncClientProtocol):
    def search(
        self,
        query: str,
        *,
        tag: str | None = None,
        forum_id: str | None = None,
        user_id: int | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> JsonType:
        """
        Search for all supported contents.

        Required scopes:
            post

        Args:
            query (str):
                Search query. Can be skipped if `user_id` is set.
            tag (str):
                Tag to search for tagged contents.
            forum_id (int):
                Id of the container forum to search for contents.
                Child forums of the specified forum will be included in
                the search.
            user_id (int):
                Id of the creator to search for contents.
            page (int):
                Page number of results.
            limit (int):
                Number of results in a page.

        Returns:
            JsonType
        """
        params = {
            "q": query,
            "tag": tag,
            "forum_id": forum_id,
            "user_id": user_id,
            "page": page,
            "limit": limit,
        }
        return self.post("/search", params=params)

    def search_thread(
        self,
        query: str,
        *,
        tag: str | None = None,
        forum_id: int | None = None,
        user_id: int | None = None,
        page: int | None = None,
        limit: int | None = None,
        date_limit: int | None = None,
    ):
        """
        Search for threads.

        Required scopes:
            post
 
        Args:
            query (str):
                Search query. Can be skipped if `user_id` is set.
            tag (str):
                Tag to search for tagged contents.
            forum_id (int):
                Id of the container forum to search for contents.
                Child forums of the specified forum will be included in
                the search.
            user_id (int):
                Id of the creator to search for contents.
            page (int):
                Page number of results.
            limit (int):
                Number of results in a page.
            data_limit (int):
                Number of thread data to be returned.

        Returns:
            JsonType
        """
        params = {
            "q": query,
            "tag": tag,
            "forum_id": forum_id,
            "user_id": user_id,
            "page": page,
            "limit": limit,
            "date_limit": date_limit,
        }
        return self.post("/search/threads", params=params)

    def search_post(
        self,
        query: str,
        *,
        tag: str | None = None,
        forum_id: int | None = None,
        user_id: int | None = None,
        page: int | None = None,
        limit: int | None = None,
        date_limit: int | None = None,
    ) -> JsonType:
        """
        Search for posts.

        Required scopes:
            post

        Args:
            query (str):
                Search query. Can be skipped if `user_id` is set.
            tag (str):
                Tag to search for tagged contents.
            forum_id (int):
                Id of the container forum to search for contents.
                Child forums of the specified forum will be included in
                the search.
            user_id (int):
                Id of the creator to search for contents.
            page (int):
                Page number of results.
            limit (int):
                Number of results in a page.
            data_limit (int):
                Number of thread data to be returned.

        Returns:
            JsonType
        """
        params = {
            "q": query,
            "tag": tag,
            "forum_id": forum_id,
            "user_id": user_id,
            "page": page,
            "limit": limit,
            "date_limit": date_limit,
        }
        return self.post("/search/posts", params=params)

    def search_profile_posts(
        self,
        query: str,
        *,
        user_id: int | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> JsonType:
        """
        Search for profile posts.

        Required scopes:
            post

        Args:
            query (str):
                Search query. Can be skipped if `user_id` is set.
            user_id (int):
                Id of the creator to search for contents.
            page (int):
                Page number of results.
            limit (int):
                Number of results in a page.
            
        Returns:
            JsonType
        """
        params = {
            "q": query,
            "user_id": user_id,
            "page": page,
            "limit": limit,
        }
        return self.post("/search/profile-posts", params=params)

    def search_tagged(
        self,
        tag: str,
        *,
        tags: List[str] | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> JsonType:
        """
        Search for tagged contents.

        Required scopes:
            post

        Args:
            tag (str):
                Tag to search for tagged contents.
            tags (list[str]):
                Array of tags to search for tagged contents.
            page (int):
                Page number of results.
            limit (int):
                Number of results in a page.

        Returns:
            JsonType
        """
        params = {
            "tag": tag,
            "tags[]": tags,
            "page": page,
            "limit": limit,
        }
        return self.post("/search/tagged", params=params)


class SyncBatchRequestsMixin(SyncClientProtocol):
    def batch(self, data) -> JsonType:
        """
        Execute multiple API requests at once (Separated by comma).
        Maximum batch jobs is 10.

        Required scopes:
            Same as called API requests.

        Args:
            data (object): ...

        Returns:
            JsonType
        """
        return self.post("/batch", data=data)


class SyncAllMixin(
    SyncCategoriesMixin,
    SyncForumsMixin,
    SyncPagesMixin,
    SyncNavigationMixin,
    SyncThreadsMixin,
    SyncPostsMixin,
    SyncUsersMixin,
    SyncProfilePostsMixin,
    SyncConversationsMixin,
    SyncNotificationsMixin,
    SyncContentTaggingMixin,
    SyncSearchingMixin,
    SyncBatchRequestsMixin,
): ...
