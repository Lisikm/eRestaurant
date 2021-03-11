const btns = document.querySelectorAll("button");

add_text_field = btn => {
    btn.addEventListener("click", e => {
    e.preventDefault();
    let p = document.createElement("p");
    let inp = document.createElement("input");
    inp.type = "text";
    inp.maxLength = 255;
    inp.name= "description";
    let new_btn = document.createElement("button");
    new_btn.innerText = "Do not add a note";
    new_btn.type = "button"
    new_btn.addEventListener("click", e => {
        e.preventDefault();
        new_btn.parentElement.lastElementChild.remove()
        let show_text_field_button = document.createElement("button");
        show_text_field_button.innerText = "Show text field to add note";
        add_text_field(show_text_field_button)
        new_btn.parentElement.appendChild(show_text_field_button);
        new_btn.remove()
    });
    btn.parentElement.appendChild(new_btn);
    btn.parentElement.appendChild(p);
    p.appendChild(inp);
    btn.remove()
    })
}

do_not_show_text_field_button = btn => {}


btns.forEach(elem => {add_text_field(elem)})
