function changeValue(api, id, field, value) {
    fetch(api, {
        method: "POST",
        headers: {"Authorization": `Bearer ${sessionStorage.getItem("token")}`},
        body: JSON.stringify({
            id: id,
            field: field,
            value: value
        })
    }).then(response => response.json()).then(data => {
        if (data.code !== 1) {
            alert(data.result)
        }
    })
}

function renderInput(id, field, value, changeApi) {
    let inputDom = document.createElement("input")
    inputDom.type = "text"
    inputDom.classList.add("form-control")
    inputDom.value = value

    inputDom.addEventListener("change", function (ev) {
        changeValue(changeApi, id, field, ev.target.value)
    })

    return inputDom
}