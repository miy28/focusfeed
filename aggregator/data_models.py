from dataclasses import dataclass, field

@dataclass
class FeedNote: #feednote struct
    title: str
    content: str
    url: str
    timestamp: str
    source: str
    extra_data: dict = field(default_factory=dict)
