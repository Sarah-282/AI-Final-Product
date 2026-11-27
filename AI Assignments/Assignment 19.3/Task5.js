"use strict";

function bubbleSort(numbers) {
    const result = numbers.slice();

    for (let end = result.length - 1; end > 0; end--) {
        let swapped = false;
        for (let index = 0; index < end; index++) {
            if (result[index] > result[index + 1]) {
                [result[index], result[index + 1]] = [result[index + 1], result[index]];
                swapped = true;
            }
        }
        if (!swapped) {
            break;
        }
    }

    return result;
}

const testCases = [
    [[5, 1, 4, 2, 8], [1, 2, 4, 5, 8]],
    [[], []],
    [[7], [7]],
    [[3, 3, 1, 2, 1], [1, 1, 2, 3, 3]],
    [[-2, 5, 0, -7], [-7, -2, 0, 5]],
];

for (const [values, expected] of testCases) {
    const result = bubbleSort(values);
    if (JSON.stringify(result) !== JSON.stringify(expected)) {
        throw new Error(`bubbleSort(${JSON.stringify(values)}) returned ${JSON.stringify(result)}`);
    }
    console.log(JSON.stringify(result));
}
