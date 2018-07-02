USE cse587;

DROP TABLE IF EXISTS facebook;
DROP TABLE IF EXISTS cambridgeAnalytic;
DROP TABLE IF EXISTS nytDocs;
DROP TABLE IF EXISTS nytFacebookDocs;
DROP TABLE IF EXISTS nytCamAnalyDocs;

CREATE TABLE cambridgeAnalytic(
tweetID bigint(20) PRIMARY KEY NOT NULL,
tweetDate DATETIME
);

CREATE TABLE facebook(
tweetID bigint(20) PRIMARY KEY NOT NULL,
tweetDate DATETIME
);

CREATE TABLE nytFacebookDocs(
docID VARCHAR(24) PRIMARY KEY NOT NULL,
docURL text,
docDate DATE
);

CREATE TABLE nytCamAnalyDocs(
docID VARCHAR(24) PRIMARY KEY NOT NULL,
docURL text,
docDate DATE
);