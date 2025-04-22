-- Articles with keyword Matcha that also have at least 5 keywords (article is content-heavy)
SELECT a.title
FROM Articles a
WHERE a.articleId IN (
    SELECT ak1.articleId
    FROM articlesKeywords ak1
    JOIN Keywords k1 ON ak1.keywordId = k1.keywordId
    WHERE k1.keyword = "Australia"
)
AND a.articleId IN (
    SELECT ak2.articleId
    FROM articlesKeywords ak2
    GROUP BY ak2.articleId
    HAVING COUNT(DISTINCT ak2.keywordId) >= 5
)
LIMIT 15;

CREATE INDEX idx ON Keywords(keyword);
DROP INDEX idx ON Keywords;