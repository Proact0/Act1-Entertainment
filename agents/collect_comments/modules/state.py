from typing import TypedDict, List, Optional

class CollectCommentsState(TypedDict, total=False):
    profile_url: str
    post_links: List[str]
    current_post_url: Optional[str]
    page_source: Optional[str]
    comments: List[str]
    csv_filename: str
