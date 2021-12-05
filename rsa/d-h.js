// diffi-helman key exchange

// pierwiastek pierwotny modulo n
function gcd(a ,b)  {
    if (b === 0) {
        return a;
    }
    return gcd(b, a % b);
}

// Primitive root modulo n
function isCoprime(a ,b)  {
    return gcd(a, b) === 1;
}
// arr.sort((a,b) => a - b)
// arr.filter(i => i < 1000)

// console.dir(arr, {'maxArrayLength':100})

// console.log(n%g)



const isPrimitiveRootModuloN = (n,g) => {
    const arr = [];
    let myPower = 0;
    while(arr.length < n-1) {
        const primitiveRoot = Math.pow(g,myPower) % n; 
        console.log(primitiveRoot);
        if(arr.indexOf(primitiveRoot) === -1) {
            arr.push(primitiveRoot)
        }
        myPower++;
    }
    const sum = arr.reduce((a,b) => a + b) 
    // console.log(arr)
    console.log(sum, 'sum')
    console.log(sum, 'sum2')
    return sum === (n*(n-1))/2;

}

function isPrime(num) {
    if(num < 2) return false;
    for (var i = 2; i < num; i++) {
        if(num%i==0)
            return false;
    }
    return true;
}
// const result = []
// for(var i = 1000; i < 2000; i++){
//     if(isPrime(i)) {
//     for (let j = 2; j < 25; j++) {
//         if (isCoprime(j,i) && j < i && isPrimitiveRootModuloN(i,j)) {
//             result.push({prime: i,root: j})
//             console.log(j,'root')
//         }
//     }
// }
// }
// console.log(result)


function findPrimefactors( n) {
    const s = new Set();
    // Print the number of 2s that divide n
    while (n % 2 == 0) {
        s.add(2);
        n = n / 2;
    }
 
    // n must be odd at this point. So we can skip
    // one element (Note i = i +2)
    for (let i = 3; i <= Math.sqrt(n); i = i + 2) {
        // While i divides n, print i and divide n
        while (n % i == 0) {
            s.add(i);
            n = n / i;
        }
    }
 
    // This condition is to handle the case when
    // n is a prime number greater than 2
    if (n > 2)
        s.add(n);
    return s;
}
function findPrimitive(n) {
 
    // Check if n is prime or not
    if (isPrime(n) == false)
        return -1;
 
    // Find value of Euler Totient function of n
    // Since n is a prime number, the value of Euler
    // Totient function is n-1 as there are n-1
    // relatively prime numbers.
    let phi = n - 1;
 
    // Find prime factors of phi and store in a set
    const setOfPrimeFactors = new Set(findPrimefactors(phi));
     
    // Check for every number from 2 to phi
    for (let r = 2; r <= phi; r++) {
        // Iterate through all prime factors of phi.
        // and check if we found a power with value 1
        let flag = false;
        for (let it of setOfPrimeFactors) {
 
            // Check if r^((phi)/primefactors) mod n
            // is 1 or not
            if (Math.pow(r, phi / it, n) == 1) {
                flag = true;
                break;
            }
        }   
 
        // If there was no power with value 1.
        if (flag == false)
            return r;
    }
 
    // If no primitive root found
    return -1;
}



// console.log(findPrimitive(761))
// console.log(findPrimefactors(760))
// console.log(isPrimitiveRootModuloN(761, 6))

const df_helman = () => {
const my128 = BigInt(15796861302894803531n)
const root =  BigInt(6n)
const x= BigInt(Math.floor(Math.random() * 20000 +10000))
const y= BigInt(Math.floor(Math.random() * 20000 +10000))
const X = root ** x % my128; 
const Y = root ** y % my128; 
console.log(X, 'X')
console.log(Y, 'Y')

const kA = Y ** x % my128;
const kB = X ** y % my128;
console.log(kA, 'kA')
console.log(kB, 'kB')
console.log('shared key', kA)
}

function extendedEuclidean(a, b) {
    if (b === 0) {
        return [1, 0, a];
    }
    const [x, y, gcd] = extendedEuclidean(b, a % b);
    return [y, x - Math.floor(a / b) * y, gcd];
}
function modInverse(){
   return  (x % m + m) % m;
}


function eulerTotient(n) {
    let result = 0;
    for (let i = 1; i < n; i++) {
        if(gcd(n, i) === 1) {
            result++;
        }
    }
    return result;
}


const rsa = () => {

    const p = 47
    const q = 71
    const n = p * q
    const phi = (p-1) * (q-1)
    const e = 79
    function modInverse(a, m)
    {
        for(let x = 1; x < m; x++){
            if (((a % m) * (x % m)) % m == 1)
            return x;
        }
    }
    const encrypt = (message, e, n) => 
        message.map(charCode => BigInt(charCode) ** BigInt(e) % BigInt(n))
    
    const decrypt = (message, d, n) => 
        message.map(charCode => BigInt(charCode) ** BigInt(d) % BigInt(n)).map(charCode => String.fromCharCode(Number(charCode))).join('')

    const [x,y] = extendedEuclidean(e, phi)
    const d = modInverse(e, phi);
    const d1 = Math.ceil((x % phi + phi) % phi)

    const message = "Oleg pigyr kolu skachal asdsaklksaldjsalk l aksdjaslkdjsalkdj jaksldjalsk jkdsal jlaskdjas lkjsakdsadjlas dkjsalkd jasl kdjljldjls akjdlas j" 
    const asciiMessage = Array.from(message).map((_, index) => message.charCodeAt(index)) 

    const encryptedMessage = encrypt(asciiMessage, e, n)
    console.log(encryptedMessage)
    const decrypted = decrypt(encryptedMessage, d, n)
    console.log(encryptedMessage.map(charCode=>String.fromCharCode(Number(charCode))).join(''), 'encrypted')
    console.log(decrypted, 'decrypted')
}


// --- three dashes means congruent

rsa()
