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

async function load_messages(phone, id) {
    const url = "/api/get/messages?phone=" + phone + "&entity=" + id
    const response = await fetch(url, {
        method: "GET",
        headers: {"Accept": "application/json", "Content-Type": "application/json"}
    });

    if (selected_dialog) {
        selected_dialog.classList.remove("list-group-item-primary");
        selected_dialog.classList.add("list-group-item-light");
    }
    selected_dialog = document.getElementById(id)
    if (selected_dialog) {
        selected_dialog.classList.remove("list-group-item-light");
        selected_dialog.classList.add("list-group-item-primary");
    }
    let messages = document.getElementById('id_messages')
    if (response.ok) {
        const data = await response.json();
        if (messages) {
            $(messages).empty()
            for (const key in data.messages) {
                let new_mess = $('<div>', {class: "d-flex justify-content-end"}).append(
                    $('<a>', {
                        href: "#",
                        title: data.messages[key]['date'],
                        class: "list-group-item list-group-item-action list-group-item-light",
                        text: data.messages[key]['message'],
                    })
                );
                if (data.messages[key]['out']) {
                    new_mess.addClass("align_right")
                };
                $(messages).append(new_mess);
            }
            $(messages).scrollTop(10000);
        }
    } else {
        document.getElementById("status").textContent = "Ошибка получения сообщений.";
    }
}

async function load_dialogs(phone) {
    const response = await fetch("/api/get/dialogs?phone=" + phone, {
        method: "GET",
        headers: {"Accept": "application/json", "Content-Type": "application/json"}
    });

    if (response.ok) {
        const data = await response.json();
        let dialogs_el = document.getElementById('id_dialogs');
        if (dialogs_el) {
            $('#id_dialogs').empty();
            for (const key in data.dialogs) {
                let new_el = $('<a>', {
                    id: data.dialogs[key].id,
                    class: "list-group-item d-flex justify-content-between align-items-start",
                    href: '#',
                    title: "username: " + data.dialogs[key].username,

                }).on('click', function () {
                        load_messages(phone, data.dialogs[key].id);
                    }
                ).append(
                    $('<div class="ms-2 me-auto">').append(
                        $('<div class="fw-bold">' + data.dialogs[key].title + '</div>')
                    )
                ).append($('<span>', {
                    class: "badge bg-primary rounded-pill",
                    text: data.dialogs[key].unread_count
                }));
                $(dialogs_el).append(new_el)
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

    load_dialogs(phone).then()
}

