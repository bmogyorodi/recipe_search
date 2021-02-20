function update_searchfield(search_exp)
{
    document.getElementById("search_field").value=search_exp;
}
var included=[]
var excluded=[]
var allItem=[
    'cheese',
    'pepper',
    'tomato',
    'salt',
    'cucumber' ,
    'flour',
    'chicken breast',
    'chicken wings',
    'chicken fillet'
]
function add_ingredient(ingredient_name)
{
  if(!allItem.includes(ingredient_name) || included.includes(ingredient_name) || excluded.includes(ingredient_name))
  {
    return 
  }
  document.getElementById("IngrIncludeInput").value="";
  var ingredientlist=document.getElementById("ingredientlist");



  var added_item=document.createElement('LI');
  var textnode=document.createTextNode(ingredient_name);
  added_item.appendChild(textnode);
  included.push(ingredient_name)
  document.getElementById("added_ingredients").appendChild(added_item);
  AddToHiddenField(document.getElementById("include_list"),ingredient_name);
}

function exclude_ingredient(ingredient_name)
{
if(!allItem.includes(ingredient_name) || excluded.includes(ingredient_name)|| included.includes(ingredient_name))
{
  return
}
document.getElementById("IngrExcludeInput").value=""
var added_item=document.createElement('LI');
var textnode=document.createTextNode(ingredient_name);
added_item.appendChild(textnode);
excluded.push(ingredient_name);
document.getElementById("excluded_ingredients").appendChild(added_item);
AddToHiddenField(document.getElementById("exclude_list"),ingredient_name);
}
function AddToHiddenField(inputField,element)
{
if(inputField.value=="")
{
  inputField.value+=element;
  return;
}
inputField.value+=","+element;


}
function ResetIngredients()
{
document.getElementById("exclude_list").value="";
document.getElementById("include_list").value="";
document.getElementById("excluded_ingredients").innerHTML='';
document.getElementById("added_ingredients").innerHTML='';
included=[]
excluded=[]
}