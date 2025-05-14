import json
import sys
from msgpack.packer import Packer
from msgpack.unpacker import Unpacker


def json_to_msgpack(json_str):
    data = json.loads(json_str)
    return Packer().pack(data)


def msgpack_to_json(msgpack_data):
    data = Unpacker(msgpack_data).unpack()
    return json.dumps(data)


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ['-e', '-d']:
        print("Usage:")
        print("\nFor Windows PowerShell:")
        print("  Encode JSON to MessagePack:")
        print('    python main.py -e \'{\\"name\\": \\"John\\", \\"age\\": 30}\'')
        print("  Decode MessagePack to JSON:")
        print("    python main.py -d 82a46e616d65a44a6f686ea36167651e")
        return

    mode = sys.argv[1]
    input_data = sys.argv[2]

    try:
        if mode == '-e':
            result = json_to_msgpack(input_data)
            print(result.hex())
        else:
            msgpack_data = bytes.fromhex(input_data)
            result = msgpack_to_json(msgpack_data)
            print(result)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {str(e)}")
    except ValueError as e:
        print(f"Error: Invalid input data - {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
