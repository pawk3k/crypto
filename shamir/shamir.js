import {
  atan2,
  chain,
  derivative,
  lsolve,
  lusolve
  e,
  evaluate,
  log,
  pi,
  pow,
  round,
  sqrt,
} from 'mathjs';

const s = 456;

const n = 3;
const k = 1000;

const sum = (array) => array.reduce((prev, curr) => prev + curr, 0);

const trivialCy = (secretNumber, n, k) => {
  const parts = [];
  for (let index = 0; index < n - 1; index++) {
    parts[index] = Math.floor(Math.random() * 1000);
  }
  parts[n - 1] = (secretNumber - sum(parts)) % k;

  parts;
  return parts;
};

const parts = trivialCy(s, n, k);

const trivialDeCy = (arr, k) => sum(arr) % k;

const secret = trivialDeCy(parts, k);

const sh = 944;

const p = 1523;

const a1 = 352;
const a2 = 62;

const splitShamir = () => {
  const der = derivative('x^2', 'x');
  const res = evaluate(['a=3', 'a*a']); // [3, 4, 12]
  res;

  const matrix = [
    [1, 1, 1],
    [1, 3, 9],
    [1, 4, 16],
  ];
  const b = [1368, 1045, 308];
  b;

  const reusult = lsolve(matrix, b);

  console.log(reusult);
};
splitShamir();
console.log(1 % 1503);
