CREATE TABLE Interactions (
    interactionId INT PRIMARY KEY AUTO_INCREMENT,
    userId INT REFERENCES FeedNotes(userId),
    noteId INT REFERENCES FeedNotes(noteId),
    timestamp DATETIME,
    interactionType ENUM('click', 'like', 'dislike', 'favorite', 'unfavorite'),
    interactionDuration DOUBLE
);