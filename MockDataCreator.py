import itertools
import string
import random
from typing import Any, Iterable, List

class MockDataCreator:

    def batcher(iterable: Iterable[Any], batch_size: int) -> Iterable[List[Any]]:
        it = iter(iterable)
        while True:
            batch = list(itertools.islice(it, batch_size))
            if not batch:
                break
            yield batch

    def take_n(generator: Iterable[Any], n: int) -> Iterable[Any]:
        return itertools.islice(generator, n)



    def create_metadata():
        available_attributes = {
            "Attribute1" : ["value1", "value2", "value3"],
            "Attribute2" : ["something1", "something2"],
            "Attribute3" : ["3v", "4v"],
            "Build4" : ["B1", "B2", "B3", "B4", "B5", "B6", "B7"],
            "Type5" : ["T1", "T2", "T3"],
            "S" : ["S1", "S2", "S3", "S4", "S5"],
            "V" : ["V1", "V2"],
            "G" : ["G1", "G2", "G3", "G4", "G5", "G6", "G7"],
            "Unmanaged":[],
            "Unmanaged2":[],
            "Unmanaged3":[],
            "BuildType" : ["Big", "Small", "Grande", "Tiny"]
            }
        
        attributes = list(available_attributes.keys())

        while True:    
            metadata = {}
            selected_attributes = random.sample(attributes, k=random.randint(7, 12))
            for key in selected_attributes:
                if available_attributes[key]:
                    metadata[key] = random.choice(available_attributes[key])
                else:
                    metadata[key] = "".join(random.choices(string.ascii_letters, k=6))
            yield metadata




    