function makeToast(text) {
    var toastData = {message: text}
    var snackbarContainer = document.querySelector('#toast');
    snackbarContainer.MaterialSnackbar.showSnackbar(toastData);
}

$(document).ready(syncTable());

function syncTable() {
    $.ajax({
        type: 'post',
        url: '/sync_admins',
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
        url: '/open_admin_dialog',
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
        url: '/add_admin_dialog',
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
    var email = document.getElementById('email').value;
    var login = document.getElementById('login').value;
    var password = document.getElementById('password').value;
    if (document.getElementById('text-form').checkValidity()) {
        $.ajax({
            type: 'post',
            url: '/add_admin',
            data: {
                'name': name,
                'email': email,
                'login': login,
                'password': password
            },
            success: function (data) {
                if (data == 'NO') {
                    document.getElementById("error").innerHTML = "<strong>Login must be unique</strong>";
                } else {
                    syncTable();
                    dialog1.close();
                    makeToast("Admin added");
                }
            }
        });
    } else {
        document.getElementById("error").innerHTML = "<strong>All fields required</strong>";
    }
}

function updateUser(id) {
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var login = document.getElementById('login').value;
    if (document.getElementById('text-form').checkValidity()) {
        $.ajax({
            type: 'post',
            url: '/update_admin',
            data: {
                'name': name,
                'email': email,
                'login': login,
                'id': id
            },
            success: function (data) {
                if (data == 'NO') {
                    document.getElementById("error").innerHTML = "<strong>Login must be unique</strong>";
                } else {
                    syncTable();
                    dialog1.close();
                    makeToast("Admin Updated");
                }
            }
        });
    } else {
        document.getElementById("error").innerHTML = "<strong>All fields required</strong>";
    }

}


function deleteUser(id) {


    $.ajax({
        type: 'post',
        url: '/delete_admin',
        data: {
            'id': id
        },
        success: function (data) {
            syncTable();
            dialog1.close();
            makeToast("Admin deleted");
        }
    });

}


function changeSort(param) {
    $.ajax({
        type: 'post',
        url: '/sync_admins',
        data: {'sort': param},
        success: function (data) {
            $('#table').html(data);
            componentHandler.upgradeDom();
            makeToast('Sorting by ' + param);
        }
    });
}


var dialog = document.querySelector('#user_edit_dialog');
if (!dialog.showModal) {
    dialogPolyfill.registerDialog(dialog);
}