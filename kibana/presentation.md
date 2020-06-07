%title: Kibana / Elasticsearch %author: tiagoprn %date: 2020-06-12

-> Kibana (and elasticsearch) <- =========

## Agenda

- Introduction to the ELK stack
- Elasticsearch - purpose
- Elasticsearch - concepts
- Elasticsearch - features
- Elasticsearch as your primary data store?
- Recommended way to use elasticsearch
- Kibana - The elasticsearch Web UI
- Using python to populate data into elasticsearch
- Exploring data on Kibana - The "Discover"
- Exploring data on Kibana - The "Saved Searches"
- Questions
- References / Recommended readings

-------------------------------------------------

# Elasticsearch - purpose

According to the official site:

"... applying domain specific knowledge to implement good relevancy models,
giving an overview of the entire result space, and doing things like spell
checking and autocompletion. All while being fast."

(due to that, it is used frequently on analytics and machine learning)

-------------------------------------------------

# Elasticsearch - purpose

On a single phrase:

Fast queries and agregations on big datasets.

-------------------------------------------------

# Elasticsearch - concepts

- NoSQL
- Index
- Sharding

-------------------------------------------------

# Elasticsearch - features

- NoSQL database ("Search-engine store")

- Schema-free (data can be inserted without an schema/structure)

- Distributed - through sharding

-------------------------------------------------

# Elasticsearch - features

- You can transform your data before indexing it (through Logstash or the
  ingest-node pipeline)

- You can (and should) map your index with the fields and its types for maximum
  performance

-------------------------------------------------

# Elasticsearch - features

- REST API to every operation on the index (inserting and querying data,
  managing the cluster, etc...)

- Using JSON to insert data and query it into the database, you can easily
  backup or extract data, integrating with other tooling.

- Powerful Web UI through Kibana

-------------------------------------------------

# Elasticsearch as your primary data store?

- Under certaing conditions, yes.

## Conditions:

- Your data is write once, read many. No updating, no need for transactions,
  integrity constraints, etc. (classical example: logs)

-------------------------------------------------

# Elasticsearch as your primary data store?

- But... you wish to do that, take these into account:

* You have backups of the data

* After indexed queries will be blazing fast, but it takes some time to build
  the index that enables that.

-------------------------------------------------

# Recommended way to use elasticsearch

- Elasticsearch is commonly used in addition to another database. That way, you
  can have the best of both worlds.

- The other database can impose constraints, transactions, etc...

- ...and you can feed these data to elasticsearch for fast searchs on high
  volumes, gaining for free the ability to do exploration analysis using Kibana
as the WebUI.

-------------------------------------------------

# Recommended way to use elasticsearch

"Like with everything else, there's no silver bullet, no one database to rule
them all. That's likely to always be the case, so know the strengths and
weaknesses of your stores!"

-------------------------------------------------

# QUESTIONS ?


-------------------------------------------------

## References / Recommended readings:

- [Recommended Readings](recommended_readings.md)

