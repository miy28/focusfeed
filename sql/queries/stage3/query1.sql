-- Articles with the most amount of associated FeedNotes
SELECT a.articleId, a.title, COUNT(DISTINCT f.noteId) AS num_notes, COUNT(DISTINCT k.keywordId) AS num_keywords
FROM Articles a
JOIN FeedNotes f ON a.articleId = f.articleId
JOIN articlesKeywords ak ON a.articleId = ak.articleId
JOIN Keywords k ON ak.keywordId = k.keywordId
GROUP BY a.articleId, a.title
ORDER BY num_notes DESC, num_keywords DESC
LIMIT 15;

CREATE INDEX idx ON Articles(title);
DROP INDEX idx ON Articles;