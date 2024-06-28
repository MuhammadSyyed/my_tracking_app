
let sidebarOpen = false;
const sidebar = document.getElementById('sidebar');

function timedPopup(type, message, goto, session_id) {
    let timerInterval;
    Swal.fire({
        title: message,
        icon: type,
        timer: 1500,
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading();
        },
        willClose: () => {
            clearInterval(timerInterval);
            document.cookie = `session_id=${session_id};`;
            window.location.href = `/${goto}`;
        }
    }).then((result) => {
        if (result.dismiss === Swal.DismissReason.timer) {
        }
    });
}
function openSidebar() {
    if (!sidebarOpen) {
        sidebar.classList.add('sidebar-responsive');
        sidebarOpen = true;
    }
}
function closeSidebar() {
    if (sidebarOpen) {
        sidebar.classList.remove('sidebar-responsive');
        sidebarOpen = false;
    }
}

function logout(session_id) {

    Swal.fire({
        title: "Are you sure?",
        text: "You want to close this session?",
        icon: "warning",
        showCancelButton: true,

        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes"

    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/logout', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "Session-Id": session_id
                },
            }).then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
                .then(data => {
                    document.location.href = '/';
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                });
        }
    });
}

function gotoDashboard(session_id) {
    document.cookie = `session_id=${session_id}`;
    window.location.href = '/dashboard';
}

function goBack() {
    window.history.back();
}
