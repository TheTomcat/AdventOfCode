from typing import Generator, List, Any, Tuple
from collections import namedtuple
import enum, math
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2021,16)

Packet = namedtuple("Packet",['ver','id','literal','sub_packets', 'bitlength'])

class TypeID(enum.Enum):
    ADD = 0
    MUL = 1
    MIN = 2
    MAX = 3
    LIT = 4
    GRT = 5
    LST = 6
    EQT = 7

def parse(data: List[str]) -> Generator:
    for char in data[0]:
        yield from format(int(char, base=16), "04b")

def pull(stream: Generator, n: int, as_generator=False) -> int:
    o = [0]*n
    for i in range(n):
        try:
            o[i] = next(stream)
        except StopIteration:
            break
    ret = int(''.join(str(i) for i in o), base=2)
    return ret

def decode_packet(stream:Generator) -> Packet:
    bits=0
    version = pull(stream, 3)
    bits += 3
    id = pull(stream, 3)
    bits += 3
    if TypeID(id) == TypeID.LIT:
        c = 1
        literal = 0
        while c:
            c = pull(stream, 1)
            literal = (literal << 4) + pull(stream, 4)
            bits += 5
        p= Packet(ver=version, id=id, literal=literal, sub_packets=[], bitlength=bits)
        return p
    if TypeID(id) != TypeID.LIT:
        type_id = pull(stream, 1)
        bits += 1
        subpack = []
        if type_id == 0:
            subpacklen = pull(stream, 15)
            bits += 15 + subpacklen
            length=0
            while length < subpacklen:
                packet = decode_packet(stream)
                length += packet.bitlength
                subpack.append(packet)
        else:
            num_sub_packs = pull(stream, 11)
            bits += 11
            for _ in range(num_sub_packs):
                packet = decode_packet(stream)
                subpack.append(packet)
                bits += packet.bitlength
        p = Packet(ver=version, id=id, literal=None, sub_packets=subpack, bitlength=bits)
        return p

def calculate_version_sum(packet:Packet) -> int:
    ver = packet.ver
    return ver + sum(calculate_version_sum(p) for p in packet.sub_packets)

def evaluate_packet(packet:Packet) -> int:
    # print(packet)
    match TypeID(packet.id):
        case TypeID.ADD:
            return op_add(packet.sub_packets)
        case TypeID.MUL:
            return op_mul(packet.sub_packets)
        case TypeID.MIN:
            return op_min(packet.sub_packets)
        case TypeID.MAX:
            return op_max(packet.sub_packets)
        case TypeID.LIT:
            return packet.literal
        case TypeID.GRT:
            return op_grt(packet.sub_packets)
        case TypeID.LST:
            return op_lst(packet.sub_packets)
        case TypeID.EQT:
            return op_eqt(packet.sub_packets)
    
def op_add(subpackets: List[Packet]) -> int:
    return sum(evaluate_packet(packet) for packet in subpackets)

def op_mul(subpackets: List[Packet]) -> int:
    return math.prod(evaluate_packet(packet) for packet in subpackets)

def op_min(subpackets: List[Packet]) -> int:
    return min(evaluate_packet(packet) for packet in subpackets)

def op_max(subpackets: List[Packet]) -> int:
    return max(evaluate_packet(packet) for packet in subpackets)

def op_grt(subpackets: List[Packet]) -> int:
    return int(evaluate_packet(subpackets[0]) > evaluate_packet(subpackets[1]))

def op_lst(subpackets: List[Packet]) -> int:
    return int(evaluate_packet(subpackets[0]) < evaluate_packet(subpackets[1]))

def op_eqt(subpackets: List[Packet]) -> int:
    return int(evaluate_packet(subpackets[0]) == evaluate_packet(subpackets[1]))

@solution_timer(2021,16,1)
def part_one(data: List[str], verbose=False):
    bits = parse(data)
    return calculate_version_sum(decode_packet(bits))


@solution_timer(2021,16,2)
def part_two(data: List[str], verbose=False):
    bits = parse(data)
    packet = decode_packet(bits)
    return evaluate_packet(packet)

if __name__ == "__main__":
    data = read_entire_input(2021,16)
    part_one(data)
    part_two(data)


test = {
    'C200B40A82':3,
    '04005AC33890':54,
    '880086C3E88112':7,
    'CE00C43D881120':9,
    'D8005AC2A8F0':1,
    'F600BC2D8F':0,
    '9C005AC2F8F0':0,
    '9C0141080250320F1802104A08':1
}
def run_tests():
    for str, answer in test.items():
        print(f'{evaluate_packet(decode_packet(parse([str])))}=={answer}')