from vision_sprayer.scenarios.simulation import SimulationScenario


def test_orchestrator_runs_complete_fake_pipeline() -> None:
    orchestrator = SimulationScenario(width=320, height=240).build_pipeline()

    snapshot = orchestrator.tick(now=1.0, dt=0.016)

    assert snapshot.frame.sequence == 1
    assert snapshot.detection is not None
    assert snapshot.track is not None
    assert snapshot.command.aim_point is not None
    assert snapshot.metrics.frame_age_ms >= 0
    assert snapshot.metrics.loop_latency_ms >= 0


def test_orchestrator_preserves_state_across_ticks() -> None:
    orchestrator = SimulationScenario(width=320, height=240).build_pipeline()

    first = orchestrator.tick(now=1.0, dt=0.016)
    second = orchestrator.tick(now=1.1, dt=0.1)

    assert first.frame.sequence == 1
    assert second.frame.sequence == 2
    assert second.track is not None
    assert second.track.age_frames == 2
