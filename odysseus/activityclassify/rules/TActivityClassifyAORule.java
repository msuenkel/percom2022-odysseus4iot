package activityclassify.rules;

import activityclassify.logicaloperator.ActivityClassifyAO;
import activityclassify.physicaloperator.ActivityClassifyPO;
import de.uniol.inf.is.odysseus.core.server.planmanagement.TransformationConfiguration;
import de.uniol.inf.is.odysseus.ruleengine.rule.RuleException;
import de.uniol.inf.is.odysseus.ruleengine.ruleflow.IRuleFlowGroup;
import de.uniol.inf.is.odysseus.transform.flow.TransformRuleFlowGroup;
import de.uniol.inf.is.odysseus.transform.rule.AbstractTransformationRule;

public class TActivityClassifyAORule extends AbstractTransformationRule<ActivityClassifyAO>
{
	@Override
	public int getPriority()
	{
		return 0;
	}

	@Override
	public void execute(ActivityClassifyAO activityClassifyAO, TransformationConfiguration config) throws RuleException
	{
		defaultExecute(activityClassifyAO, new ActivityClassifyPO(activityClassifyAO), config, true, true);
	}

	@Override
	public boolean isExecutable(ActivityClassifyAO operator, TransformationConfiguration transformConfig)
	{
		return operator.isAllPhysicalInputSet();
	}

	@Override
	public String getName()
	{
		return "ActivityClassifyAO -> ActivityClassifyPO";
	}

	@Override
	public IRuleFlowGroup getRuleFlowGroup()
	{
		return TransformRuleFlowGroup.TRANSFORMATION;
	}

	@Override
	public Class<? super ActivityClassifyAO> getConditionClass()
	{	
		return ActivityClassifyAO.class;
	}
}