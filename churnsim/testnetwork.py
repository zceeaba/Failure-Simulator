import networkx as nx

number_of_nodes = 10
G = nx.complete_graph(number_of_nodes)

print(G.nodes)

import random
from nxsim import BaseNetworkAgent

class ZombieOutbreak(BaseNetworkAgent):
    def __init__(self, environment=None, agent_id=0, state=()):
        super().__init__(environment=environment, agent_id=agent_id, state=state)
        self.bite_prob = 0.05

    def run(self):
        while True:
            if self.state['id'] == 1:
                self.zombify()
                print("zombify happens here")
                yield self.env.timeout(1)
            else:
                yield self.env.event()


    def zombify(self):
        normal_neighbors = self.get_neighboring_agents(state_id=0)
        for neighbor in normal_neighbors:
            if random.random() < self.bite_prob:
                neighbor.state['id'] = 1 # zombie
                print(self.env.now, self.id, neighbor.id, sep='\t')
                break


from nxsim import NetworkSimulation

# Initialize agent states. Let's assume everyone is normal.
init_states = [{'id': 0, } for _ in range(number_of_nodes)]  # add keys as as necessary, but "id" must always refer to that state category
print(init_states)
# Seed a zombie
init_states[5] = {'id': 1}

sim = NetworkSimulation(topology=G, states=init_states, agent_type=ZombieOutbreak,
                        max_time=30, num_trials=1, logging_interval=1.0)

sim.run_simulation()
