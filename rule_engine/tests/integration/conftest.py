import pytest
from proto.messages_pb2 import Batch, GpuInfo
import time

@pytest.fixture
def fixed_batch():
    gpu_id = 12
    gpu_info = GpuInfo(
        gpu_id=gpu_id,
        model="RTX 3090",
        max_ker_temp=int(60.0),
        max_mem_temp=int(115.0),
    )

    batch = Batch(
        gpu_info=gpu_info,
        ker_temp=90.0,
        ker_load=60.0,
        mem_temp=80.0,
        mem_load=66.33,
        timestamp=str(time.time()),
    )
    return batch


@pytest.fixture
def make_batch():
    def _make_batch(gpu_id: int):
        gpu_info = GpuInfo(
            gpu_id=gpu_id,
            model="RTX 3090",
            max_ker_temp=int(60.0),
            max_mem_temp=int(115.0),
        )

        batch = Batch(
            gpu_info=gpu_info,
            ker_temp=90.0,
            ker_load=60.0,
            mem_temp=80.0,
            mem_load=66.33,
            timestamp=str(time.time()),
        )
        return batch
    return _make_batch