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

"""Jax MAPPO system trainer."""

from mava.components.jax import training
from mava.specs import DesignSpec

TRAINER_SPEC = DesignSpec(
    initial_state_fn=training.InitialState,
    gae_fn=training.GAE,
    loss=training.MAPGWithTrustRegionClippingLoss,
    epoch_update=training.MAPGEpochUpdate,
    minibatch_update=training.MAPGMinibatchUpdate,
    sgd_step=training.MAPGWithTrustRegionStep,
    step=training.DefaultStep,
)
