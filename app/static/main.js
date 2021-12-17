console.log('This is a message from jkavascripts');

const name = "Nkosie";
const age = 33;

greating = `My name is ${name} I am ${age} years old .`;

console.log (greating);

console.log(greating.substring(11,16).toUpperCase());


const fruits = ['bannana', 'mango', 'lemon'];

fruits.unshift('watermelon');
fruits.push('apple');
mango = fruits.indexOf('mango')
 const person = {firstName : "Nkosie",
                lastName : "Maphumulo",
                age:"33",
                hobbies:["music","coding", "playing"],
                address:{street:"14 Protia rd",
                        town:"wychwood",
                        city:"Germiston",
                        postalCode:1401,
                        province:"Gauteng"
            }     
} 
const todo = [
    {id : "1",
    text: "Need to calibrate l2",
    date:"23-04-2021"},
    {id : "2",
    text: "Need to calibrate l1",
    date:"19-06-2021"},
    {id : "3",
    text: "Need to do quich check on l3",
    date:"23-04-2021"}
];

const todojson = JSON.stringify(todo)
console.log(todojson)
console.log(fruits)
console.log(fruits.includes('bannana' && 'man'))

console.log(person.address.town)

