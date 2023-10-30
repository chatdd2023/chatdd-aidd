import argparse
from dotenv import load_dotenv
import os

'''
  功能：工程初始化相关参数设置
  author:boge
  date:2023-11-26
'''
#解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument("--http_port", "-http_port", type=int, default=8900, nargs="?", help="http_port",required=False)
parser.add_argument("--num_process", "-num_process", type=int, default=1, nargs="?", help="num_process",required=False)
parser.add_argument("--env", "-env", type=str, default="dev", nargs="?", help="env",required=False)
args=parser.parse_args()

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)

match args.env:
    case "prod":
         load_dotenv(grandparent_dir+"/conf/prod.env")
    case "pre":
         load_dotenv(grandparent_dir+"/conf/pre.env")
    case _:
         load_dotenv(grandparent_dir+"/conf/dev.env")


