CREATE TABLE ArticleStats (
    articleId INT PRIMARY KEY,
    likes_count INT DEFAULT 0,
    dislikes_count INT DEFAULT 0,
    FOREIGN KEY (articleId) REFERENCES Articles(articleId)
);
