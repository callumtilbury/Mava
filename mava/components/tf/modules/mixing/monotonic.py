# python3
# Copyright 2021 InstaDeep Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# TODO (StJohn):
#   - [] Complete class for monotonic mixing

"""Mixing for multi-agent RL systems"""

from typing import Dict

import sonnet as snt
import tensorflow as tf
from acme.tf import utils as tf2_utils

from mava import specs as mava_specs
from mava.components.tf.architectures import BaseArchitecture
from mava.components.tf.modules.mixing import BaseMixingModule
from mava.components.tf.networks.monotonic import MonotonicMixingNetwork


class MonotonicMixing(BaseMixingModule):
    """Multi-agent monotonic mixing architecture.
    This is the component which can be used to add monotonic mixing to an underlying
    agent architecture. It currently supports generalised monotonic mixing using
    hypernetworks (1 or 2 layers) for control of decomposition parameters (QMix)."""

    def __init__(
        self,
        architecture: BaseArchitecture,
        environment_spec: mava_specs.MAEnvironmentSpec,
        qmix_hidden_dim: int = 64,
        num_hypernet_layers: int = 2,
        hypernet_hidden_dim: int = 0,  # Defaults to qmix_hidden_dim
    ) -> None:
        """Initializes the mixer.
        Args:
            architecture: the BaseArchitecture used.
        """
        super(MonotonicMixing, self).__init__()

        self._architecture = architecture
        self._environment_spec = environment_spec
        self._qmix_hidden_dim = qmix_hidden_dim
        self._num_hypernet_layers = num_hypernet_layers
        self._hypernet_hidden_dim = hypernet_hidden_dim

    def _create_mixing_layer(self) -> snt.Module:
        """Modify and return system architecture given mixing structure."""
        state_specs = self._environment_spec.get_extra_specs()
        state_specs = state_specs["s_t"]
        # TODO Currently hard coded to 3 but need to generalise
        # Need to figure out how to get the size of one-hot representation
        # of the global state that is returned by the environment.
        # One hot input dimension of global state
        state_specs = tf.TensorSpec(shape=(3,))

        self._num_agents = len(self._agent_networks)
        q_value_dim = tf.TensorSpec(self._num_agents)

        # Implement method from base class
        self._mixed_network = MonotonicMixingNetwork(
            self._architecture,
            self._agent_networks,
            self._qmix_hidden_dim,
            num_hypernet_layers=self._num_hypernet_layers,
            hypernet_hidden_dim=self._hypernet_hidden_dim,
        )

        tf2_utils.create_variables(self._mixed_network, [q_value_dim, state_specs])
        return self._mixed_network

    def create_system(self) -> Dict[str, Dict[str, snt.Module]]:
        # Implement method from base class
        networks = self._architecture.create_actor_variables()
        self._agent_networks = networks["values"]
        networks["mixing"] = self._create_mixing_layer()
        networks["target_mixing"] = self._create_mixing_layer()
        return networks
