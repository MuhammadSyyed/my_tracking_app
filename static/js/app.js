
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

function gotoMap(session_id) {
    document.cookie = `session_id=${session_id}`;
    window.location.href = '/map';
}

function gotoAddLoc(session_id) {
    document.cookie = `session_id=${session_id}`;
    window.location.href = '/addloc';
}

function gotoLocation(session_id) {
    document.cookie = `session_id=${session_id}`;
    window.location.href = '/location';
}

function deleteLocation(loc_id,session_id){
    document.cookie = `session_id=${session_id}`;
    window.location.href = `/delete_loc/${loc_id}`;
}

function gotoSearch(session_id) {
    document.cookie = `session_id=${session_id}`;
    window.location.href = '/search';
}

function goBack() {
    window.history.back();
}

async function sendLocation() {
    const selectElement = document.getElementById('current_loc');
    const selectedValue = selectElement.value;
    console.log(selectedValue);

    try {
        const response = await fetch('/set_loc', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Cookie': `session_id:${'{{session_id}}'}`,
            },
            body: JSON.stringify({ location: selectedValue })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }

        const data = await response.json();
        console.log('Success:', data);
    } catch (error) {
        console.error('Error:', error);
    }
}