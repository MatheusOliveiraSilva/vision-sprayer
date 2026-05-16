import argparse

from vision_sprayer.pipeline.factories import create_camera_pipeline, create_sim_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the vision sprayer realtime pipeline.")
    subparsers = parser.add_subparsers(dest="command")

    sim_parser = subparsers.add_parser("sim", help="Run the simulated target pipeline.")
    sim_parser.add_argument(
        "--smoke-frames",
        type=int,
        default=0,
        help="Exit after rendering this many frames. Useful for automated smoke checks.",
    )

    camera_parser = subparsers.add_parser("camera", help="Run camera + YOLO bottle detection.")
    camera_parser.add_argument("--source", type=int, default=0, help="OpenCV camera source index.")
    camera_parser.add_argument("--model", default="yolo11n.pt", help="YOLO model path or name.")
    camera_parser.add_argument("--target", default="bottle", help="YOLO class name to track.")
    camera_parser.add_argument("--confidence", type=float, default=0.25, help="Detection confidence threshold.")
    camera_parser.add_argument("--device", default=None, help="Ultralytics device, for example cpu, mps, or 0.")
    camera_parser.add_argument("--width", type=int, default=None, help="Requested camera width.")
    camera_parser.add_argument("--height", type=int, default=None, help="Requested camera height.")
    camera_parser.add_argument("--no-window", action="store_true", help="Run camera pipeline without opening a window.")
    camera_parser.add_argument(
        "--smoke-frames",
        type=int,
        default=0,
        help="Exit after rendering this many frames. Useful for automated smoke checks.",
    )

    cameras_parser = subparsers.add_parser("cameras", help="List available OpenCV camera source indices.")
    cameras_parser.add_argument("--max-sources", type=int, default=1, help="Number of source indices to probe.")

    parser.add_argument(
        "--smoke-frames",
        type=int,
        default=0,
        help="Backwards-compatible smoke frame count for the default sim command.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    command = args.command or "sim"
    if command == "cameras":
        # Local import keeps OpenCV's native runtime out of visual commands.
        from vision_sprayer.adapters.camera.opencv_camera_source import list_camera_sources

        sources = list_camera_sources(max_sources=args.max_sources)
        print("Available camera sources:", ", ".join(str(source) for source in sources) or "none")
        return

    width, height = 960, 540
    pipeline = create_pipeline(args=args, command=command, width=width, height=height)
    if command == "camera":
        # Local import keeps OpenCV display runtime out of sim commands.
        from vision_sprayer.app.opencv_runner import run_opencv_pipeline

        run_opencv_pipeline(
            pipeline=pipeline,
            title="Vision Sprayer camera",
            smoke_frames=args.smoke_frames,
            display=not args.no_window,
        )
        return

    # Local import keeps Pygame's SDL runtime out of camera commands.
    from vision_sprayer.app.pygame_runner import run_pygame_pipeline

    run_pygame_pipeline(pipeline=pipeline, title="Vision Sprayer sim", smoke_frames=args.smoke_frames)


def create_pipeline(args: argparse.Namespace, command: str, width: int, height: int):
    if command == "camera":
        return create_camera_pipeline(
            source=args.source,
            model_name=args.model,
            target_class_name=args.target,
            confidence_threshold=args.confidence,
            device=args.device,
            width=args.width,
            height=args.height,
        )
    return create_sim_pipeline(width=width, height=height)


if __name__ == "__main__":
    main()
