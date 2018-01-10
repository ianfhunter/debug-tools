import numpy as np
from enum import Enum, auto
import string
import argparse

class ErrorType(Enum):
    COMPLETE_ERROR = auto()
    PARTIAL_ERROR = auto()
    NO_ERROR = auto()

def check_dimension(result, expected, dimension_labels):
    wrong = 0
    leaf_errors = []
    if len(result.shape) > 1:
        for i in range(len(result)):
            err = check_dimension(result[i], expected[i],dimension_labels[1:])
            if err == ErrorType.COMPLETE_ERROR:
                leaf_errors.append(i)
                wrong += 1   
    else:
        for i in range(len(result)):
            global threshold
            if np.abs(result[i] - expected[i]) > threshold:
                leaf_errors.append(i)
                wrong += 1
    if wrong == len(result):
        return ErrorType.COMPLETE_ERROR
    elif wrong > 0:
        print("The dimension", dimension_labels[0], "has errors for elements:", leaf_errors)
        return ErrorType.PARTIAL_ERROR
    else:
        return ErrorType.NO_ERROR
    
#expected = np.ones((123,45,8))
#result = np.ones((123,45,8))
#result = np.random.randint(-1,2,(123,45,8))

#np.save("result.npy", result)
#np.save("expected.npy", expected)

parser = argparse.ArgumentParser(description='Compare 2 Matrices for patterns.')
parser.add_argument('--result', dest='result_path', nargs='?', required=True,
                    help='path to result matrix npy')
parser.add_argument('--expected', dest='expected_path', nargs='?', required=True,
                    help='path to expected matrix npy')
parser.add_argument('--threshold', dest='threshold', nargs='?', required=True,
                    help='absolute delta that will count as a successful comparison.')

args = parser.parse_args()
print(args.result_path)
threshold = int(args.threshold)

result = np.load(args.result_path)
expected = np.load(args.expected_path)

dimensions = len(expected.shape)
dimension_labels = list(string.ascii_uppercase[-dimensions:])

print("Overall Number of Dimensions:",dimensions, dimension_labels,"\n")

check_dimension(result, expected, dimension_labels)

