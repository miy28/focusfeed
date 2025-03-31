-- have to do this to ensure we get the original id if we tried insert on existing keyword.
SELECT keywordId
FROM Keywords
WHERE keyword = (%s);