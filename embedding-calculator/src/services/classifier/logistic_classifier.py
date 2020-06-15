#  Copyright (c) 2020 the original author or authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

from typing import Dict, List

import attr
import numpy as np
from sklearn.linear_model import LogisticRegression

from src.services.dto.face_prediction import NamePrediction
from src.services.imgtools.types import Array1D


@attr.s(auto_attribs=True, frozen=True)
class LogisticClassifier:
    CURRENT_VERSION = "LogisticClassifier_v0"

    model: LogisticRegression
    class_2_face_name: Dict[int, str]
    emb_calc_version: str
    version: str = CURRENT_VERSION

    @classmethod
    def train(cls, embeddings: List[Array1D], names: List[str], emb_calc_version: str) -> 'LogisticClassifier':
        assert len(embeddings) == len(names)
        model = LogisticRegression(C=100000, solver='lbfgs', multi_class='multinomial')
        labels = list(range(len(names)))
        model.fit(X=embeddings, y=labels)
        class_2_face_name = {cls: name for cls, name in zip(labels, names)}
        return LogisticClassifier(model, class_2_face_name, emb_calc_version)

    def predict(self, embedding: Array1D, emb_calc_version: str) -> NamePrediction:
        assert self.emb_calc_version == emb_calc_version
        probabilities = self.model.predict_proba([embedding])[0]
        top_class = np.argsort(-probabilities)[0]
        face_name = self.class_2_face_name[top_class]
        probability = probabilities[top_class]
        return NamePrediction(face_name, probability)


class LogisticClassifierMock(LogisticClassifier):
    def __init__(self):
        pass  # Mock init

    @classmethod
    def train(cls, embeddings, names, emb_calc_version):
        return LogisticClassifier(None, {}, emb_calc_version)

    def predict(self, embedding: Array1D, emb_calc_version: str) -> NamePrediction:
        return NamePrediction('MockPrediction', 0)
