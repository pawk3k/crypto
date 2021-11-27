// # X/N  !== 0  wzglednie pierwsze
// # 4 testy losowosci 20 000
// # test1
// # n(1) - liczba 1
// # test2
// # 11100011
// # dlugosc serii 111 = 3

import { curry } from 'lodash';

// # test3
// # czy istnieje seria 26 lub wiecej

// # test4
// # test pokerowy

const blumgenerator = () => {
  const p = 1823;
  const q = 98011;
  const n = p * q;
  const gcd = (a, b) => {
    if (b === 0) return a;
    return gcd(b, a % b);
  };

  const getX = () => {
    while (true) {
      let x = Math.floor(Math.random() * n);
      if (gcd(n, x) === 1) return x;
    }
  };
  const x = getX();
  const x0 = (x * x) % n;
  // fill array with zeros
  const array = new Array(3).fill(0);
  const getLastBit = (prevX) => {
    return prevX.toString(2)[prevX.toString(2).length - 1];
  };

  array[0] = { currentX: x0, result: getLastBit(x0) };

  const getNextX = (prevX) => (prevX * prevX) % n;

  for (let i = 1; i < 3; i += 1) {
    const currentX = getNextX(array[i - 1].currentX);

    array[i] = { currentX, result: getLastBit(currentX) };
  }

  const result = array.reduce((acc, curr) => curr.result + acc, '');

  return result;
};

blumgenerator();


test('should ', () => {
    
})
