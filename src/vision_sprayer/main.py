from vision_sprayer.config import CONFIG
from vision_sprayer.scenarios.camera import CameraScenario


def main() -> None:
    CameraScenario(config=CONFIG).run()


if __name__ == "__main__":
    main()
