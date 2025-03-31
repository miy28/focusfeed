CREATE TABLE FeedNotes (
    noteId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    articleId INT,
    FOREIGN KEY (articleId) REFERENCES Articles(articleId),
    title VARCHAR(255),
    summary VARCHAR(300),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);