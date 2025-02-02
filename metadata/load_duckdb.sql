INSTALL parquet;
LOAD parquet;

CREATE TABLE metadata AS
    SELECT * FROM read_parquet("./bw_db/metadata.parquet");

CREATE UNIQUE INDEX acc_idx ON metadata (acc);
