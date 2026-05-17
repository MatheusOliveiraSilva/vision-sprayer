from vision_sprayer.adapters.actuator.fake_actuator import FakeActuator
from vision_sprayer.domain.models import Point
from vision_sprayer.observability.metrics import MetricsCollector
from vision_sprayer.targeting.targeting_policy import TargetingPolicy
from vision_sprayer.tracking.target_tracker import TargetTracker


def build_tracker() -> TargetTracker:
    return TargetTracker()


def build_targeting_policy(initial_width: int, initial_height: int) -> TargetingPolicy:
    return TargetingPolicy(initial_aim=Point(initial_width / 2, initial_height / 2))


def build_fake_actuator() -> FakeActuator:
    return FakeActuator()


def build_metrics_collector() -> MetricsCollector:
    return MetricsCollector()

