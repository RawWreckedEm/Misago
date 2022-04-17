from typing import Dict, Optional

from ariadne import SubscriptionType, convert_kwargs_to_snake_case

from ....categories.get import get_category_by_id
from ....categories.models import Category
from ....pubsub.threads import threads_updates
from ...cleanargs import InvalidArgumentError, clean_id_arg

threads_subscription = SubscriptionType()


@threads_subscription.source("threads")
@convert_kwargs_to_snake_case
async def threads_source(*_, category: Optional[str] = None):
    category_obj = None
    categories_map: Dict[int, bool] = {}

    try:
        category_id = clean_id_arg(category) if category else None
        if category and category_id:
            category_obj = await get_category_by_id(category_id)
            categories_map[category_id] = bool(category_obj)
    except InvalidArgumentError:
        pass

    # consume thread event, check if its category is subscribed before yielding
    async for event in threads_updates():
        if category and not category_obj:
            continue  # skip all threads

        event_category_id = event["category_id"]
        if event_category_id not in categories_map:
            categories_map[event_category_id] = await is_event_in_subscribed_category(
                category_obj, event_category_id
            )

        if not categories_map[event_category_id]:
            continue  # failed to find category

        yield event


async def is_event_in_subscribed_category(
    category: Optional[Category], event_category_id: int
) -> bool:
    event_category = await get_category_by_id(event_category_id)
    if not event_category:
        # event category is invalid category type or expired
        return False
    if not category:
        # skip check if event's category is child to subscribed category
        return True

    return category.is_parent(event_category)


@threads_subscription.field("threads")
def threads_resolver(
    obj, *_, category: Optional[str] = None  # pylint: disable=unused-argument
):
    return obj["id"]
