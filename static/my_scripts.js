// Smaze symboly na frontendu (na backendu je toto pomale a buguje nejspis protoze se porad posilaji post requesty)
function reset_symbols() {
    let akt_id = "";
    for(let x = 0; x<15; x++)
    {
        for (let y = 0; y<15; y++)
        {
            akt_id = "btn_" + x + "_" + y;
            document.getElementById(akt_id).textContent = "";
        }
    }
}

// Vy/zapne tlacitka na hraci plose, state je boolean hodnota
function change_buttons_state(state){
    let akt_id = "";
    for(let x = 0; x<15; x++)
    {
        for (let y = 0; y<15; y++)
        {
            akt_id = "btn_" + x + "_" + y;
            document.getElementById(akt_id).disabled = state;
        }
    }
}