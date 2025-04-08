import os
import sys
import argparse
from Framework_Core.utils.fileUtils import FileUtils
from Framework_Core.utils.logger import test_logger

def main():
    parser = argparse.ArgumentParser(description='将YAML测试用例转换为pytest测试用例')
    parser.add_argument('yaml_path', help='YAML文件路径')
    parser.add_argument('--output', '-o', help='输出目录路径（可选）')
    
    args = parser.parse_args()
    
    try:
        # 检查YAML文件是否存在
        if not os.path.exists(args.yaml_path):
            test_logger.error(f"YAML文件不存在: {args.yaml_path}")
            sys.exit(1)
            
        # 创建FileUtils实例
        file_utils = FileUtils()
        
        # 如果指定了输出目录，则修改输出路径
        if args.output:
            file_utils.test_case_dir = args.output
            if not os.path.exists(args.output):
                os.makedirs(args.output)
        
        # 生成测试文件
        test_file_path = file_utils.generate_test_file(args.yaml_path)
        test_logger.info(f"测试用例文件已生成: {test_file_path}")
        
    except Exception as e:
        test_logger.error(f"转换失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 