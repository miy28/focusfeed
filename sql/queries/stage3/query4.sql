-- Keywords that are only found in one article
SELECT k.keyword
FROM Keywords k
JOIN articlesKeywords ak ON k.keywordId = ak.keywordId
GROUP BY k.keywordId, k.keyword
HAVING COUNT(DISTINCT ak.articleId) = 5
LIMIT 15;

CREATE INDEX idx ON articlesKeywords(articleId);
DROP INDEX idx ON Articles;