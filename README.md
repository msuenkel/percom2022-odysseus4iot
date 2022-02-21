# PerCom2022-Artifact-Odysseus4IoT
This software artifact was developed in combination with the paper publication **Resource-Aware Classification via Model Management Enabled Data Stream Optimization** as artifact submission **Artifact: Resource-Aware Classification via Model Management Enabled Data Stream Optimization**. Links will be added later when available.

This artifact consists of a GitHub repository ([github.com/msuenkel/percom2022-odysseus4iot](https://github.com/msuenkel/percom2022-odysseus4iot)) and containerized software modules on DockerHub ([hub.docker.com/u/msuenkel](https://hub.docker.com/u/msuenkel))

1. [What is Odysseus4IoT](#odysseus4iot)
1. [What is Odysseus4IoT-GlobalQueryScript(GQS)](#odysseus4iotgqs)
1. [How to run this artifact](#howtorun)

<a name="odysseus4iot"></a>
## 1. What is Odysseus4IoT
Odysseus4IoT is a Java application which enables data stream optimizations for machine learning classification pipelines. First the operator graph representing the classification pipeline of selected machine learning models is generated. This step is exploiting the occurrences of identical processing and by that performs redundancy elimination. Additionally Odysseus4IoT also performs operator placement optimization by minimizing network utilization between participating Odysseus Server nodes.

Odysseus4IoT was developed using [OpenJDK 11](https://jdk.java.net/java-se-ri/11) and [Gson](https://mvnrepository.com/artifact/com.google.code.gson/gson).

<a name="odysseus4iotgqs"></a>
## 2. What is Odysseus4IoT-GlobalQueryScript(GQS)
GlobalQueryScript(GQS) is a Java application which enables the deployment of global queries to [Odysseus](https://odysseus.informatik.uni-oldenburg.de/) nodes. A global query is defined in JSON format. Odysseus4IoT is generating such global queries as output.

A global query consists of a **name** and a **list of partial queries**. A partial query represents a typical query in a DSMS like Odysseus. It has a **name** and a **parser** which defines the language in which the query is written. Also **server** information is provided which holds the **socket** and **user credentials** of the Odysseus node where this query is thought to be installed to. Lastly, the **queryText** contains the actual query.

GlobalQueryScript(GQS) was developed using [OpenJDK 11](https://jdk.java.net/java-se-ri/11) and [Gson](https://mvnrepository.com/artifact/com.google.code.gson/gson).

### 2.1. How to use GlobalQueryScript(GQS)
There are two modes in which GlobalQueryScript(GQS) can be used:
1. **Interactive Mode**  
When running GQS without parameters you will start it in interactive mode. This basically is a command line tool, where you can interactively put commands.
1. **Script Mode**  
When running GQS with {file} parameter you will start it in script mode. In this mode all the commands which are defined in the provided GQS script will be executed in order.

### 2.2. Available Commands
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

<a name="howtorun"></a>
## 3. How to run this artifact
1. Install Prerequisites
   1. Install OpenJDK 11
   1. Install Docker (Docker Compose >= 1.29.2)
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
4. Run the Odysseus4IoT ecosystem and wait until all the services are fully up and running  
```docker-compose up -d```
5. Run Odysseus4IoT/ModelMiner  
```gradlew runOdysseus4iot --args="1"```
6. Deployment via GQS  
```gradlew runOdysseus4iotGQS --args="script1.gqs"```
7. Shutting Down  
```docker-compose down -v```
