includedIngr = JSON.parse(document.getElementById('IncludedIngrData').textContent);
excludedIngr = JSON.parse(document.getElementById('ExcludedIngrData').textContent);
mustHaveIngr = JSON.parse(document.getElementById('MustHaveIngrData').textContent);
allIngr = JSON.parse(document.getElementById('AllIngrData').textContent);


document.getElementById("searchForm").onsubmit = function() {
    document.getElementById("IncludeListInput").value = includedIngr.join();
    document.getElementById("ExcludeListInput").value = excludedIngr.join();
    document.getElementById("MustHaveListInput").value = mustHaveIngr.join();
}

document.getElementById("IngrIncludeButton").onclick = function() {
    var input = document.getElementById("IngrIncludeInput");
    var value = input.value;
    addIngredient(includedIngr, value, "IncludedIngrList");
    input.value = "";   
}

document.getElementById("IngrExcludeButton").onclick = function() {
    var input = document.getElementById("IngrExcludeInput");
    var value = input.value;
    addIngredient(excludedIngr, value, "ExcludedIngrList");
    input.value = "";
}

document.getElementById("IngrMustHaveButton").onclick = function() {
    var input = document.getElementById("IngrMustHaveInput");
    var value = input.value;
    addIngredient(mustHaveIngr, value, "MustHaveIngrList");
    input.value = "";
}

document.getElementById("ClearIngrButton").onclick = clearIngredients;

function addIngredient(ingrArray, ingr, listId) {
    if (!includedIngr.includes(ingr) && !excludedIngr.includes(ingr) 
            && !mustHaveIngr.includes(ingr) && allIngr.includes(ingr)) {
        // Case-fold ingredient so that upper case searches correctly
        ingr = ingr.toLowerCase()
        // Add ingredient to list
        ingrArray.push(ingr);
        
        // Display the ingredient
        var li = document.createElement("li");
        li.classList.add("list-inline-item");

        var button = document.createElement("button");
        button.classList.add("btn", "btn-outline-secondary", "rounded-pill", "ingr-button");
        button.dataset.ingredient = ingr;
        button.dataset.listId = listId;
        button.onclick = ingredientButtonClick;

        var remove_icon = document.createElement("i");
        remove_icon.classList.add("fas", "fa-times");
        button.appendChild(remove_icon);

        var text_node = document.createTextNode(" " + ingr);
        button.appendChild(text_node);

        li.appendChild(button);
        document.getElementById(listId).appendChild(li);
    }
}

function removeIngredient(ingrArray, ingr) {
    // Find the index of the ingredient to be removed
    idx = ingrArray.indexOf(ingr)

    // Remove the ingredient if it was found in the list
    if (idx > -1) {
        ingrArray.splice(idx, 1);
    }
}

function ingredientButtonClick() {
    listId = this.dataset.listId;
    ingr = this.dataset.ingredient;

    // Remove ingredient from array
    if (listId == "IncludedIngrList") {
        removeIngredient(includedIngr, ingr);
    } else if (listId == "ExcludedIngrList") {
        removeIngredient(excludedIngr, ingr);
    } else {
        removeIngredient(mustHaveIngr, ingr);
    }

    // Remove button
    document.getElementById(listId).removeChild(this.parentNode);
}

function clearIngredients() {
    includedIngr = [];
    excludedIngr = [];
    mustHaveIngr = [];
    document.getElementById("IncludedIngrList").innerHTML = "";
    document.getElementById("ExcludedIngrList").innerHTML = "";
    document.getElementById("MustHaveIngrList").innerHTML = "";
}

var ingr_buttons = document.getElementsByClassName("ingr-button");

for (var i = 0; i < ingr_buttons.length; i++) {
    ingr_buttons[i].onclick = ingredientButtonClick;
}

document.getElementById("IngrMustHaveInput").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("IngrMustHaveButton").click();
    }
});

document.getElementById("IngrIncludeInput").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("IngrIncludeButton").click();
    }
});

document.getElementById("IngrExcludeInput").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("IngrExcludeButton").click();
    }
});
