package activityclassify.physicaloperator;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.json.JSONException;
import org.json.JSONObject;

import activityclassify.logicaloperator.ActivityClassifyAO;
import de.uniol.inf.is.odysseus.core.collection.Tuple;
import de.uniol.inf.is.odysseus.core.metadata.IMetaAttribute;
import de.uniol.inf.is.odysseus.core.metadata.IStreamObject;
import de.uniol.inf.is.odysseus.core.physicaloperator.IPhysicalOperator;
import de.uniol.inf.is.odysseus.core.physicaloperator.IPunctuation;
import de.uniol.inf.is.odysseus.core.predicate.IPredicate;
import de.uniol.inf.is.odysseus.core.sdf.schema.SDFAttribute;
import de.uniol.inf.is.odysseus.core.sdf.schema.SDFSchema;
import de.uniol.inf.is.odysseus.core.server.physicaloperator.AbstractPipe;
import de.uniol.inf.is.odysseus.core.server.physicaloperator.IHasPredicates;

public class ActivityClassifyPO<T extends IStreamObject<IMetaAttribute>> extends AbstractPipe<T, T> implements IHasPredicates
{
	final boolean overlappingPredicates;
	final boolean sendingHeartbeats;
	private List<IPredicate<?>> predicates;
	private String username;
	private String password;
	private String table;
	private String selectModelByColumn;
	private String selectModelByValue;
	private String rpcServerString;
	private String database;
	private String port;
	private String host;
	private String metaValues;

	public ActivityClassifyPO(ActivityClassifyAO activityClassifyAO)
	{
		super();
		this.overlappingPredicates = activityClassifyAO.isOverlappingPredicates();
		this.sendingHeartbeats = activityClassifyAO.isSendingHeartbeats();
		this.table = activityClassifyAO.getTable();
		this.username = activityClassifyAO.getUsername();
		this.host = activityClassifyAO.getHost();
		this.port= activityClassifyAO.getPort();
		this.database = activityClassifyAO.getDatabase();
		this.password = activityClassifyAO.getPassword();
		this.rpcServerString = activityClassifyAO.getRpcServer();
		this.selectModelByColumn = activityClassifyAO.getSelectModelByColumn();
		this.selectModelByValue = activityClassifyAO.getSelectModelByValue();
		initPredicates(activityClassifyAO.getPredicates());
	}

	@Override
	public List<IPredicate<?>> getPredicates()
	{
		return predicates;
	}

	private void initPredicates(List<IPredicate<?>> predicates)
	{
		this.predicates = new ArrayList<IPredicate<?>>(predicates.size());
		
		for (IPredicate<?> p : predicates)
		{
			this.predicates.add(p.clone());
		}
	}

	@Override
	public OutputMode getOutputMode()
	{
		return OutputMode.NEW_ELEMENT;
	}

	@Override
	protected void process_next(T object, int port)
	{
		Tuple res = (Tuple) object;
		final Tuple output = new Tuple(this.getOutputSchema(port).getAttributes().size(), false);
		JSONObject dbProperties = new JSONObject();
		JSONObject sensorDataJson = new JSONObject();
		SDFSchema inputSchema = this.getInputSchema(port);
		output.setAttribute(0, res.getAttribute(0)); //output.setAttributes(res); <- BY OORMILA
		
		SDFAttribute elem = null;
		for(int index = 0; index < inputSchema.getAttributes().size(); index++)
		{
			elem = inputSchema.get(index);
			String name = elem.getAttributeName();
			Object attrValue = res.getAttribute(inputSchema.findAttributeIndex(name));
			try
			{
				if(attrValue.toString().equalsIgnoreCase("NaN"))
				{
					attrValue=0;
				}
				
				sensorDataJson.put(String.format("%03d_%s", index, name), attrValue);
			}
			catch(JSONException e)
			{
				e.printStackTrace();
			}
		}

		try
		{
			dbProperties.put("selectModelByColumn", this.selectModelByColumn);
			dbProperties.put("selectModelByValue", this.selectModelByValue);
			dbProperties.put("table", this.table);
			dbProperties.put("host", this.host);
			dbProperties.put("port", this.port);
			dbProperties.put("database", this.database);
			dbProperties.put("username", this.username);
			dbProperties.put("password", this.password);
		}
		catch (JSONException e)
		{
			e.printStackTrace();
		}

		new Thread(() ->
		{
			try
			{
				XmlRpcClientConfigImpl cf = new XmlRpcClientConfigImpl();
				cf.setServerURL(new URL("http://"+this.rpcServerString+"/rpc"));
				System.out.println("accessing rpc at url : "+cf.getServerURL());
				cf.setConnectionTimeout(10000);
				XmlRpcClient client = new XmlRpcClient();
				client.setConfig(cf);
				Vector<String> params = new Vector<>();
				params.add(dbProperties.toString());
				params.add(sensorDataJson.toString());
				Object result = client.execute("predict", params);
				
				String classificationResult = ((String) result);
				System.out.println("The activity is: "+ classificationResult);
				output.setAttribute(this.getOutputSchema().findAttributeIndex("activity"), classificationResult);
				metaValues=res.getMetadata().toString();
				System.out.println(metaValues);
				
				output.setMetadata(res.getMetadata().clone());
				transfer((T) output);
			}
			catch (Exception exception)
			{
				System.err.println("JavaClient: " + exception);
			}
		}).start();
	}

	@Override
	public void processPunctuation(IPunctuation punctuation, int port)
	{
		for (int i = 0; i < predicates.size(); i++)
		{
			sendPunctuation(punctuation, i);
		}
	}

	@Override
	public boolean process_isSemanticallyEqual(IPhysicalOperator ipo)
	{
		if (!(ipo instanceof ActivityClassifyPO))
		{
			return false;
		}
		
		ActivityClassifyPO spo = (ActivityClassifyPO) ipo;
		
		if(this.predicates.size() == spo.predicates.size())
		{
			for(int i = 0; i < this.predicates.size(); i++)
			{
				if(!this.predicates.get(i).equals(spo.predicates.get(i)))
				{
					return false;
				}
			}
			
			return true;
		}
		
		return false;
	}

	@Override
	public void setPredicates(List<IPredicate<?>> predicates)
	{
		this.predicates = predicates;
	}
}