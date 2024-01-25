async function load_status(phone) {
    document.getElementById("status").textContent = "Запрос...";

    const response = await fetch("/api/check/status?phone=" + phone, {
        method: "GET",
        headers: {"Accept": "application/json", "Content-Type": "application/json"}
    });

    if (response.ok) {
        const data = await response.json();
        document.getElementById("status").textContent = "Статус пользователя: " + data['status'];
    } else {
        document.getElementById("status").textContent = "Ошибка получения статуса.";
    }
}

let selected_dialog = null

async function load_messages(element_id, phone, id){
    const url = "/api/get/messages?phone=" + phone + "&entity=" + id
    const response = await fetch(url, {
        method: "GET",
        headers: {"Accept": "application/json", "Content-Type": "application/json"}
    });

    if (selected_dialog) {
        selected_dialog.classList.remove("list-group-item-primary");
        selected_dialog.classList.add("list-group-item-light");
    }
    selected_dialog = document.getElementById(element_id)
    if (selected_dialog) {
        selected_dialog.classList.remove("list-group-item-light");
        selected_dialog.classList.add("list-group-item-primary");
    }
    if (response.ok) {
        const data = await response.json();
        if (selected_dialog) {
            selected_dialog.innerHTML = "";
            for (const key in data.messages) {
                let align_right = data.messages[key]['out'] ? " align_right":  ""
                selected_dialog.innerHTML +=
                    "<div class='d-flex justify-content-end" + align_right + "'>" +
                    "<a title=\"" + data.messages[key]['date'] + "\" href=\"#\"  id=\"" + key +
                    "\" class=\"list-group-item list-group-item-action list-group-item-light\">\n" +
                    data.messages[key]['message'] + "</a></div>"
            }
        }
    } else {
        document.getElementById("status").textContent = "Ошибка получения сообщений.";
    }
}

async function load_dialogs(element_id, phone) {
    const response = await fetch("/api/get/dialogs?phone=" + phone, {
        method: "GET",
        headers: {"Accept": "application/json", "Content-Type": "application/json"}
    });

    if (response.ok) {
        const data = await response.json();
        if (document.getElementById(element_id)) {
            document.getElementById(element_id).innerHTML = "";
            for (const key in data.dialogs) {
                document.getElementById(element_id).innerHTML +=
                    // "<a href=\"#\" onclick='load_messages(\"id_messages\", " + phone + ", " + key + ")' " +
                    // "id=\"" + key + "\" " +
                    // "class=\"list-group-item list-group-item-action list-group-item-light\">\n" +
                    // data.dialogs[key] +
                    // "<span class=\"badge bg-primary rounded-pill text-right\">0</span>\n</a>"
                    "<a href=\"#\" onclick='load_messages(\"id_messages\", " + phone + ", " + key + ")' " +
                        "class=\"list-group-item d-flex justify-content-between align-items-start\" " +
                        "id=\"" + key + "\">" +
                        "<div class=\"ms-2 me-auto\">\n" +
                            "<div class=\"fw-bold\">" + data.dialogs[key] + "</div>\n" +
                        "</div>\n" +
                        "<span class=\"badge bg-primary rounded-pill\">0</span>\n" +
                    "</a>"
            }
        }
    } else {
        document.getElementById("status").textContent = "Ошибка получения диалогов.";
    }
}

function onload() {
    let phone = document.getElementById("phone").value;
    load_status(phone).then();

    const interval = setInterval(
        function () {
            load_status(phone).then();
        },
        15000
    );

    load_dialogs('id_dialogs', phone)
}

