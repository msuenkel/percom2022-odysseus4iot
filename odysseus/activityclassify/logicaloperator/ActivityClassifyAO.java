package activityclassify.logicaloperator;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.logging.Logger;

import org.postgresql.core.JavaVersion;

import de.uniol.inf.is.odysseus.core.logicaloperator.LogicalOperatorCategory;
import de.uniol.inf.is.odysseus.core.predicate.IPredicate;
import de.uniol.inf.is.odysseus.core.sdf.schema.SDFAttribute;
import de.uniol.inf.is.odysseus.core.sdf.schema.SDFDatatype;
import de.uniol.inf.is.odysseus.core.sdf.schema.SDFSchema;
import de.uniol.inf.is.odysseus.core.sdf.schema.SDFSchemaFactory;
import de.uniol.inf.is.odysseus.core.server.logicaloperator.AbstractLogicalOperator;
import de.uniol.inf.is.odysseus.core.server.logicaloperator.UnaryLogicalOp;
import de.uniol.inf.is.odysseus.core.server.logicaloperator.annotations.LogicalOperator;
import de.uniol.inf.is.odysseus.core.server.logicaloperator.annotations.Parameter;
import de.uniol.inf.is.odysseus.core.server.logicaloperator.builder.BooleanParameter;
import de.uniol.inf.is.odysseus.core.server.logicaloperator.builder.PredicateParameter;
import de.uniol.inf.is.odysseus.core.server.logicaloperator.builder.StringParameter;
import de.uniol.inf.is.odysseus.core.server.physicaloperator.IHasPredicates;

@LogicalOperator(name = "ActivityClassify", minInputPorts = 1, maxInputPorts = 1, doc = "This operator can be used to route the elements in the stream to different further processing operators, depending on the predicate.", category = { LogicalOperatorCategory.PROCESSING })
public class ActivityClassifyAO extends UnaryLogicalOp implements IHasPredicates
{
	private static final long serialVersionUID = -8015847502104587689L;

	private boolean overlappingPredicates = false;
	private List<IPredicate<?>> predicates = new LinkedList<IPredicate<?>>();

	/**
	 * if an element is routed to an output, heartbeats will be send to all
	 * other outputs.
	 */
	private boolean sendingHeartbeats = false;
	private String table;
	private String selectModelByColumn;
	private String username;
	private String password;
	private String host;
	private String port;
	private String database;
	private String rpcServer;
	private String selectModelByValue;
    Logger lgr = Logger.getLogger(JavaVersion.class.getName());

	public ActivityClassifyAO()
	{
		super();
	}

	public ActivityClassifyAO(ActivityClassifyAO activityClassifyAO)
	{
		super(activityClassifyAO);
		this.overlappingPredicates = activityClassifyAO.overlappingPredicates;
		this.sendingHeartbeats = activityClassifyAO.sendingHeartbeats;
		this.table=activityClassifyAO.table;
		this.username=activityClassifyAO.username;
		this.password=activityClassifyAO.password;
		this.host=activityClassifyAO.host;
		this.port=activityClassifyAO.port;
		this.rpcServer=activityClassifyAO.rpcServer;
		this.database=activityClassifyAO.getDatabase();
		this.selectModelByColumn=activityClassifyAO.selectModelByColumn;
		this.selectModelByValue=activityClassifyAO.selectModelByValue;
		
		if(activityClassifyAO.predicates != null)
		{
			for(IPredicate<?> pred : activityClassifyAO.predicates)
			{
				this.predicates.add(pred.clone());
			}
		}
	}
	
	/* BY OORMILA
	@Override
	protected SDFSchema getOutputSchemaIntern(int pos)
	{
		 List<SDFAttribute> outputAttributes = new ArrayList<SDFAttribute>();
		    // Retrieve old attributes (they should all be part of the output schema)
		    outputAttributes.addAll(getInputSchema(0).getAttributes());
		 
		    // add new Attributes
		    SDFAttribute prediction = new SDFAttribute(null, "prediction",
		            SDFDatatype.STRING, null, null, null);
		   outputAttributes.add(prediction);
		    // Create new Schema with Factory, keep input Schema!
		    SDFSchema schema = SDFSchemaFactory.createNewWithAttributes(outputAttributes, getInputSchema(0));
		    return schema;
	}*/
	
	@Override
	protected SDFSchema getOutputSchemaIntern(int pos)
	{
		List<SDFAttribute> outputAttributes = new ArrayList<SDFAttribute>();
		// Retrieve old attributes and add only the first one (should be the id)
		outputAttributes.add(getInputSchema(0).getAttributes().get(0));
		// add new Attributes
		SDFAttribute activity = new SDFAttribute(null, "activity",
		SDFDatatype.STRING, null, null, null);
		outputAttributes.add(activity);
		// Create new Schema with Factory, keep input Schema!
		SDFSchema schema = SDFSchemaFactory.createNewWithAttributes(outputAttributes, getInputSchema(0));
		return schema;
	}

	@Parameter(type = PredicateParameter.class, isList = true,optional = true)
	public void setPredicates(List<IPredicate<?>> predicates)
	{
		this.predicates = predicates;
		addParameterInfo("PREDICATES", generatePredicatesString(predicates));
	}
	
	@Override
	public List<IPredicate<?>> getPredicates()
	{
		return predicates;
	}

	private String generatePredicatesString(List<IPredicate<?>> predicates)
	{
		StringBuilder sb = new StringBuilder();
		sb.append("[");
		
		for(int i = 0; i < predicates.size(); i++)
		{
			IPredicate<?> predicate = predicates.get(i);
			sb.append(generatePredicateString(predicate));
			
			if(i < predicates.size() - 1)
			{
				sb.append(",");
			}
		}
		
		sb.append("]");
		
		return sb.toString();
	}

	private String generatePredicateString(IPredicate<?> predicate)
	{
		return "RelationalPredicate('" + predicate.toString() + "')";
	}

	@Override
	public AbstractLogicalOperator clone()
	{
		return new ActivityClassifyAO(this);
	}
	
	@Parameter(name = "overlappingPredicates", type = BooleanParameter.class, optional = true, doc = "Evaluate all (true) or only until first true predicate (false), i.e. deliver to all ports where predicate is true or only to first")
	public void setOverlappingPredicates(boolean overlappingPredicates)
	{
		this.overlappingPredicates = overlappingPredicates;
	}
	
	public boolean isOverlappingPredicates()
	{
		return this.overlappingPredicates;
	}
	
	@Parameter(name = "sendingHeartbeats", type = BooleanParameter.class, optional = true, doc = "If an element is routed to an output, heartbeats will be send to all other outputs")
	public void setSendingHeartbeats(boolean sendingHeartbeats)
	{
		this.sendingHeartbeats = sendingHeartbeats;
	}
	
	public boolean isSendingHeartbeats()
	{
		return this.sendingHeartbeats;
	}
	
	@Parameter(name="table",aliasname = "table", type = StringParameter.class, isList = false, optional = false, doc = "table name to load model from.")
	public void setTable(String table)
	{
		this.table = table;
	}
	
	public String getTable()
	{
		return this.table;
	}
	
	@Parameter(name="username",aliasname = "username",type = StringParameter.class, isList = false, optional = false, doc = "username to access table from the database")
	public void setUsername(String username)
	{
		this.username = username;
	}
	
	public String getUsername()
	{
		return this.username;
	}
	
	@Parameter(name="password",aliasname = "password",type = StringParameter.class, isList = false, optional = false, doc = "password to access model table")
	public void setPassword(String password)
	{
		this.password = password;
	}
	
	public String getPassword()
	{
		return this.password;
	}
	
	@Parameter(name="selectModelByValue",aliasname = "selectModelByValue", type = StringParameter.class, isList = false, optional = false, doc = "column name to fetch model from")
	public void setSelectModelByValue(String selectModelByValue)
	{
		this.selectModelByValue = selectModelByValue;
	}
	
	public String getSelectModelByValue()
	{
		return this.selectModelByValue;
	}
	
	@Parameter(name="selectModelByColumn" ,aliasname = "selectModelByColumn", type = StringParameter.class, isList = false, optional = false, doc = "column name to fetch model from")
	public void setSelectModelByColumn(String selectModelByColumn)
	{
		this.selectModelByColumn = selectModelByColumn;
	}
	
	public String getSelectModelByColumn()
	{
		return this.selectModelByColumn;
	}
	
	@Parameter(name="host" ,aliasname = "host", type = StringParameter.class, isList = false, optional = false, doc = "database host")
	public void setHost(String host)
	{
		this.host = host;
	}
	
	public String getHost()
	{
		return host;
	}
	
	@Parameter(name="port" ,aliasname = "port", type = StringParameter.class, isList = false, optional = false, doc = "database port")
	public void setPort(String port)
	{
		this.port = port;
	}
	
	public String getPort()
	{
		return port;
	}
	
	@Parameter(name="database" ,aliasname = "database", type = StringParameter.class, isList = false, optional = false, doc = "database name")
	public void setDatabase(String database)
	{
		this.database = database;
	}
	
	public String getDatabase()
	{
		return database;
	}
	
	@Parameter(name="rpcServer" ,aliasname = "rpcServer", type = StringParameter.class, isList = false, optional = false, doc = "rpc server host and port in the format host:port")
	public void setRpcServer(String rpcServer)
	{
		this.rpcServer = rpcServer;
	}
	
	public String getRpcServer()
	{
		return rpcServer;
	}
}