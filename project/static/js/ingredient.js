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
        function add_ingredient()
        {
        const new_element=document.getElementById("include_ingredients").value;
        if(!allItem.includes(new_element) || included.includes(new_element) || excluded.includes(new_element))
        {
          return 
        }
        document.getElementById("include_ingredients").value="";
        var ingredientlist=document.getElementById("ingredientlist");
        
        
        
        var added_item=document.createElement('LI');
        var textnode=document.createTextNode(new_element);
        added_item.appendChild(textnode);
        included.push(new_element)
        document.getElementById("added_ingredients").appendChild(added_item);
        AddToHiddenField(document.getElementById("include_list"),new_element);
        }
      function exclude_ingredient()
      {
        const new_element=document.getElementById("exclude_ingredients").value;
        

        if(!allItem.includes(new_element) || excluded.includes(new_element)|| included.includes(new_element))
        {
          return
        }
        document.getElementById("exclude_ingredients").value=""
        var added_item=document.createElement('LI');
        var textnode=document.createTextNode(new_element);
        added_item.appendChild(textnode);
        excluded.push(new_element);
        document.getElementById("excluded_ingredients").appendChild(added_item);
        AddToHiddenField(document.getElementById("exclude_list"),new_element);
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