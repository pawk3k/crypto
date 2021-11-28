// # X/N  !== 0  wzglednie pierwsze
// # 4 testy losowosci 20 000
// # test1
// # n(1) - liczba 1
// # test2
// # 11100011
// # dlugosc serii 111 = 3

// # test3
// # czy istnieje seria 26 lub wiecej

// # test4
// # test pokerowy

const gcd = (a, b) => {
  if (b === 0) return a;
  return gcd(b, a % b);
};

const getX = (n) => {
  while (true) {
    let x = Math.floor(Math.random() * n);
    if (gcd(n, x) === 1) return x;
  }
};

const blumgenerator = () => {
  const p = 102871;
  const q = 61583;
  const n = p * q;
  const x = 102329478;

  const x0 = (x * x) % n;
  const array = new Array(3).fill(0);
  const getLastBit = (prevX) => {
    return prevX.toString(2)[prevX.toString(2).length - 1];
  };

  array[0] = { currentX: x0, result: getLastBit(x0) };

  const getNextX = (prevX) => (prevX * prevX) % n;

  for (let i = 1; i < 20000; i += 1) {
    const currentX = getNextX(array[i - 1].currentX);
    array[i] = { currentX, result: getLastBit(currentX) };
  }

  array;
  const result = array.reduce((acc, curr) => curr.result + acc, '');

  return Array.from(result);
};

const blumStream = blumgenerator();

const series = blumStream
  .toString()
  .split('0')
  .map((item) => item.split(',').join(''))
  .map((el) => el.length - 1)
  .filter((el) => el >= 0)
  .reduce(
    (prev, curr) => ({ ...prev, [curr + 1]: (prev[curr + 1] || 0) + 1 }),
    {}
  );

test('test serii', () => {
  const moreThanSix = Object.entries(series)
    .filter((item) => Number(item[0]) > 5)
    .reduce((prev, curr) =>
      //@ts-ignore
      typeof prev == 'object' ? prev[1] + curr[1] : prev + curr[1]
    );

  expect(series[1]).toBeGreaterThan(2315);
  expect(series[1]).toBeLessThan(2685);

  expect(series[2]).toBeGreaterThan(1114);
  expect(series[2]).toBeLessThan(1386);

  expect(series[3]).toBeGreaterThan(527);
  expect(series[3]).toBeLessThan(723);

  expect(series[4]).toBeGreaterThan(240);
  expect(series[4]).toBeLessThan(384);

  expect(series[5]).toBeGreaterThan(103);
  expect(series[5]).toBeLessThan(209);

  expect(moreThanSix).toBeGreaterThan(103);
  expect(moreThanSix).toBeLessThan(209);
});

test('test pojedynczych bitów', () => {
  const numberOfOnes = blumStream.reduce(
    (acc, curr) => Number(acc) + Number(curr)
  );
  expect(numberOfOnes).toBeGreaterThan(9725);
  expect(numberOfOnes).toBeLessThan(10275);
});

test('test dlugiej serii', () => {
  expect('26' in series).toBeFalsy();
});

test('pokerowy', () => {
  const strM = blumStream.join('');
  const chunk = (arr, size) =>
    [...Array(Math.ceil(arr.length / size))].map((_, i) =>
      arr.slice(size * i, size + size * i)
    );

  const numbers = chunk(strM, 4)
    .map((binNumber) => parseInt(String(binNumber), 2))
    .reduce((prev, curr) => ({ ...prev, [curr]: (prev[curr] || 0) + 1 }), {});

  const x =
    (16 / 5000) *
      Object.values(numbers)
        .map((number) => +number * +number)
        .reduce((prev, curr) => prev + curr) -
    5000;
  expect(x).toBeGreaterThan(2.16);
  expect(x).toBeLessThan(46.17);
});
