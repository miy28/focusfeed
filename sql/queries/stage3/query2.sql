-- Articles with keyword Germany that don't include keyword Politics
SELECT a.title
FROM Articles a
WHERE a.articleId IN (
    SELECT ak1.articleId
    FROM articlesKeywords ak1
    JOIN Keywords k1 ON ak1.keywordId = k1.keywordId
    WHERE k1.keyword = 'Germany'
)
AND a.articleId NOT IN (
    SELECT ak2.articleId
    FROM articlesKeywords ak2
    JOIN Keywords k2 ON ak2.keywordId = k2.keywordId
    WHERE k2.keyword = 'Politics'
)
LIMIT 15;

CREATE INDEX idx ON Keywords(keyword);
DROP INDEX idx ON Keywords;