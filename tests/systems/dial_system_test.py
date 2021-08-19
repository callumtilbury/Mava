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

"""Tests for Dial."""

import functools

import launchpad as lp
import sonnet as snt

import mava
from mava.systems.tf import dial
from mava.utils import lp_utils
from mava.utils.enums import ArchitectureType
from mava.utils.environments import debugging_utils


class TestDial:
    """Simple integration/smoke test for dial."""

    def test_recurrent_dial_on_debugging_env(self) -> None:
        """Test recurrent dial."""
        # environment
        environment_factory = functools.partial(
            debugging_utils.make_environment,
            env_name="simple_spread",
            action_space="discrete",
        )

        # networks
        network_factory = lp_utils.partial_kwargs(
            dial.make_default_networks,
            archecture_type=ArchitectureType.recurrent,
        )

        # system
        system = dial.DIAL(
            environment_factory=environment_factory,
            network_factory=network_factory,
            num_executors=1,
            min_replay_size=16,
            max_replay_size=1000,
            batch_size=16,
            optimizer=snt.optimizers.Adam(learning_rate=1e-3),
            checkpoint=False,
            sequence_length=3,
            period=3,
        )

        program = system.build()

        (trainer_node,) = program.groups["trainer"]
        trainer_node.disable_run()

        # Launch gpu config - don't use gpu
        local_resources = lp_utils.cpu_only(program.groups.keys())
        lp.launch(
            program,
            launch_type="test_mt",
            local_resources=local_resources,
        )

        trainer: mava.Trainer = trainer_node.create_handle().dereference()

        for _ in range(2):
            trainer.step()
