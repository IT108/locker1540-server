function makeToast(text) {
    var toastData = {message: text}
    var snackbarContainer = document.querySelector('#toast');
    snackbarContainer.MaterialSnackbar.showSnackbar(toastData);
}

$(document).ready(syncTable());

function syncTable() {
    $.ajax({
        type: 'post',
        url: '/sync',
        data: {'sort': 'name'},
        success: function (data) {
            $('#table').html(data);
            componentHandler.upgradeDom();
        }
    });
}

var dialog1

function openDialog(id) {
    $.ajax({
        type: 'post',
        url: '/open_dialog',
        data: {'id': id},
        success: function (data) {
            $('#dialogBlock').html(data);
            dialog1 = document.querySelector('#user_edit_dialog');
            if (!dialog1.showModal) {
                dialogPolyfill.registerDialog(dialog1);
            }
            dialog1.showModal();
            componentHandler.upgradeDom();
        }
    });
}

function addUserDialog() {
    $.ajax({
        type: 'post',
        url: '/add_user_dialog',
        success: function (data) {
            $('#dialogBlock').html(data);
            dialog1 = document.querySelector('#user_edit_dialog');
            if (!dialog1.showModal) {
                dialogPolyfill.registerDialog(dialog1);
            }
            dialog1.showModal();
            componentHandler.upgradeDom();
        }
    });
}

function addUser() {
    var name = document.getElementById('name').value;
    var card = document.getElementById('card').value;
    var position = $('input[name=options]:checked', '#options-form').val();
    var active = true;
    if (document.getElementById('text-form').checkValidity()) {
        $.ajax({
            type: 'post',
            url: '/add_user',
            data: {
                'name': name,
                'card': card,
                'position': position,
                'active': active
            },
            success: function (data) {
                syncTable();
                dialog1.close();
                makeToast("User added");
            }
        });
    } else {
        document.getElementById("error").innerHTML = "<strong>8 Characters A-F, a-f or 0-9 expected</strong>";
    }
}

function updateUser(id) {
    var name = document.getElementById("name").value;
    var card = document.getElementById('card').value;
    var position = $('input[name=options]:checked', '#options-form').val();
    var active = true;
    if (document.getElementById('text-form').checkValidity()) {
        $.ajax({
            type: 'post',
            url: '/update_user',
            data: {
                'id': id,
                'name': name,
                'card': card,
                'position': position,
                'active': active
            },
            success: function (data) {
                syncTable();
                dialog1.close();
                makeToast("User Updated");
            }
        });
    } else {
        document.getElementById("error").innerHTML = "<strong>8 Characters A-F, a-f or 0-9 expected</strong>";
    }

}

function changeSort(param) {
    $.ajax({
        type: 'post',
        url: '/sync',
        data: {'sort': param},
        success: function (data) {
            $('#table').html(data);
            componentHandler.upgradeDom();
            makeToast('Sorting by ' + param);
        }
    });
}

function toggleUser(id) {
    $.ajax({
        type: 'post',
        url: '/toggle_user',
        data: {'id': id},
        success: function (data) {
            syncTable();
            makeToast('User ' + data);
        }
    });
}

var dialog = document.querySelector('#user_edit_dialog');
if (!dialog.showModal) {
    dialogPolyfill.registerDialog(dialog);
}

function getSerialCard() {
    document.addEventListener("scanner", setCard);
    var data = {action: 'scan'};
    window.postMessage(data,'*');
}

function setCard(data) {
    document.getElementById('card').value = data.detail.barcode;
    document.removeEventListener("scanner", setCard);
}