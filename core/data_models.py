import pickle

from dataclasses import dataclass, field

@dataclass
class ArticleIterator: # previously FeedNote struct
    # noteId: int
    title: str
    desc: str
    url: str
    timestamp: str
    source: str
    keywords: list[str]
    snippet: str
    extra_data: dict = field(default_factory=dict)

@dataclass
class FeedNote:
    title: str
    summary: str
    url: str 