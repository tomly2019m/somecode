## 函数
### 解构赋值
实例1

```js
var [x, y, z] = ['hello', 'JavaScript', 'ES6'];//将后面的数组值依次传给前面的变量
let [x, [y, z]] = ['hello', ['JavaScript', 'ES6']];//多数组嵌套 依次对应即可
let [, , z] = ['hello', 'JavaScript', 'ES6']; // 忽略前两个元素，只对z赋值第三个元素
```
利用解构赋值，可以快速的获取一个js对象中的某些属性的值。  

实例2
```js
var person = {
    name: '小明',
    age: 20,
    gender: 'male',
    passport: 'G-12345678',
    school: 'No.4 middle school'
};
var {name, age, passport} = person;
// name, age, passport分别被赋值为对应属性,注意变量名字不能是属性名以外的值，否则会返回undefined
```
对同一对象进行解构赋值时，如果对象还嵌套着一个对象，可以进行如下的解构赋值操作：
```js
var person = {
    name: '小明',
    age: 20,
    gender: 'male',
    passport: 'G-12345678',
    school: 'No.4 middle school',
    address: {
        city: 'Beijing',
        street: 'No.1 Road',
        zipcode: '100001'
    }
};
var {name, address: {city, zip}} = person;
name; // '小明'
city; // 'Beijing'
zip; // undefined, 因为属性名是zipcode而不是zip
// 注意: address不是变量，而是为了让city和zip获得嵌套的address对象的属性:
address; // Uncaught ReferenceError: address is not defined
```
如果想要将对象的属性值取出来，并且想要另外取一个名字，可以这样操作：
```js
var person = {
    name: '小明',
    age: 20,
    gender: 'male',
    passport: 'G-12345678',
    school: 'No.4 middle school'
};

// 把passport属性赋值给变量id:
let {name, passport:id} = person;
name; // '小明'
id; // 'G-12345678'
// 注意: passport不是变量，而是为了让变量id获得passport属性:
passport; // Uncaught ReferenceError: passport is not defined
```
解构赋值可以给定需要定义的变量一个默认值，具体情况如下：
```js
var person = {
    name: '小明',
    age: 20,
    gender: 'male',
    passport: 'G-12345678'
};

// 如果person对象没有single属性，默认赋值为true:
var {name, single=true} = person;
name; // '小明'
single; // true
```
已经定义的变量不能被解构赋值：
```js
// 声明变量:
var x, y;
// 解构赋值:
{x, y} = { name: '小明', x: 100, y: 200};
// 语法错误: Uncaught SyntaxError: Unexpected token =
```
#### 用法
1.用于变量的值交换：

```js
var x=1, y=2;
[x, y] = [y, x];
```
2.快速获取当前的域名和路径：
```js
var {hostname:domain, pathname:path} = location;
```
3.函数的参数是一个对象：
```js
function buildDate({year, month, day, hour=0, minute=0, second=0}) {
    return new Date(year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second);
}
```
### 方法
给js中一个对象填加一个方法，实例如下：

```js
var xiaoming = {
    name: '小明',
    birth: 1990,
    age: function () {
        var y = new Date().getFullYear();
        return y - this.birth;
    }
};

xiaoming.age; // 如果利用console.log()输出的话，对得到function的源代码
xiaoming.age(); // 加上圆括号就表示调用
```
this指针和c++等语言一样，表示指向对象本身。
可以将函数的实现和对象的定义分离:
```js
function getAge() {
    var y = new Date().getFullYear();
    return y - this.birth;
}

var xiaoming = {
    name: '小明',
    birth: 1990,
    age: getAge
};

xiaoming.age(); // 25, 正常结果
getAge(); // NaN this指针在外部调用，指向的是window这个对象，但是window中没有birth这个属性 所以返回了NaN 
```
在对象的方法中嵌套函数，如果嵌套的函数中有<font color = ff0000>`this`</font>指针出现，那么该指针指向的并不是对象本身，而是<font color = ff0000>`window`</font>：
```js
var xiaoming = {
    name: '小明',
    birth: 1990,
    age: function () {
        function getAgeFromBirth() {
            var y = new Date().getFullYear();
            return y - this.birth; //此处this指针使用不正确
        }
        return getAgeFromBirth();
    }
};

xiaoming.age(); // Uncaught TypeError: Cannot read property 'birth' of undefined
```
想要让上述指针正常运转，得另外使用一个变量来承载<font color = ff0000>`this`</font>指针：
```js
var xiaoming = {
    name: '小明',
    birth: 1990,
    age: function () {
        var that = this; // 在方法内部一开始就捕获this
        function getAgeFromBirth() {
            var y = new Date().getFullYear();
            return y - that.birth; // 用that而不是this
        }
        return getAgeFromBirth();
    }
};

xiaoming.age(); // 25
```
#### apply
在一个独立的函数中，可以利用<font color = ff0000>`apply()`</font>方法指定<font color = ff0000>`this`</font>指针的指向，使得独立的函数正常运转，实例如下：

```js
function getAge() {
    var y = new Date().getFullYear();
    return y - this.birth;
}

var xiaoming = {
    name: '小明',
    birth: 1990,
    age: getAge
};

xiaoming.age(); // 25
getAge.apply(xiaoming, []); // 25, this指向xiaoming, 参数为空
```
<font color = ff0000>`apply()`</font>函数和<font color = ff0000>`call()`</font>函数：

* <font color = ff0000>`apply()`</font>函数把传入的参数打包成为<font color = ff0000>`Array`</font>之后再传入。
* <font color = ff0000>`call()`</font>函数直接按照顺序传入参数。
实例:
```js
Math.max.apply(null, [3, 5, 4]); // 5
Math.max.call(null, 3, 5, 4); // 5
```
两种调用<font color = ff0000>`max()`</font>函数的方式都是正确的，上者参数是<font color = ff0000>`[]`</font>，而下者参数是按顺序直接输入的。   
对于普通函数通常把<font color = ff0000>`this`</font>指定为<font color = ff0000>`null`</font>。   

#### 装饰器
利用<font color = ff0000>`apply()`</font>函数，可以动态的改变函数的行为。
例如，可以将JavaScript的内置函数<font color = ff0000>`phaseInt()`</font>添加一个统计被调用次数的功能：

```js
var count = 0;
var oldParseInt = parseInt; // 保存原函数

window.parseInt = function () {
    count += 1;
    return oldParseInt.apply(null, arguments); // 调用原函数
};
parseInt('10');
parseInt('20');
parseInt('30');
console.log('count = ' + count); // 3
```
### 高阶函数
JavaScript的函数其实都指向某个变量。既然变量可以指向函数，函数的参数能接收变量，那么一个函数就可以接收另一个J函数作为参数，这种函数就称之为高阶函数。
实例：

```js
function add(x, y, jf) {
    return f(x) + f(y);
}
add(-5, 6, Math.abs);
```
函数的调用过程为，先调用<font color = ff0000>`add()`</font>，而<font color = ff0000>`add()`</font>函数里面又调用了<font color = ff0000>`abs()`</font>,通过<font color = ff0000>`abs()`</font>对数据进行处理之后返回结果，再将这两个结果相加。<font color = ff0000>`abs()`</font>作为<font color = ff0000>`add()`</font>的一个参数。   
编写高阶函数，就是让函数的参数能够接收别的函数。   

#### map
<font color = ff0000>`map()`</font>是定义在<font color = ff0000>`Array`</font>中的一个高阶函数，参数是用户自定义的一个函数，用法示例：

```js
//示例1
function pow(x) {
    return x * x;
}
var arr = [1, 2, 3, 4, 5, 6, 7, 8, 9];
var results = arr.map(pow); // [1, 4, 9, 16, 25, 36, 49, 64, 81]
console.log(results);

//示例2
var arr = [1, 2, 3, 4, 5, 6, 7, 8, 9];
arr.map(String); // ['1', '2', '3', '4', '5', '6', '7', '8', '9']
```
`map()`方法可以通过少量代码高效的进行一些复杂的变换，如将`Array`中的元素变成原的平方，如将数值转化为字符串类型。**注意，map并不修改`Array`原始数据，而是返回一个处理好的`Array`。**
#### reduce
`reduce()`方法就`Array`对象是一个“套娃”函数，参数是用户自定义的函数，执行的逻辑为：依次将`Array`中的前两个元素的结果作为下一次执行的首元素，而将`Array`中第三个元素作为下一次执行第二元素，有递归的意思在。值得注意的是，这里的用户自定义函数的参数个数要为2。

```js
[x1, x2, x3, x4].reduce(f) 等价于 f(f(f(x1, x2), x3), x4)
```

**注意：`map()`函数能够接受三个参数，但是一般只会用到第一个参数，故当向`map()`传入的自定义函数有2个以及以上的参数时，要特别注意**   

#### filter
filter的作用是将`Array`中的某些元素**过滤**掉，返回剩下来的元素。
和`map()`类似，`Array`的`filter()`也是一个高阶函数，能够接收一个函数参数，依据返回值的`true`还是`false`来确定是否需要保留或者丢弃。
实例：

```js
//去掉Array中的偶数
var arr = [1, 2, 4, 5, 6, 9, 10, 15];
var r = arr.filter(function (x) {
    return x % 2 !== 0;
});
r; // [1, 5, 9, 15]

//去掉Array中的空字符
var arr = ['A', '', 'B', null, undefined, 'C', '  '];
var r = arr.filter(function (s) {
    return s && s.trim(); // 注意：IE9以下的版本没有trim()方法
});
r; // ['A', 'B', 'C']
```
##### 回调函数
`filter()`接收的回调函数可以有很多参数，但是一般只会使用第一个参数，回调的函数还可以接收另外两个参数，分别代表着元素的下标和数组本身，具体见以下示例：

```js
var arr = ['A', 'B', 'C'];
var r = arr.filter(function (element, index, self) {
    console.log(element); // 依次打印'A', 'B', 'C'
    console.log(index); // 依次打印0, 1, 2
    console.log(self); // self就是变量arr
    return true;
});
```
利用`filter()`去除重复元素：
```javascript
var arr = ['apple', 'strawberry', 'banana', 'pear', 'apple', 'orange', 'orange', 'strawberry'];
var r;
r = arr.filter(
    function(elment, index, self){
        return self.indexOf(element) === index;
    }//inexOf函数返回的是元素第一次出现的下标，如果重复返回false 则滤过 true表示保留
)
```
#### sort
`Array`中`sort()`方法就是用于数据的排序的方法，但是`sort()`方法对于数据的排序是默认按照字符串的来排序的，但是`sort()`也是一个高阶函数，可以接收用户自定义的函数作为参数传入。通常规定，对于两个元素`x`和`y`，如果认为`x < y`，则返回`-1`，如果认为`x == y`，则返回`0`，如果认为`x > y`，则返回`1`，这样，排序算法就不用关心具体的比较过程，而是根据比较结果直接排序。
按照数字大小进行排序，方法中的自定义函数可以这么写：

```js
var arr = [10, 20, 1, 2];
arr.sort(function (x, y) {
    if (x < y) {
        return -1;
    }
    if (x > y) {
        return 1;
    }
    return 0;
});
console.log(arr); // [1, 2, 10, 20]

//需要降序排序
function (x, y) {
    if (x < y) {
        return 1;
    }
    if (x > y) {
        return -1;
    }
    return 0;
}
```
**注意：`sort()`方法会对`Array`对象进行修改，但是返回值仍然是一个处理后的`Array`。**

#### Array中的其他高阶函数
##### every
`every()`方法用于判断数组中是否每一个元素都满足条件，如果是，返回`true`，否则返回`false`。
实例：

```js
var arr = ['Apple', 'pear', 'orange'];
console.log(arr.every(function (s) {
    return s.length > 0;
})); // true, 因为每个元素都满足s.length>0

console.log(arr.every(function (s) {
    return s.toLowerCase() === s;
})); // false, 因为不是每个元素都全部是小写
```
##### find
`find()`方法用于查找第一个满足某一条件的元素，如果找到了返回该元素，否则返回`undefined`。
实例

```js
var arr = ['Apple', 'pear', 'orange'];
console.log(arr.find(function (s) {
    return s.toLowerCase() === s;
})); // 'pear', 因为pear全部是小写

console.log(arr.find(function (s) {
    return s.toUpperCase() === s;
})); // undefined, 因为没有全部是大写的元素
```
##### findIndex
`findIndex()`方法与`find()`类似，不过返回值是元素的下标。如果没找到，返回`-1`。

```js
var arr = ['Apple', 'pear', 'orange'];
console.log(arr.findIndex(function (s) {
    return s.toLowerCase() === s;
})); // 1, 因为'pear'的索引是1

console.log(arr.findIndex(function (s) {
    return s.toUpperCase() === s;
})); // -1
```

##### forEach
`forEach()`和`map()`类似，都是将每个元素一次的传入自定义的函数，但是不会返回一个新的数组。

```js
var arr = ['Apple', 'pear', 'orange'];
arr.forEach(console.log); // 依次打印每个元素
```

### 闭包
高阶函数可以接受函数作为参数外，还可以把函数作为结果返回。
实例：

```js
function lazy_sum(arr) {
    var sum = function () {
        return arr.reduce(function (x, y) {
            return x + y;
        });
    }
    return sum;
}
```
当调用`lazy_sum()`时，返回的并不是一个结果，而是一整个求和的`sum()`函数：
```js
var f = lazy_sum([1, 2, 3, 4, 5]); // function sum()
```
只有调用`f()`时，才会返回结果：
```js
f(); // 15
```
每一次调用上述函数的时候，都会返回一个新的函数：
```js
var f1 = lazy_sum([1, 2, 3, 4, 5]);
var f2 = lazy_sum([1, 2, 3, 4, 5]);
f1 === f2; // false
```
`f1()`和`f2()`的调用结果互相不影响。
实例：
```js
function count() {
    var arr = [];
    for (var i=1; i<=3; i++) {
        arr.push(function () {
            return i * i;
        });
    }
    return arr;
}

var results = count();
var f1 = results[0];
var f2 = results[1];
var f3 = results[2];
```
在上述的例子中，每次循环都会创建一个新的函数，然后，把创建的3个函数都添加到一个`Array`中去，即`arr`这个`Array`中的每一个元素都是一个函数。
调用这些函数：
```js
f1(); // 16
f2(); // 16
f3(); // 16
```
得到的结果都是`16`，而不是`1`，`4`，`9`。原因在于返回的函数引用了局部的变量`i`，而当三个函数都返回的时候，局部变量`i`的值已经变成了`4`，当我们直接调用这些返回的函数的时候，使用到的临时变量的值都是`4`，因此调用三个函数，返回值都是`16`。因此，在使用闭包的时候，需要尽可能的避免临时变量的使用，因为临时变量的值会发生改变，这会导致之后的函数调用出现一些意想不到的错误，如果一定需要使用临时的变量，则应当再创建一个函数，把临时变量当作这个函数的参数传入，上述例子可以通过这样的方法解决：
```js
function count() {
    var arr = [];
    for (var i=1; i<=3; i++) {
        arr.push((function (n) {
            return function () {
                return n * n;
            }
        })(i));
    }
    return arr;
}

var results = count();
var f1 = results[0];
var f2 = results[1];
var f3 = results[2];

f1(); // 1
f2(); // 4
f3(); // 9
```
此处用到了一个“创建一个匿名函数并立即执行”的语法：
```js
(function (x) {
    return x * x;
})(3); // 9
```
其一般的形式如下所示，由于`javascript`语法解析的相关的问题，这里需要讲整个匿名函数定义用括号括起来：
```js
(function(x1,x2...){
    //do something
})(a1,a2...);
```
在没有`class`机制，只有函数的编程语言中，可以借助闭包，来实现一个变量的封装，例如可以利用js创建一个计数器的私有变量：
```js
'use strict';

function create_counter(initial) {
    var x = initial || 0;
    return {
        inc: function () {
            x += 1;
            return x;
        }
    }
}

//使用方法
var c1 = create_counter();
c1.inc(); // 1
c1.inc(); // 2
c1.inc(); // 3

var c2 = create_counter(10);
c2.inc(); // 11
c2.inc(); // 12
c2.inc(); // 13
```
在返回的对象中，实现了一个闭包，该闭包携带了一个局部的变量`x`，并且从外部无法访问到这个局部的变量，这也就是说，闭包就是携带状态的函数，并且它的状态可以完全对外隐藏起来。
闭包还可以把多个参数变成单个参数的函数，例如：
```js
function make_pow(n) {
    return function (x) {
        return Math.pow(x, n);
    }
}//返回一个函数 这个函数可以便捷的计算出 x的n次方，那么当下一次要计算x的n次方时，只需要调用这个新建出来的函数即可
// 创建两个新函数:
var pow2 = make_pow(2);
var pow3 = make_pow(3);

console.log(pow2(5)); // 25
console.log(pow3(7)); // 343
//实现了从多个参数到单个参数的转变
```

### 箭头函数
箭头函数之所以叫做箭头函数，是因为其形式形如一个箭头：

```js
x => x * x
```
上述的箭头函数相当于以下函数：
```js
function f(x){
    return x * x;
};
```
箭头函数相当于一个匿名的函数，在此基础之上并简化的了函数的定义，一般箭头函数具有两种格式，一种就是像`x => x * x`这样子的只包含一个表达式，另外一种格式包含函数的大体结构，包括`{...}`和`return`，例如以下箭头函数：
```js
x => {
    if (x > 0) {
        return x * x;
    }
    else {
        return -x * x;
    }   
}
```
如果参数的数量不止一个，需要用圆括号`()`把参数括起来：
```js
(x, y) => x * x + y * y;//两个参数

//无参数
() => 3.1415926

//可变参数
(x, y, ...rest) => {
    var i, sum = x + y;
    for (i = 0; i < rest.length; i++){
        sum += rest[i];
    }
    return sum;
}
```
如果箭头函数的返回值是一个对象，需要加上`()`：
```js
//SyntaxError
x => {foo : x}


//要改成以下形式
x => ({foo : x})
```
#### this
箭头函数看上去是对于匿名函数的一种简写形式，但是实际上，箭头函数的一个重要特性就是内部的`this`仍属于词法的作用域，由上下文来确定。（即`this`并不会像匿名函数中的那样会出现异常）
在不用箭头函数的情况下，下面的例子无法得到预期的效果：

```js
var obj = {
    birth: 1990,
    getAge: function () {
        var b = this.birth; // 1990
        var fn = function () {
            return new Date().getFullYear() - this.birth; // this指向window或undefined
        };
        return fn();
    }
};

//如果将上述匿名函数修改为箭头函数，那么程序可以正常运行
var fn = () => new Date().getFullYear() - this.birth; // this仍然指向obj
```
由于`this`在箭头函数中已经按照词法作用域绑定了，所以，用`call()`或者`apply()`调用箭头函数的时候，无法对`this`进行绑定，即传给`call()`和`apply()`的第一个参数将被忽略：
```js
var obj = {
    birth: 1990,
    getAge: function (year) {
        var b = this.birth; // 1990
        var fn = (y) => y - this.birth; // this.birth仍是1990
        return fn.call({birth:2000}, year); //无视传入的对象，year仍然是1990
    }
};
obj.getAge(2015); // 25
```
### generator
generator(生成器)是一种数据类型，一个generator看上去像一个函数，但是与函数不同的是，它可以多次返回。
generator的定义如下：

```js
function* foo(x) {
    yield x + 1;
    yield x + 2;
    return x + 3;
}
```
generator和函数不同的是，generator有`function*`定义，并且，出了`return`外，还可以通过`yield`返回多次。
实例，用generator生成斐波那契数列：
```js
function* fib(max){
    var
        t,
        a = 0,
        b = 1,
        n = 0;
    while (n < max){
        yield a;
        [a, b] = [b, a + b];
        n++;
    }
    return;
}
```
直接调用一个generator和调用函数不一样，`fib(5)`仅仅是创建了一个generator对象，并没有去执行它。
调用generator对象有两种方法，第一种方法是通过直接调用generator的`next()`方法：
```js
var f = fib(5);
f.next(); // {value: 0, done: false}
f.next(); // {value: 1, done: false}
f.next(); // {value: 1, done: false}
f.next(); // {value: 2, done: false}
f.next(); // {value: 3, done: false}
f.next(); // {value: undefined, done: true}
```
`next()`方法会执行generator的代码，然后每次遇到`yield x`,就会返回一个对象`{value : x, done:false/true}`,然后“暂停”。返回的`value`就是`yield`的返回值，`done`表示这个generator是否已经执行结束，如果`done`为`true`，则`value`的值就是`return`返回的值。当`done`的值为`true`时，这个generator对象就执行完毕了。
第二种方法就是直接用`for ... of`循环迭代generator对象，这种方式不需要自己判断`done`:
```js
function* fib(max) {
    var
        t,
        a = 0,
        b = 1,
        n = 0;
    while (n < max) {
        yield a;
        [a, b] = [b, a + b];
        n++;
    }
    return;
}
for (var x of fib(10)){
    console.log(x)//会依次输出 0 1 1 2 3...
}
```
## 标准对象
### Date
在JavaScript中，`Date`对象用于表示日期和时间。
要获取系统的当前时间，用法如下：

```js
var now = new Date(); //新建一个date对象
now;//current time of the system
now.getFullYear();//get the year
now.getMonth();//get the month
now.getDate();//get the day number in a month
now.getDay();//get which day in a week
now.getHours();//get the hours in 24 hours
now.getMinutes(); //get the minutes
now.getSeconds(); // get the second
now.getMillSeconds();//get the millseconds
now.getTime();//return a number that represents the time
```
如果想要创建一个指定日期和时间的`Date`对象，可以用以下形式创建：
```js
var d = new Date(2020, 8, 7, 9, 58, 26, 123)
d;//d的时间就是人为设定的时间
```
值得注意的一点是，JavaScript中的月份是从0开始的，也就是0代表一月，1代表二月。在设置时间的时候需要引起注意，不要弄错。
第二种创建一个指定日期和时间的方法是解析一个标准的格式化字符串：
```js
var d = Date.parse('2015-06-24T19:49:22.875+08:00');
d; // 1435146562875
```
但是它返回的并不是一个`Date`对象，而是一个时间戳，也就是当前设置的时间离1970年1月1日0时整的毫秒数。
有了时间戳，可以很容易的将时间戳转化为相应的`Date`对象，方法如下所示：
```js
var d = new Date(1435146562875);
d; // Wed Jun 24 2015 19:49:22 GMT+0800 (CST)
d.getMonth(); // 5
```
**注意：使用`Date.parse()`时传入的字符串使用实际月份01-12，转换为Date对象后getMonth()获取的月份值为0-11。**

时区的转换：
```js
var d = new Date(1435146562875);
d.toLocaleString(); // '2015/6/24 下午7:49:22'，本地时间（北京时区+8:00），显示的字符串与操作系统设定的格式有关
d.toUTCString(); // 'Wed, 24 Jun 2015 11:49:22 GMT'，UTC时间，与本地时间相差8小时
```
### RegExp(正则表达式)
正则表达式是一种用来进行字符串匹配的强大工具，它的设计思想是用一种描述性的语言来给字符串定一个规则，凡是符合规则的字符串，我们就认为是“匹配”了，否则，该字符串就是不合法的。
判断一个字符串是否是Email字符串，可以利用以下方法：
1.创建一个匹配Email的正则表达式；
2.用改正则表达式去匹配用户的输入来判断输入是否合法，也即是否为Email字符串。
在正则表达式中，如果直接给出字符串，就是精确匹配。用`\d`来匹配数字，`\w`可以匹配一个字符或者数字，所以：

* `'00\d'`可以用来匹配`'007'`，但是无法匹配`'00A'`;
* `'\d\d\d'`可以用来匹配`'010'`;
* `'\w\w'`可以用来匹配`'js'`;
* `.`可以用来匹配任意字符，因此`'js.'`可以用来匹配`'jsp'`、`'jss'`等;
要匹配变长的字符，在正则表达式中，用`*`表示任意多个字符（包含0个），用`+`表示至少一个字符，用`?`表示0个或1个字符，用`{n}`表示n个字符，用`{n,m}`表示n-m个字符。

例如：`\d{3}\s+\d{3,8}`
1.`\d{3}`表示匹配三个数字，例如`'010'`;
2.`\s`表示匹配一个空格（或者一个tab等空白符），所以`\s+`表示至少有一个空格，可以用来匹配`' '`、`'\t\t'`等;
3.`d{3,8}`表示匹配一个3-8位的数字，例如`'12345'`;
实例，匹配一个“xxx-xxxxx”这样的号码，写出表达式:`\d{3}\-\d{3,8}`。
上述表达式中，由于“-”是一个特殊字符，所以需要用`\`进行转义。
#### 进阶
要做到更为精确的匹配，可以用`[]`表示范围，比如：

* `[0-9a-zA-Z\_]`可以匹配一个数字、字母或者下划线；
* `[0-9a-zA-Z\_]+`可以匹配至少由一个数字、字母或者下划线组成的字符串，比如`'a100'`,`'0_Z'`,`'js2015'`等等；
* `[a-zA-z\_\$][0-9a-zA-Z\_\$]*`可以匹配由字母、下划线、`$`开头，后面接一个任意长度的由数字、字母、下划线、`$`组成的字符串组成的字符串，这也就是JavaScript的变量名规则；
* `[]`后面接`{}`代表相应的数量，同上面的规则
* `A|B`可以匹配`A`或者`B`，所以`(J|j)ava(S|s)cript`可以匹配四种不同字符串；
* `^`表示行的开头，例如`^\d`表示要以数字开头；
* `$`表示行的结束，例如`$\d`表示要以数字结束；
* `^ ... $`表示整行匹配

#### RegExp
以上是正则表达式的一些基础知识，在JavaScript中，我们有两种方式来创建一个正则表达式：
第一种方式就是直接通过`/正则表达式/`写出来，第二种方式是通过`new RegExp('正则表达式')`创建一个RegExp对象。
两种写法是一样的：

```js
var re1 = /ABC\-001/;
var re2 = new RegExp('ABC\\-001');
//此处 \\ 是转义字符 表示 \
re1; // /ABC\-001/
re2; // /ABC\-001/
```
RegExp对象的`test()`方法用于判断一个字符串是否符合条件。
```js
var re = /^\d{3}\-\d{3,8}$/;
re.test('010-12345'); // true
re.test('010-1234x'); // false
re.test('010 12345'); // false
```
#### 切分字符串
用正则表达式切分字符串比用固定的字符更灵活，正常的切分字符串的代码时这样的：

```js
'a b   c'.split(' '); // ['a', 'b', '', '', 'c']
```
上述方法无法正确的识别出连续的空格，可以用正则表达式进行改进：
```js
'a b   c'.split(/\s+/); // ['a', 'b', 'c']
```
可以加入新的分隔符`,`:
```js
'a,b, c  d'.split(/[\s\,]+/); // ['a', 'b', 'c', 'd']
```
#### 分组
出了简单的判断是否匹配之外，正则表达式还有提取子串的强大功能，用`()`表示的就是要提取的分组(group)。例如：
`^(\d{3})-(\d{3,8})$`分别定义了两个组，运行效果如下：

```js
var re = /^(\d{3})-(\d{3,8})$/;
re.exec('010-12345'); // ['010-12345', '010', '12345']
re.exec('010 12345'); // null
```
如果正则表达式中定义了组，就可以在RexExp对象上用`exec()`方法提取出来。
`exec()`方法在匹配成功之后，会返回一个`Array`，第一个元素是正则表达式匹配到的字符串，后面的字符串表示匹配成功的子串。
`exec()`方法在匹配失败之后会返回一个`null`。
下面这个正则表达式可以直接识别出合法的时间：
```js
var re = /^(0[0-9]|1[0-9]|2[0-3]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])$/;
re.exec('19:05:30'); // ['19:05:30', '19', '05', '30']
```
#### 贪婪匹配
正则匹配默认的是贪婪匹配，也就是尽可能多的匹配更多的字符，例如：

```js
var re = /^(\d+)(0*)$/;
re.exec('102300'); // ['102300', '102300', '']
```
由于`\d+`采取了贪婪匹配，直接把后面的所有数字全都匹配了，结果`0*`只能匹配空字符了。
这并不是我们想要的结果，因此，我们必须让`\d+`采用非贪婪匹配，才能把后面的`0`给匹配出来，加入一个`?`就可以让`\d+`采取非贪婪匹配：
```js
var re = /^(\d+?)(0*)$/;
re.exec('102300'); // ['102300', '1023', '00']
```
#### 全局搜索
JavaScript中的正则表达式还有以下几点特殊的用法，最常见的就是`g`,表示全局匹配：

```js
var r1 = /test/g;
// 等价于:
var r2 = new RegExp('test', 'g');
```
全局匹配可以执行多次`exec()`方法来搜索一个匹配的字符串，当我们指定`g`标志之后，每次运行`exec()`，正则表达式本身会更新`lastIndex`属性，`lastIndex`表示上次匹配到的最后的索引：
```js
var s = 'JavaScript, VBScript, JScript and ECMAScript';
var re=/[a-zA-Z]+Script/g;

// 使用全局匹配:
re.exec(s); // ['JavaScript']
re.lastIndex; // 10

re.exec(s); // ['VBScript']
re.lastIndex; // 20

re.exec(s); // ['JScript']
re.lastIndex; // 29

re.exec(s); // ['ECMAScript']
re.lastIndex; // 44

re.exec(s); // null，直到结束仍没有匹配到
```
全局搜索和`^...$`两者之间不能混用，否则只会匹配一次。
正则表达式还可以指定`i`标志，表示或略大小写，`m`标志表示执行多次的匹配。

### JSON

JSON是JavaScript Object Notation的缩写，它是一种数据交换格式。

JSON中的数据类型有以下几类：

* number：和JavaScript中的`number`完全一致；
* boolean：就是JavaScript中的`true`或者`false`；
* string：就是JavaScript中的`string`；
* null：就是JavaScript中的`null`；
* array：就是JavaScript中的`Array`，表示方式——`[]`；
* object：就是JavaScript中的`{ ... } `；

以及上面的任意组合。

并且JSON还定死了字符集必须是UTF-8，为了统一解析，JSON的字符串规定必须使用双引号`""`，Object的键也必须使用双引号`""`。

#### 序列化

让我们先把小明这个对象序列化成JSON格式的字符串：

```js
'use strict';

var xiaoming = {
    name: '小明',
    age: 14,
    gender: true,
    height: 1.65,
    grade: null,
    'middle-school': '\"W3C\" Middle School',
    skills: ['JavaScript', 'Java', 'Python', 'Lisp']
};

var s = JSON.stringify(xiaoming);
console.log(s);

//输出结果：{"name":"小明","age":14,"gender":true,"height":1.65,"grade":null,"middle-school":"\"W3C\" Middle School","skills":["JavaScript","Java","Python","Lisp"]}
```

要输出的好看一点，可以加上参数，按照缩进来输出：

```js
JSON.stringify(xiaoming, null, '  ');//第三个参数就是每次缩进的量（空格数目）也可以设置成其他字符，不过这样就不太美观了

//结果
{
  "name": "小明",
  "age": 14,
  "gender": true,
  "height": 1.65,
  "grade": null,
  "middle-school": "\"W3C\" Middle School",
  "skills": [
    "JavaScript",
    "Java",
    "Python",
    "Lisp"
  ]
}
```

第二个参数用于控制如何筛选对象的键值，如果我们只想输出指定的属性，可以传入`Array`:

```js
JSON.stringify(xiaoming, ['name', 'skills'], '  ');

//结果
{
  "name": "小明",
  "skills": [
    "JavaScript",
    "Java",
    "Python",
    "Lisp"
  ]
}
```

还可以传入一个函数，这样对象的每个键值对都会被预先处理：

```js
function convert(key, value){
    if (typeof value === 'string'){
        return value.toUpperCase();
    }
    return value;
}//把所有值改成大写

JSON.stringify(xiaoming, convert, '  ');

//结果
{
  "name": "小明",
  "age": 14,
  "gender": true,
  "height": 1.65,
  "grade": null,
  "middle-school": "\"W3C\" MIDDLE SCHOOL",
  "skills": [
    "JAVASCRIPT",
    "JAVA",
    "PYTHON",
    "LISP"
  ]
}
```

如果想要精确的控制转化后的字符串，可以给小明定义一个`toJSON()`的方法，直接返回JSON应该序列化的数据，示例如下：

```js
var xiaoming = {
    name: '小明',
    age: 14,
    gender: true,
    height: 1.65,
    grade: null,
    'middle-school': '\"W3C\" Middle School',
    skills: ['JavaScript', 'Java', 'Python', 'Lisp'],
    toJSON: function () {
        return { // 只输出name和age，并且改变了key：
            'Name': this.name,
            'Age': this.age
        };
    }
};

JSON.stringify(xiaoming); // '{"Name":"小明","Age":14}'
```

#### 反序列化

拿到一个JSON格式的字符串，我们直接用`JSON.parse()`把它变成一个JavaScript对象：

```js
JSON.parse('[1,2,3,true]'); // [1, 2, 3, true]
JSON.parse('{"name":"小明","age":14}'); // Object {name: '小明', age: 14}
JSON.parse('true'); // true
JSON.parse('123.45'); // 123.45
```

`JSON.parse()`还可以接收一个函数，用来转化解析出的属性：

```js
var obj = JSON.parse('{"name":"小明","age":14}', function (key, value) {
    if (key === 'name') {
        return value + '同学';
    }
    return value;
}); //把 小明 转化为 小明同学
console.log(JSON.stringify(obj)); // {name: '小明同学', age: 14}
```





## 面向对象编程

### 创建对象

JavaScript对每个创建的对象都会设置一个原型，指向它的原型对象

当我们`obj.xxx`访问一个对象的属性的时候，JavaScript引擎首先会在当前的对象上查找是否有该属性，如果没有找到该属性，就会去其原型的对象上去找，如果一直没有找到，就会一直找到`Object.prototype`对象，最后如果还是没有找到，那么就睡返回`undefined`。

例如，创建一个`Array`对象：

```js
var arr = [1, 2, 3];
```

其原型链如下所示：

```js
arr ----> Array.prototype ----> Object.prototype ----> null
```

`Array.prototype`里面定义了`indexOf()`、`shift()`等方法，因此我们可以在`Array`对象上调用这些方法。

当我们创建一个函数的时候：

```js
function foo() {
    return 0;
}
```

在JavaScript中，函数也属于一个对象，它的原型链是这样的：

```js
foo ----> Function.prototype ----> Object.prototype ----> null
```

由于`Function.prototype`中定义了`apply()`等方法，因此，所有的函数都可以调用`apply()`方法。

#### 构造函数

出了直接用`{...}`创建一个对象外，JavaScript中还可以用一种构造函数的方法来创建一个对象，它的用法是，先定义一个构造函数：

```js
function Student(name) {
    this.name = name;
    this.hello = function () {
        alert('Hello, ' + this.name + '!');
    }
}
```

从形式上来看，这似乎是一个普通的函数，但是在JavaScript中，可以用关键字`new`来调用这个函数，并会返回一个对象：

```js
var xiaoming = new Student('小明');
xiaoming.name; // '小明'
xiaoming.hello(); // Hello, 小明!
```

**<font color = #ff0000>注意，</font>**如果不写`new`，这就是一个普通的函数，它返回`undefined`，但是如果写了`new`，它就会变成一个构造函数，它绑定的`this`指向新创建的对象，并默认返回`this`，也就是说，函数最后可以不用写`return this;`。

新创建的`xiaoming`的原型链如下：

```js
xiaoming ----> Student.prototype ----> Object.prototype ----> null
```

也就是说，`xaioming`的原型指向函数`Student`的原型，如果另外创建的了别的对象，这些对象的原型都是指向`Student`的原型：

```js
xiaoming ↘
xiaohong -→ Student.prototype ----> Object.prototype ----> null
xiaojun  ↗
```

用`new Student()`创建出来的对象还从原型上获得了一个`constructor`属性，它指向函数`Student`本身，即：

```js
xiaoming.constructor === Student.prototype.constructor; // true
Student.prototype.constructor === Student; // true

Object.getPrototypeOf(xiaoming) === Student.prototype; // true

xiaoming instanceof Student; // true
```

用一张图表示上述的关系，就是这样的：

![l](C:\Users\HIPAA\Desktop\javascript基础\picture\l.png)

红色的箭头就是原型链，从继承的关系上来看，我们认为，`xaioming`、`xiaohong`这些对象继承于`Student`。

根据上述的讨论，要让创建的对象共享一个`hello`函数，根据对象的属性查找规则，我们只要把`hello`函数移动到需要被创建的对象的共同的原型上就可以了，也就是`Stuent.prototype`：

```js
function Student(name) {
    this.name = name;
}

Student.prototype.hello = function () {
    alert('Hello, ' + this.name + '!');
};
```

#### 不用new来创建一个对象

```js
function Student(props) {
    this.name = props.name || '匿名'; // 默认值为'匿名'
    this.grade = props.grade || 1; // 默认值为1
}

Student.prototype.hello = function () {
    alert('Hello, ' + this.name + '!');
};

function createStudent(props) {
    return new Student(props || {})
}
```

上述<font color = ff0000>`creatStudent()`</font>函数有以下几个巨大的优点：一是不需要用<font color = ff0000>`new`</font>来调用，二是参数十分的灵活，可以不传参数，也可以像下面这种方式传递参数：

```js
var xiaoming = createStudent({
    name: '小明'
});

xiaoming.grade; // 1
```

### 原型继承

