CREATE TABLE Articles (
    articleId INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    abstract VARCHAR(255),
    url VARCHAR(255),
    publishedAt DATETIME
);