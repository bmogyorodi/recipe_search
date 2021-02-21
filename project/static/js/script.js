includedIngr = JSON.parse(document.getElementById('IncludedIngrData').textContent);
excludedIngr = JSON.parse(document.getElementById('ExcludedIngrData').textContent);


document.getElementById("searchForm").onsubmit = function() {
    document.getElementById("IncludeListInput").value = includedIngr.join()
    document.getElementById("ExcludeListInput").value = excludedIngr.join()
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

document.getElementById("ClearIngrButton").onclick = clearIngredients;

function addIngredient(ingrArray, ingr, listId) {
    if (!includedIngr.includes(ingr) && !excludedIngr.includes(ingr)) {
        // Add ingredient to list
        ingrArray.push(ingr);
        
        // Display the ingredient
        document.getElementById("listId");
        var ul = document.createElement("li");
        ul.classList.add("list-inline-item");
        var text_node = document.createTextNode(ingr);
        ul.appendChild(text_node);
        document.getElementById(listId).appendChild(ul)
    }
}

function removeIngredient(ingrArray, ingr, listId) {
    // Find the index of the ingredient to be removed
    idx = ingrArray.indexOf(ingr)

    // Remove the ingredient if it was found in the list
    if (idx > -1) {
        ingrArray.splice(idx, 1);

        // Remove the ingredient from the displayed list
    }

}

function clearIngredients() {
    includedIngr = [];
    excludedIngr = [];
    document.getElementById("IncludedIngrList").innerHTML = "";
    document.getElementById("ExcludedIngrList").innerHTML = "";
}
