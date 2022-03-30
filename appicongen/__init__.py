import argparse

def main():
    parser = argparse.ArgumentParser(description='Tool for generating macOS/iOS app icons')
    parser.add_argument('--macos', action='store_true', help='Generate macOS icons')
    parser.add_argument('--ios', action='store_true', help='Generate iOS icons')
    parser.add_argument('--ipados', action='store_true', help='Generate iPadOS icons')
    parser.add_argument('--watchos', action='store_true', help='Generate watchOS icons')

    args = parser.parse_args()
    print("Hello")
