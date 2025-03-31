CREATE TABLE articlesKeywords (
    articleId INT REFERENCES Articles(articleId),
    keywordId INT REFERENCES Keywords(keywordId),
    PRIMARY KEY (articleId, keywordId)
);