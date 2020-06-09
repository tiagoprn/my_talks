%title: Kibana / Elasticsearch
%author: tiagoprn
%date: 2020-06-12

## Agenda

- Introduction to the ELK stack
- Elasticsearch - purpose
- Elasticsearch - concepts
- Elasticsearch - features
- Elasticsearch - What is sharding and its' benefits?
- Elasticsearch as your primary data store?
- Recommended way to use elasticsearch
- Considerations on how to query your data on elasticsearch
- Considerations on how to query your data on elasticsearch - example
- Using python to populate data into elasticsearch
- Kibana - The elasticsearch Web UI
- Exploring data on Kibana - The "Discover"
- Exploring data on Kibana - The "Saved Searches"
- Exploring data on Kibana - "Dashboards"
- Questions
- References / Recommended readings

-------------------------------------------------

# Introduction to the ELK stack

- [E]lasticsearch: data persistance, the "database"
- [L]ogstash: aggregates and transforms data before persisting
- [K]ibana: WebUI to Elasticsearch

The main value here is given by Elasticsearch. Both other components are
entirely optional.

-------------------------------------------------

# Elasticsearch - purpose (1/2)

According to the official site:

"... applying domain specific knowledge to implement good relevancy models,
giving an overview of the entire result space, and doing things like spell
checking and autocompletion. All while being fast."

(due to that, it is used frequently on analytics and machine learning)

-------------------------------------------------

# Elasticsearch - purpose (2/2)

On a single phrase:

Fast queries and agregations on big datasets.

-------------------------------------------------

# Elasticsearch - concepts

- NoSQL: a no-relational database
- Index: It is analogous to a "database" on the relational world.
- Sharding: Mechanism to distribute your data between nodes.

-------------------------------------------------

# Elasticsearch - features (1/3)

- NoSQL database ("Search-engine store")

- Schema-free (data can be inserted without an schema/structure)

- Distributed - through sharding

-------------------------------------------------

# Elasticsearch - features (2/3)

- You can transform your data before indexing it (through Logstash or the
  ingest-node pipeline)

- You can (and should) map your index with the fields and its types for maximum
  performance

-------------------------------------------------

# Elasticsearch - features (3/3)

- REST API to every operation on the index (inserting and querying data,
  managing the cluster, etc...)

- Using JSON to insert data and query it into the database, you can easily
  backup or extract data, integrating with other tooling.

- Powerful Web UI through Kibana

-------------------------------------------------

# Elasticsearch - What is sharding and its' benefits?

- sharding = split index data into smaller parts (shards). Each one of those
  parts lives on a different node (machine) - AKA "horizontal scaling".

- Enables higher performance/throughput, since you can distribute and
  paralelize operations between the shards.

- Also useful to help on failover handling, enabling to have one or more copies
  of the same data on many nodes.

-------------------------------------------------

# Elasticsearch as your primary data store? (1/2)

- Under certaing conditions, yes.

## Conditions:

- Your data is write once, read many. No updating, no need for transactions,
  integrity constraints, etc. (classical example: logs)

-------------------------------------------------

# Elasticsearch as your primary data store? (2/2)

- But... you wish to do that, take these into account:

* You have backups of the data

* After indexed queries will be blazing fast, but it takes some time to build
  the index that enables that.

-------------------------------------------------

# Recommended way to use elasticsearch (1/2)

- Elasticsearch is commonly used in addition to another database. That way, you
  can have the best of both worlds.

- The other database can impose constraints, transactions, etc...

- ...and you can feed these data to elasticsearch for fast searchs on high
  volumes, gaining for free the ability to do exploration analysis using Kibana
as the WebUI.

-------------------------------------------------

# Recommended way to use elasticsearch (2/2)

"Like with everything else, there's no silver bullet, no one database to rule
them all. That's likely to always be the case, so know the strengths and
weaknesses of your stores!"

-------------------------------------------------

# Considerations on how to query your data on elasticsearch (1/3)

- When you index (save) a document into ElasticSearch, that document is saved
  multiple times — on a shard and its replica(s). However, the information you
save is only made available at the next index refresh.

-------------------------------------------------

# Considerations on how to query your data on elasticsearch (2/3)

- **An index refresh is an operation that makes the latest changes applied to an**
**index available for search** (meaning they’ll reflect in results for search
queries). ElasticSearch **refreshes every index automatically by the value of its**
**refresh interval, which is set to 1 second by default**.

-------------------------------------------------

# Considerations on how to query your data on elasticsearch (3/3)

- **ElasticSearch does not "just" store the data you index, but it also tries to**
  **detect and determine the data type of each field you send it using dynamic**
**mapping.** It then uses tokenizers to break the indexed data into individual
terms (e.g: a textual sentence can be broken down into individual words, using
a whitespace as a separator to detect individual search terms within it). Then
it stores that information next to the original payload. That is one of the
reasons on why it makes statistical analysis so fast on big datasets, and
that is also important to understand why some queries we send to it do not work.

-------------------------------------------------

# Considerations on how to query your data on elasticsearch - example (1/3)

- Suppose we insert the following text to be stored on es:

`Email me at john.smith@global-international.com`

This will be stored on elasticsearch as:

`[ Email, me, at, john.smith, global, international.com ]`

**Noticed the e-mail is not stored as an e-mail?** So, if you try an exact search
for `john.smith@global-international.com`, it will never return. But you can
overcome that using es "mapping" feature.

-------------------------------------------------

# Considerations on how to query your data on elasticsearch - example (2/3)

- With the mapping feature we can tell es how to store the information and how
  we plan to search for it. On the example above, we would have to tell es that
we want it to NOT analyse an e-mail field when it finds one, so that we can do
an exact search on its` value. On the next slide we can see an example on how
to do that:

```
elasticSearchClient.indices.create({
 "index":"users", //index name
 "body":{
  "mappings":{
   "someType" : { //document type
    "properties" : {
     "email" : { //Prevent email field from being analyzed
      "type" : "string",
      "index" : "not_analyzed"
      }
     }
    }
   }
  }
});
```

-------------------------------------------------

# Considerations on how to query your data on elasticsearch - example (3/3)

Then, we could query like below:

```
elasticSearchClient.search({
 index: "users",
 type: "sometype",
 body: {
  query:{
    "bool": {
      "must": [
        {
          term:{
           "email": "john.smith@global-international.com"
          }
        }
      ]
    }
  }
 })
```

-------------------------------------------------

# Using python to populate data into elasticsearch

- Simple insert
(inserting records one by one on es)

`make populate-simple`

- Bulk insert
(bulk/mass inserting records on es)

`make populate-bulk`

-------------------------------------------------

# Kibana - The elasticsearch Web UI

TODO

-------------------------------------------------

# Exploring data on Kibana - The "Discover"

## Queries:
(Important: all operators and commands from kibana query language must be
UPPERCASE)

Examples:

- Name: "Final Fantasy" AND Genre: Role-Playing
- mario AND tennis
- (Name: mario AND tennis) AND (Rank: [10000 TO 99000])
- Rank: [1 TO 10]
- Rank: 1
- Rank:>=10 AND Rank:<=15
- (Rank:>=800) AND (Rank:<=1000) AND (Name: Mario) AND (NOT Name: Party)
- Publisher:Nintendo AND Name: Animal
- Name: ?ario AND (Platform:GB)

**TIP:** If you need to sort your data by a specific field and on asc/desc order, you can
manipulate the final piece of the URL on kibana. E.g.:

```
http://localhost:5601/app/kibana#/...,sort:!(Global_Sales,desc))
                                      ^----------- HERE you can manipulate the sorting
```

-------------------------------------------------

# Exploring data on Kibana - The "Saved Searches"

TODO

-------------------------------------------------

# Exploring data on Kibana - "Dashboards"

TODO

-------------------------------------------------

# QUESTIONS ?


-------------------------------------------------

# References / Recommended readings:

- [Recommended Readings](recommended_readings.md)

Data from the video games sales dataset was downloaded as CSV from
[here](https://www.kaggle.com/gregorut/videogamesales)

