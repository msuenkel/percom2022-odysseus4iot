# percom2022-odysseus4iot

# Welcome to GlobalQueryScript(GQS) for Odysseus

## What is GlobalQueryScript(GQS)
GlobalQueryScript(GQS) is a Java application which enables the deployment of global queries to [Odysseus](https://odysseus.informatik.uni-oldenburg.de/) nodes. A global query is defined in JSON format. A sample global query definition can be found [here](https://gitlab.rz.uni-bamberg.de/mobi/futureiot/odysseus4iot/-/blob/master/eclipse-project/odysseus4iot/globalquery1.json).  

A global query consists of a **name** and a **list of partial queries**. A partial query represents a typical query in a DSMS like Odysseus. It has a **name** and a **parser** which defines the language in which the query is written. Also **server** information is provided which holds the **socket** and **user credentials** of the Odysseus node where this query is thought to be installed to. Lastly, the **queryText** contains the actual query. A sample Odysseus query can be found [here](https://gitlab.rz.uni-bamberg.de/mobi/futureiot/odysseus4iot/-/blob/master/eclipse-project/odysseus4iot/samplequery.qry). In order to convert a pretty formatted query text to a single line JSON value string you can use a tool like [Unicode to Java string literal converter](http://snible.org/java2/uni2java.html).  

GlobalQueryScript(GQS) was developed using [OpenJDK 11](https://jdk.java.net/java-se-ri/11) and [Gson](https://mvnrepository.com/artifact/com.google.code.gson/gson).

## How to use GlobalQueryScript(GQS)
You can either get the source code by cloning this repository and compiling and running it on your own or by using the [executable jar file](https://gitlab.rz.uni-bamberg.de/mobi/futureiot/odysseus4iot/-/blob/master/eclipse-project/odysseus4iot/gqs.jar). There are two modes in which GlobalQueryScript(GQS) can be used:
1. **Interactive Mode**  
When running GQS without parameters you will start it in interactive mode. This basically is a command line tool, where you can interactively put commands.
   ```
   java -jar gqs.jar
   ```
1. **Script Mode**  
When running GQS with {file} parameter you will start it in script mode. In this mode all the commands which are defined in the provided GQS script will be executed in order. A sanple GQS script can be found [here](https://gitlab.rz.uni-bamberg.de/mobi/futureiot/odysseus4iot/-/blob/master/eclipse-project/odysseus4iot/script1.gqs).
   ```
   java -jar gqs.jar script.gqs
   ```
## Available Commands
The commands which are available in the interactive mode and can be used writing a GQS schript are depicted in the following table.  

| Command          | Description                            |
| ---------------- |  ------------------------------------- |
| load {file}      | loads a global query from a json file  |
| unload {qname}   | unloads a global query by query name   |
| list             | lists all loaded global queries        |
| deploy {qname}   | deploys a global query by query name   |
| undeploy {qname} | undeploys a global query by query name |
| exit             | terminates the application             |
| quit             | terminates the application             |



# PerCom2022-Artifact-Odysseus4IoT
This software artifact was developed in combination with the paper publication **Resource-Aware Classification via Model Management Enabled Data Stream Optimization** as artifact submission **Resource-Aware Classification via Model Management Enabled Data Stream Optimization (Artifact)**. Links will be added later when available.

This artifact consists of a GitHub repository ([github.com/msuenkel/](https://github.com/msuenkel/percom2022-odysseus4iot)) and containerized software modules on DockerHub ([hub.docker.com/u/msuenkel](https://hub.docker.com/u/msuenkel))

In order to run this artifact successfully

1. Prerequisites
   1. Install JDK 11
   1. Install Docker
   1. Install pgAdmin
   1. Install GraphViz
2. Clone this git repository  
```git clone https://github.com/msuenkel/percom2022-odysseus4iot.git```
3. Pull docker images
```docker pull msuenkel/percom2022-odysseus-server:latest```  
```docker pull msuenkel/percom2022-odysseus-webstudio-backend:latest```  
```docker pull msuenkel/percom2022-odysseus-webstudio-frontend:latest```  
```docker pull msuenkel/percom2022-odysseus-webstudio-mongo:latest```  
```docker pull msuenkel/percom2022-postgres:latest```  
```docker pull msuenkel/percom2022-python-rpc-classification:latest```
4. Run Odysseus4IoT Ecosystem (Wait until all the services are fully up and running!)  
```docker compose up -d``` in ```/```
5. Run Odysseus4IoT/ModelMiner  
```gradlew runOdysseus4iot --args="1"``` in ```/```
6. Deployment via GQS  
```gradlew runOdysseus4iotGQS --args="script1.gqs"``` in ```/```
7. Shutting Down  
```docker compose down -v``` in ```/```

SQL for computing evaluation results in db as views
```
CREATE EXTENSION postgres_fdw;

CREATE SERVER fdw_cattledb
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'localhost', port '5432', dbname 'cattledb');

CREATE USER MAPPING FOR postgres
SERVER fdw_cattledb
OPTIONS (user 'postgres', password 'postgres');

CREATE FOREIGN TABLE fdw_result_sensor_data_19_eval_1
(
    bytes_sent integer,
    minlatencyinms bigint
)
SERVER fdw_cattledb
OPTIONS (schema_name 'public', table_name '_result_sensor_data_19_eval_1');

CREATE FOREIGN TABLE fdw_result_sensor_data_19_eval_2
(
    bytes_sent integer,
    minlatencyinms bigint
)
SERVER fdw_cattledb
OPTIONS (schema_name 'public', table_name '_result_sensor_data_19_eval_2');

CREATE FOREIGN TABLE fdw_result_sensor_data_19_eval_3
(
    bytes_sent integer,
    minlatencyinms bigint
)
SERVER fdw_cattledb
OPTIONS (schema_name 'public', table_name '_result_sensor_data_19_eval_3');

CREATE FOREIGN TABLE fdw_result_sensor_data_20_eval_1
(
    bytes_sent integer,
    minlatencyinms bigint
)
SERVER fdw_cattledb
OPTIONS (schema_name 'public', table_name '_result_sensor_data_20_eval_1');

CREATE FOREIGN TABLE fdw_result_sensor_data_20_eval_2
(
    bytes_sent integer,
    minlatencyinms bigint
)
SERVER fdw_cattledb
OPTIONS (schema_name 'public', table_name '_result_sensor_data_20_eval_2');

CREATE FOREIGN TABLE fdw_result_sensor_data_20_eval_3
(
    bytes_sent integer,
    minlatencyinms bigint
)
SERVER fdw_cattledb
OPTIONS (schema_name 'public', table_name '_result_sensor_data_20_eval_3');

CREATE FOREIGN TABLE fdw_result_node2_1
(
    bytes_sent integer,
    minlatencyinms bigint
)
SERVER fdw_cattledb
OPTIONS (schema_name 'public', table_name '_result_node2_1');

CREATE FOREIGN TABLE fdw_result_sink_1
(
    bytes_sent integer,
    minlatencyinms bigint
)
SERVER fdw_cattledb
OPTIONS (schema_name 'public', table_name '_result_sink_1');

CREATE VIEW evalcase1 AS
SELECT 'evalcase1' AS evalcase, subquery1.networkloadInBytes_edge, 0 AS networkloadInBytes_fog, subquery1.networkloadInBytes_edge AS networkloadInBytes_total, subquery2.latencyInMS_avg, subquery2.latencyInMS_median, subquery2.latencyInMS_min, subquery2.latencyInMS_max
FROM
(
	SELECT SUM(subquery0.bytes_sent) AS networkloadInBytes_edge
	FROM
	(
		SELECT MAX(fdw_result_sensor_data_19_eval_1.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_19_eval_1
		UNION ALL
		SELECT MAX(fdw_result_sensor_data_20_eval_2.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_20_eval_2
	) subquery0
) subquery1,
(
	SELECT ROUND(AVG(fdw_result_sink_1.minlatencyinms)) AS latencyInMS_avg, percentile_cont(0.5) WITHIN GROUP (ORDER BY fdw_result_sink_1.minlatencyinms ASC) AS latencyInMS_median, MIN(fdw_result_sink_1.minlatencyinms) AS latencyInMS_min, MAX(fdw_result_sink_1.minlatencyinms) AS latencyInMS_max
	FROM fdw_result_sink_1
)subquery2;

CREATE VIEW evalcase2 AS
SELECT 'evalcase2' AS evalcase, subquery1.networkloadInBytes_edge, subquery2.networkloadInBytes_fog, (subquery1.networkloadInBytes_edge + subquery2.networkloadInBytes_fog) AS networkloadInBytes_total, subquery3.latencyInMS_avg, subquery3.latencyInMS_median, subquery3.latencyInMS_min, subquery3.latencyInMS_max
FROM
(
	SELECT SUM(subquery0.bytes_sent) AS networkloadInBytes_edge
	FROM
	(
		SELECT MAX(fdw_result_sensor_data_19_eval_1.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_19_eval_1
		UNION ALL
		SELECT MAX(fdw_result_sensor_data_19_eval_2.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_19_eval_2
		UNION ALL
		SELECT MAX(fdw_result_sensor_data_19_eval_3.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_19_eval_3
		UNION ALL
		SELECT MAX(fdw_result_sensor_data_20_eval_1.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_20_eval_1
		UNION ALL
		SELECT MAX(fdw_result_sensor_data_20_eval_2.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_20_eval_2
		UNION ALL
		SELECT MAX(fdw_result_sensor_data_20_eval_3.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_20_eval_3
	) subquery0
) subquery1,
(
	SELECT SUM(subquery0.bytes_sent) AS networkloadInBytes_fog
	FROM
	(
		SELECT MAX(fdw_result_node2_1.bytes_sent) AS bytes_sent
		FROM fdw_result_node2_1
	) subquery0
) subquery2,
(
	SELECT ROUND(AVG(fdw_result_node2_1.minlatencyinms)) AS latencyInMS_avg, percentile_cont(0.5) WITHIN GROUP (ORDER BY fdw_result_node2_1.minlatencyinms ASC) AS latencyInMS_median, MIN(fdw_result_node2_1.minlatencyinms) AS latencyInMS_min, MAX(fdw_result_node2_1.minlatencyinms) AS latencyInMS_max
	FROM fdw_result_node2_1
)subquery3;

CREATE VIEW evalcase3 AS
SELECT 'evalcase3' AS evalcase, subquery1.networkloadInBytes_edge, subquery2.networkloadInBytes_fog, (subquery1.networkloadInBytes_edge + subquery2.networkloadInBytes_fog) AS networkloadInBytes_total, subquery3.latencyInMS_avg, subquery3.latencyInMS_median, subquery3.latencyInMS_min, subquery3.latencyInMS_max
FROM
(
	SELECT SUM(subquery0.bytes_sent) AS networkloadInBytes_edge
	FROM
	(
		SELECT MAX(fdw_result_sensor_data_19_eval_1.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_19_eval_1
		UNION ALL
		SELECT MAX(fdw_result_sensor_data_19_eval_2.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_19_eval_2
		UNION ALL
		SELECT MAX(fdw_result_sensor_data_20_eval_1.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_20_eval_1
		UNION ALL
		SELECT MAX(fdw_result_sensor_data_20_eval_2.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_20_eval_2
	) subquery0
) subquery1,
(
	SELECT SUM(subquery0.bytes_sent) AS networkloadInBytes_fog
	FROM
	(
		SELECT MAX(fdw_result_node2_1.bytes_sent) AS bytes_sent
		FROM fdw_result_node2_1
	) subquery0
) subquery2,
(
	SELECT ROUND(AVG(fdw_result_node2_1.minlatencyinms)) AS latencyInMS_avg, percentile_cont(0.5) WITHIN GROUP (ORDER BY fdw_result_node2_1.minlatencyinms ASC) AS latencyInMS_median, MIN(fdw_result_node2_1.minlatencyinms) AS latencyInMS_min, MAX(fdw_result_node2_1.minlatencyinms) AS latencyInMS_max
	FROM fdw_result_node2_1
)subquery3;

CREATE VIEW evalcase4 AS
SELECT 'evalcase4' AS evalcase, subquery1.networkloadInBytes_edge, subquery2.networkloadInBytes_fog, (subquery1.networkloadInBytes_edge + subquery2.networkloadInBytes_fog) AS networkloadInBytes_total, subquery3.latencyInMS_avg, subquery3.latencyInMS_median, subquery3.latencyInMS_min, subquery3.latencyInMS_max
FROM
(
	SELECT SUM(subquery0.bytes_sent) AS networkloadInBytes_edge
	FROM
	(
		SELECT MAX(fdw_result_sensor_data_19_eval_1.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_19_eval_1
		UNION ALL
		SELECT MAX(fdw_result_sensor_data_20_eval_1.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_20_eval_1
	) subquery0
) subquery1,
(
	SELECT SUM(subquery0.bytes_sent) AS networkloadInBytes_fog
	FROM
	(
		SELECT MAX(fdw_result_node2_1.bytes_sent) AS bytes_sent
		FROM fdw_result_node2_1
	) subquery0
) subquery2,
(
	SELECT ROUND(AVG(fdw_result_node2_1.minlatencyinms)) AS latencyInMS_avg, percentile_cont(0.5) WITHIN GROUP (ORDER BY fdw_result_node2_1.minlatencyinms ASC) AS latencyInMS_median, MIN(fdw_result_node2_1.minlatencyinms) AS latencyInMS_min, MAX(fdw_result_node2_1.minlatencyinms) AS latencyInMS_max
	FROM fdw_result_node2_1
)subquery3;

CREATE VIEW evalcase5 AS
SELECT 'evalcase5' AS evalcase, subquery1.networkloadInBytes_edge, subquery2.networkloadInBytes_fog, (subquery1.networkloadInBytes_edge + subquery2.networkloadInBytes_fog) AS networkloadInBytes_total, subquery3.latencyInMS_avg, subquery3.latencyInMS_median, subquery3.latencyInMS_min, subquery3.latencyInMS_max
FROM
(
	SELECT SUM(subquery0.bytes_sent) AS networkloadInBytes_edge
	FROM
	(
		SELECT MAX(fdw_result_sensor_data_19_eval_1.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_19_eval_1
		UNION ALL
		SELECT MAX(fdw_result_sensor_data_20_eval_1.bytes_sent) AS bytes_sent
		FROM fdw_result_sensor_data_20_eval_1
	) subquery0
) subquery1,
(
	SELECT SUM(subquery0.bytes_sent) AS networkloadInBytes_fog
	FROM
	(
		SELECT MAX(fdw_result_node2_1.bytes_sent) AS bytes_sent
		FROM fdw_result_node2_1
	) subquery0
) subquery2,
(
	SELECT ROUND(AVG(fdw_result_sink_1.minlatencyinms)) AS latencyInMS_avg, percentile_cont(0.5) WITHIN GROUP (ORDER BY fdw_result_sink_1.minlatencyinms ASC) AS latencyInMS_median, MIN(fdw_result_sink_1.minlatencyinms) AS latencyInMS_min, MAX(fdw_result_sink_1.minlatencyinms) AS latencyInMS_max
	FROM fdw_result_sink_1
)subquery3;
```