

document.addEventListener('DOMContentLoaded', function() {
    // Retrieve the form element by its ID
    const formElement = document.getElementById('musicForm');
    const categoryButton = document.getElementById('category');

    // Setting an item
    localStorage.setItem('testKey', 'testValue');

    // Getting an item
    const value = localStorage.getItem('testKey');
    console.log(value);  // Should log 'testValue'. WORKS

    const value2 = localStorage.getItem('user');
    console.log(value);  // Should log 'testValue'. WORKS
    console.log(value2)
    if(value2){
        document.getElementById('display').innerHTML = value2;
    }
    // Check if the form element exists
    if (formElement.innerText) {
        console.log(formElement.innerText)
        // Retrieve the inner text of the form, for whatever purpose you need it

        // Store the inner text in local storage
        localStorage.setItem('user', formElement.innerHTML);

        // Add a submit event listener to the form
        // formElement.addEventListener('submit', function(event) {
        //     event.preventDefault();
        //     console.log("event is being triggered")
        //     const bro3 = localStorage.getItem('user');  // Log the data on submit
        //     console.log(bro3);

        //  });
    } else {
        console.log("No element with ID 'musicForm' found");
    }
});


