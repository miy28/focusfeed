CREATE TABLE Keywords (
    keywordId INT PRIMARY KEY AUTO_INCREMENT,
    keyword VARCHAR(200) UNIQUE -- normalized keywords to help semantic search and indexing
);