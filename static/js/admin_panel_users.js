$(document).on("click", ".edit", function () {
    var row = $(this).closest("tr");
    var name = row.find("td:eq(0)").text();
    var email = row.find("td:eq(1)").text();
    var birthday = row.find("td:eq(2)").text();
    var gender = row.find("td:eq(3)").text();
    var password = row.find("td:eq(4)").text();
    var role = row.find("td:eq(5)").text();

    var input = $(this).parents("tr").find('input[type="text"]');
    input.each(function () {
        if (!$(this).val()) {
            $(this).addClass("error");
            empty = true;
        } else {
            $(this).removeClass("error");
        }
    });

    row.find("td:eq(0)").html(`<input type="text" name="name" class="form-control" value="${name}" required>`);
    row.find("td:eq(1)").html(`<input type="email" name="email" class="form-control" value="${email}" readonly>`);
    row.find("td:eq(2)").html(`<input type="text" name="birthday" class="form-control" value="${birthday}" required>`);
    row.find("td:eq(3)").html(`
    <select name="gender" class="form-control gender-input" id="gender-input">
        <option value="man" ${gender === 'man' ? 'selected' : ''}>man</option>
        <option value="woman" ${gender === 'woman' ? 'selected' : ''}>woman</option>
    </select>
`)
    //row.find("td:eq(3)").html(`<input type="text" name="gender" class="form-control" value="${gender}">`);
    row.find("td:eq(4)").html("********").attr("contenteditable", "false");
    row.find("td:eq(5)").html(`
    <select name="role" class="form-control role-input" id="role-input">
        <option value="user" ${role === 'user' ? 'selected' : ''}>user</option>
        <option value="admin" ${role === 'admin' ? 'selected' : ''}>admin</option>
    </select>
`)
    $(this).removeClass("edit").addClass("save").attr("title", "Save").find("i").removeClass("fa-pencil").addClass("fa-save");
});


$(document).on("click", ".save", function () {
    var row = $(this).closest("tr");
    var name = row.find("td:eq(0) input").val();
    var email = row.find("td:eq(1) input").val();
    var birthday = row.find("td:eq(2) input").val();
    var gender = row.find("td:eq(3) select").val();
    var password = row.find("td:eq(4) input").val();
    var role = row.find("td:eq(5) select").val();

    row.find("td:eq(0)").text(name);
    row.find("td:eq(1)").text(email);
    row.find("td:eq(2)").text(birthday);
    row.find("td:eq(3)").text(gender);
    row.find("td:eq(4)").html("********"); // Змінено на відображення 8 зірочок
    row.find("td:eq(5)").text(role);


    $.post('/update_users', { name: name, email: email, birthday: birthday, gender: gender, role: role }, function (data) {
        $("#displaymessage").html(data);
        $("#displaymessage").show();
        if (data === "Email already exists")
            // Видалити рядок, якщо електронна адреса вже існує
            deleteRow(newRow);
        return;
    });
    $(this).removeClass("save").addClass("edit").attr("title", "Edit").find("i").removeClass("fa-save").addClass("fa-pencil");

});
// Delete row on delete button click



$(document).on("click", ".delete", function () {
    var row = $(this).closest("tr");
    var email = row.find(".email").text(); // Retrieve the email value from the td element
    $.post('/delete_users', { email: email }, function (data) {
        $("#displaymessage").html(data);
        $("#displaymessage").show();
        if (data.includes("User deleted successfully")) {
            row.remove();
        }
    });
});


//add button

document.addEventListener("DOMContentLoaded", function () {
    // Отримати кнопку "Add New"
    var addBtn = document.querySelector(".add-new");

    // Додати обробник події для кнопки "Add New"
    addBtn.addEventListener("click", function () {
        // Створити новий рядок для введення даних користувача
        var newRow = document.createElement("tr");

        // Створити HTML-розмітку для нового рядка
        newRow.innerHTML = `
            <td><input type="text" name="name" id="name" class="form-control name-input" placeholder="Enter name" required></td>
            <td><input type="email" name="email" class="form-control email-input" placeholder="Enter email" required></td>
            <td>
                <input type="text" name="birthday" class="form-control date-input" id="birthday" placeholder="YYYY-MM-DD" required pattern="\d{4}-\d{2}-\d{2}"
                title="Please enter a date in the format YYYY-MM-DD" required>
            </td>
            <td>
                <select name="gender" class="form-control gender-input" id="gender-input">
                    <option value="man">man</option>
                    <option value="woman">woman</option>
                </select>
            </td>
            <td><input type="password" name="password" class="form-control password-input" placeholder="Enter password" required></td>
            <td>
                <select name="role" class="form-control role-input" id="role-input">
                    <option value="admin">admin</option>
                    <option value="user">user</option>
                </select>
            </td>
            <td>
                <a class="add" title="add" data-toggle="tooltip"><i class="fa fa-user-plus"></i></a>
                <a class="save" title="save" data-toggle="tooltip"><i class="fa fa-save"></i></a>
                <a class="delete" title="delete" data-toggle="tooltip"><i class="fa fa-trash-o"></i></a>
            </td>`;

        // Зміна кнопки редагування на кнопку збереження
        var editBtn = newRow.querySelector(".save");
        editBtn.addEventListener("click", function () {
            // Додайте код для збереження даних з нового рядка
            var nameInput = newRow.querySelector(".name-input");
            var emailInput = newRow.querySelector(".email-input");
            var birthdayInput = newRow.querySelector(".date-input");
            var genderInput = newRow.querySelector(".gender-input");
            var passwordInput = newRow.querySelector(".password-input");
            var roleInput = newRow.querySelector(".role-input");
            var name = nameInput.value;
            var email = emailInput.value;
            var birthday = birthdayInput.value;
            var gender = genderInput.value;
            var password = passwordInput.value;
            var role = roleInput.value;

            // Виконати дії для збереження даних
            var row = this.closest("tr");

            this.querySelector("i").classList.remove("fa-save");
            this.querySelector("i").classList.add("fa-pencil");

            // Виконати перевірку електронної адреси на сервері перед збереженням

            //
            // Відправити дані на сервер для збереження
            $.post('/add_users', { name: name, email: email, gender: gender, birthday: birthday, password: password, role: role }, function (data) {
                if (data === "Email already exists") {
                    $("#displaymessage").html(data);
                    $("#displaymessage").show();
                    deleteRow(newRow);
                    return;

                } else {
                    $("#displaymessage").html(data);
                    $("#displaymessage").show();
                    // Видалити рядок, якщо електронна адреса вже існує
                    deleteRow(newRow);
                    return;
                }
            });

            // Видалити рядок після збереження
            row.querySelector(".delete").addEventListener("click", function () {
                row.remove();
            });
        });

        // Отримати таблицю та додати новий рядок
        var tableBody = document.querySelector("tbody");
        tableBody.appendChild(newRow);
    });
});


// Функція видалення рядка
function deleteRow(row) {
    var parentRow = row.parentNode;
    parentRow.removeChild(row);
}
