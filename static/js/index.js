function type_documents()
{
    let selection = document.getElementById("id_option");
    let get_div = document.getElementById("other_doc");
    let get_full_form = document.getElementById("full_form")

    let decision = selection.options[selection.selectedIndex].value;


    if(decision === "I")
    {
        get_div.style.display = "none";
    }
    else if(decision === "E")
    {
        get_div.style.display = "block";
    }
}