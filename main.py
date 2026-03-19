import argparse
import sys
from src.engines.engine_volc import VolcEngine
from src.engines.engine_auth_gen import PollinationsEngine
from src.tools.tool_status_monitor import PollinationsMonitor

def main():
    parser = argparse.ArgumentParser(description="AutoStory-Alpha CLI 生产工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # Status command
    status_parser = subparsers.add_parser("status", help="检查账户状态")

    # Generate command
    gen_parser = subparsers.add_parser("gen", help="生成图片")
    gen_parser.add_argument("--engine", choices=["volc", "poll"], required=True, help="选择生图引擎")
    gen_parser.add_argument("--prompt", required=True, help="提示词内容")
    gen_parser.add_argument("--name", required=True, help="保存文件名")

    args = parser.parse_args()

    if args.command == "status":
        monitor = PollinationsMonitor()
        monitor.get_status()
    elif args.command == "gen":
        if args.engine == "volc":
            engine = VolcEngine()
            engine.generate_image(args.prompt, args.name)
        elif args.engine == "poll":
            engine = PollinationsEngine()
            engine.generate_image(args.prompt, args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
