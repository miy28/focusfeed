SELECT a.articleId, a.title, a.abstract
FROM Articles a
JOIN articlesKeywords ak ON ak.articleId = a.articleId
JOIN Keywords k ON ak.keywordId = k.keywordId
WHERE k.keyword = (%s) -- simulate user wants 'keyword' in their feed.
ORDER BY RAND()
LIMIT 1;