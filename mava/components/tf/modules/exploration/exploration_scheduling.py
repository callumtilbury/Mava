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
class LinearExplorationScheduler:
    def __init__(self, epsilon_min: float = 0.05, epsilon_decay: float = 1e-4):
        """
        Decays epsilon linearly to epsilon_min.
        """
        self._epsilon_min = epsilon_min
        self._epsilon_decay = epsilon_decay
        self._epsilon = 1.0

    def decrement_epsilon(self) -> None:
        if self._epsilon == self._epsilon_min:
            return

        self._epsilon -= self._epsilon_decay
        if self._epsilon < self._epsilon_min:
            self._epsilon = self._epsilon_min

    def get_epsilon(self) -> float:
        return self._epsilon

    def reset_epsilon(self) -> None:
        self._epsilon = 1.0


class ExponentialExplorationScheduler(LinearExplorationScheduler):
    def __init__(self, epsilon_min: float = 0.05, epsilon_decay: float = 1e-4):
        """
        Decays epsilon exponentially to epsilon_min.
        """
        super(ExponentialExplorationScheduler, self).__init__(
            epsilon_min,
            epsilon_decay,
        )

    def decrement_epsilon(self) -> None:
        if self._epsilon == self._epsilon_min:
            return
        elif self._epsilon < self._epsilon_min:
            # Should only ever happen once.
            self._epsilon = self._epsilon_min
            return
        self._epsilon *= 1 - self._epsilon_decay
