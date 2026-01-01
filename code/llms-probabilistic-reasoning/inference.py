from pgmpy.inference import VariableElimination
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD

# Create the Bayesian Network structure
bn = DiscreteBayesianNetwork([('V0', 'V1'), ('V0', 'V2'), ('V0', 'V3'), ('V1', 'V3')])

# Define CPDs based on the provided tables

# CPD for V0 (root node)
cpd_v0 = TabularCPD(
    variable='V0',
    variable_card=2,
    values=[[0.5072], [0.4928]],
    state_names={'V0': ['s0', 's1']}
)

# CPD for V1 (depends on V0)
cpd_v1 = TabularCPD(
    variable='V1',
    variable_card=2,
    values=[[0.3110, 0.0704],
            [0.6890, 0.9296]],
    evidence=['V0'],
    evidence_card=[2],
    state_names={'V1': ['s0', 's1'], 'V0': ['s0', 's1']}
)

# CPD for V2 (depends on V0)
cpd_v2 = TabularCPD(
    variable='V2',
    variable_card=2,
    values=[[0.8950, 0.0562],
            [0.1050, 0.9438]],
    evidence=['V0'],
    evidence_card=[2],
    state_names={'V2': ['s0', 's1'], 'V0': ['s0', 's1']}
)

# CPD for V3 (depends on V0 and V1)
cpd_v3 = TabularCPD(
    variable='V3',
    variable_card=2,
    values=[[0.0607, 0.8173, 0.8890, 0.2251],
            [0.9393, 0.1827, 0.1110, 0.7749]],
    evidence=['V0', 'V1'],
    evidence_card=[2, 2],
    state_names={'V3': ['s0', 's1'], 'V0': ['s0', 's1'], 'V1': ['s0', 's1']}
)

# Add CPDs to the bn
bn.add_cpds(cpd_v0, cpd_v1, cpd_v2, cpd_v3)

# Validate the bn
assert bn.check_model()

# Create inference object
inference = VariableElimination(bn)

# Compute P(V3=s1 | V1=s0)
query_result = inference.query(variables=['V3'], evidence={'V1': 's0'})
prob_v3_s1_given_v1_s0 = query_result.values[1]  # Index 1 corresponds to V3=s1

print(prob_v3_s1_given_v1_s0)