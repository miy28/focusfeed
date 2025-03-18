from dataclasses import dataclass, field

@dataclass
class FeedNote: #feednote struct
    # noteId: int
    title: str
    content: str
    url: str
    timestamp: str
    source: str
    keyword: str
    extra_data: dict = field(default_factory=dict)
