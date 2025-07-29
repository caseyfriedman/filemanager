
CREATE DATABASE test1;

CREATE TABLE IF NOT EXISTS "public"."timestamp_test" (
    "id" uuid NOT NULL,
    "filename" text NOT NULL,
    "fileloc" text NOT NULL,
    "metadata" jsonb NOT NULL,
    "timestamp_added" timestamp NOT NULL,
    "timestamp_updated" timestamp
)
WITH (oids = false);

CREATE INDEX IF NOT EXISTS idx_timestamp_added ON public.timestamp_test USING btree (timestamp_added);

CREATE INDEX IF NOT EXISTS timestamp_test_metadata_idx ON public.timestamp_test USING gin (metadata jsonb_path_ops);
